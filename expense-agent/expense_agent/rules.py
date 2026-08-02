"""Ordered categorization rules.

Rule order is load-bearing: Investments / Rent / Self-Transfers must be tested
before the generic person-to-person-transfer fallback, or e.g. a large rent IMPS
payment gets misfiled as an anonymous transfer. See config.py for the keyword
tables this module walks.

Only transactions with no reliable structural or keyword signal are queued for
the LLM — and only the bare merchant fragment (never the full narration, never
amounts) is what it will see.
"""

from dataclasses import dataclass

from . import cache as cache_mod
from . import config
from .parsing import RawTransaction


@dataclass
class CategoryResult:
    category: str | None       # None while needs_llm is True
    confidence: str | None     # "high" | "medium" | "low"; None while needs_llm
    note: str
    needs_llm: bool = False
    llm_candidate: str | None = None   # a weak keyword guess, offered as a hint
    fragment: str | None = None        # merchant-only text — the only thing the LLM sees


def _decompose(narration: str) -> tuple[str, str | None]:
    """Split a masked narration into (mode, counterparty-or-merchant-fragment)."""
    parts = [p.strip() for p in narration.split("/")]
    mode = parts[0][:4].upper() if parts else ""
    if mode in ("UPI", "IMPS") and len(parts) >= 4:
        counterparty = parts[3] if parts[1] in ("P2A", "P2M") else parts[2]
        fragment = " ".join(counterparty.split())
        return mode, (fragment or None)
    if narration.upper().startswith("ACH-DR-"):
        return "ACH", narration[7:].split("-")[0].strip().title()
    return mode, None


def extract_merchant_fragment(narration: str) -> str | None:
    """Pull just the counterparty/merchant token out of a masked narration.

    This is both the LLM's entire input and the merchant-cache key — it must
    never carry a reference number, bank name, or amount.
    """
    _, fragment = _decompose(narration)
    return fragment


def display_desc(narration: str) -> str:
    """A short human-readable label for the transaction table (e.g. "UPI · Zomato")."""
    mode, fragment = _decompose(narration)
    if fragment and mode in ("UPI", "IMPS"):
        return f"{mode} · {fragment}"
    if fragment and mode == "ACH":
        return f"ACH mandate · {fragment}"
    return narration[:60]


def apply_manual_override(narration: str, cache: cache_mod.MerchantCache) -> CategoryResult | None:
    """A user-entered correction (via `scripts/correct.py`) wins over every rule
    and every keyword, unconditionally — a human said so, so this is checked
    first, before any other rule runs, not just for the transactions rules
    would otherwise send to the LLM.

    Only merchant-fragment-keyed corrections exist (see cache.py) — a
    correction to one merchant applies to every transaction with that same
    merchant fragment, past and future, not to a single dated transaction.
    """
    _, fragment = _decompose(narration)
    if not fragment:
        return None
    cached = cache.get(fragment)
    if cached and cached.source == "manual":
        return CategoryResult(cached.category, "high", cached.reason)
    return None


def _matches_any(text: str, keywords: list[str]) -> bool:
    return any(kw in text for kw in keywords)


def _match_merchant_keyword(text: str):
    """Return (category, strength) for the first keyword table hit, or None."""
    for category, keywords, strength in config.MERCHANT_KEYWORDS:
        if _matches_any(text, keywords):
            return category, strength
    return None


def is_self_transfer(narration: str, holder_name: str | None) -> bool:
    """The /P2V/ marker is a reliable structural signal on its own.

    The `holder_name` fallback is deliberately conservative: it only looks at
    the counterparty field (never the full narration — UPI narrations carry a
    free-text remarks field that can incidentally contain the sender's own
    name on a transfer to someone else entirely), and it requires every
    significant token of the holder's name to appear there, not just one — a
    single-token match (e.g. a shared surname) is exactly the false-positive
    this guards against: "AGRIMA DUTT SHARMA" is not "Arjit Sharma" just
    because they share a surname.
    """
    low = narration.lower()
    if config.SELF_TRANSFER_MARKER in low:
        return True
    if holder_name:
        tokens = [t.upper() for t in holder_name.split() if len(t) >= 3]
        _, fragment = _decompose(narration)
        if tokens and fragment:
            frag_upper = fragment.upper()
            if all(t in frag_upper for t in tokens):
                return True
    return False


def categorize_transaction(txn: RawTransaction, holder_name: str | None = None) -> CategoryResult:
    text = txn.narration_masked
    low = text.lower()

    if _matches_any(low, config.INVESTMENT_KEYWORDS):
        return CategoryResult("Investments", "high", "")

    if config.RENT_TOKEN in low:
        return CategoryResult("Rent", "high", "")

    if is_self_transfer(text, holder_name):
        return CategoryResult("Self Transfers", "high", "")

    hit = _match_merchant_keyword(low)
    if hit and hit[1] == "strong":
        return CategoryResult(hit[0], "high", "")

    if txn.credit > 0:
        return CategoryResult(
            "Salary/Income", "low",
            "Credit with no matching keyword — confirm the source.",
        )

    if hit and hit[1] == "weak":
        return CategoryResult(
            None, None, "",
            needs_llm=True, llm_candidate=hit[0],
            fragment=extract_merchant_fragment(text),
        )

    if "/p2a/" in low or low.startswith("imps"):
        # A bare person-to-person transfer. No model can infer intent from a
        # human name alone, so this is never queued for the LLM — it is
        # deterministically low-confidence and goes straight to the review panel.
        return CategoryResult(
            "Transfers (P2P)", "low",
            "Person-to-person transfer — purpose not inferable from narration.",
        )

    if "/p2m/" in low:
        return CategoryResult(
            None, None, "",
            needs_llm=True, llm_candidate=None,
            fragment=extract_merchant_fragment(text),
        )

    return CategoryResult("Uncategorized", "low", "No recognisable signal.")
