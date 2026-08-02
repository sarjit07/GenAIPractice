"""Deterministic aggregation + the reconciliation gate.

Nothing in this module talks to the LLM. Every number in the final report comes
from here — the graph never lets prose or a model produce a total.
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

from .parsing import RawTransaction
from .rules import CategoryResult, display_desc

RECONCILE_TOLERANCE = 0.01


@dataclass
class CategorizedTransaction:
    date: str
    day_label: str
    month_label: str
    desc: str
    detail: str
    debit: float
    credit: float
    balance: float
    category: str
    confidence: str
    note: str


def build_categorized(txn: RawTransaction, result: CategoryResult) -> CategorizedTransaction:
    if result.category is None or result.confidence is None:
        raise ValueError(
            "build_categorized() called on an unresolved (needs_llm) result — "
            "the LLM/fallback branch must resolve category+confidence first"
        )
    return CategorizedTransaction(
        date=txn.date, day_label=txn.day_label, month_label=txn.month_label,
        desc=display_desc(txn.narration_masked), detail=txn.narration_masked,
        debit=txn.debit, credit=txn.credit, balance=txn.balance,
        category=result.category, confidence=result.confidence, note=result.note,
    )


def reconcile(
    opening_balance: float, closing_balance: float, txns: list[CategorizedTransaction]
) -> tuple[bool, str]:
    """The hard gate: if this fails, the graph halts before rendering anything.

    Catches dropped rows, the `" "`-amount parsing bug, duplicated rows, and
    sign errors — the single most valuable check in the whole pipeline.
    """
    total_debits = round(sum(t.debit for t in txns), 2)
    total_credits = round(sum(t.credit for t in txns), 2)
    expected_closing = round(opening_balance - total_debits + total_credits, 2)

    if abs(expected_closing - closing_balance) >= RECONCILE_TOLERANCE:
        return False, (
            f"Balance does not reconcile: opening {opening_balance:.2f} - debits "
            f"{total_debits:.2f} + credits {total_credits:.2f} = {expected_closing:.2f}, "
            f"but the statement's own closing balance is {closing_balance:.2f}. "
            f"This usually means a row was dropped or misparsed."
        )

    by_cat = defaultdict(float)
    for t in txns:
        by_cat[t.category] += t.debit
    category_sum = round(sum(by_cat.values()), 2)
    if abs(category_sum - total_debits) >= RECONCILE_TOLERANCE:
        return False, (
            f"Category totals ({category_sum:.2f}) do not sum to total debits "
            f"({total_debits:.2f}) — a transaction was likely counted twice or dropped "
            f"during categorization."
        )

    return True, "Reconciled."


def _txn_dict(t: CategorizedTransaction) -> dict:
    return {
        "date": t.date, "day": t.day_label, "month": t.month_label,
        "desc": t.desc, "detail": t.detail,
        "debit": t.debit, "credit": t.credit, "balance": t.balance,
        "cat": t.category, "conf": t.confidence, "note": t.note,
    }


def compute_metrics(
    account_masked: str,
    period: str,
    opening_balance: float,
    closing_balance: float,
    txns: list[CategorizedTransaction],
) -> dict:
    income = round(sum(t.credit for t in txns), 2)
    outflow = round(sum(t.debit for t in txns), 2)

    by_cat_amt: dict[str, float] = defaultdict(float)
    by_cat_cnt: dict[str, int] = defaultdict(int)
    for t in txns:
        if t.debit:
            by_cat_amt[t.category] += t.debit
            by_cat_cnt[t.category] += 1

    self_transfers = round(by_cat_amt.get("Self Transfers", 0.0), 2)
    investments = round(by_cat_amt.get("Investments", 0.0), 2)
    # Self-transfers and investment mandates are not consumption — excluded from
    # "spend" but still counted in "outflow".
    true_spend = round(outflow - self_transfers - investments, 2)
    net = round(income - outflow, 2)
    # Guard the division: a statement window with no credits must report the
    # savings rate as not computable, never a bare 0% or a ZeroDivisionError.
    savings_rate = round(net / income * 100, 1) if income > 0 else None

    categories = sorted(
        [
            {
                "cat": k,
                "amt": round(v, 2),
                "n": by_cat_cnt[k],
                "pct": round(v / outflow * 100, 1) if outflow else 0.0,
            }
            for k, v in by_cat_amt.items()
        ],
        key=lambda c: -c["amt"],
    )

    by_day: dict[str, float] = defaultdict(float)
    by_month: dict[str, dict] = defaultdict(lambda: {"spend": 0.0, "income": 0.0})
    day_label_by_date: dict[str, str] = {}
    for t in txns:
        by_day[t.date] += t.debit
        by_month[t.month_label]["spend"] += t.debit
        by_month[t.month_label]["income"] += t.credit
        day_label_by_date[t.date] = t.day_label

    days = sorted(by_day.keys())
    if days:
        span_days = (
            datetime.strptime(days[-1], "%Y-%m-%d") - datetime.strptime(days[0], "%Y-%m-%d")
        ).days + 1
    else:
        span_days = 0

    daily = [
        {"date": d, "label": day_label_by_date[d], "amt": round(by_day[d], 2)}
        for d in days
    ]
    monthly = [
        {"month": m, "spend": round(v["spend"], 2), "income": round(v["income"], 2)}
        for m, v in by_month.items()
    ]

    txn_dicts = [_txn_dict(t) for t in txns]
    top10 = sorted(txn_dicts, key=lambda t: -t["debit"])[:10]
    review = [t for t in txn_dicts if t["conf"] == "low"]

    avg_daily_spend = round(true_spend / span_days, 2) if span_days else 0.0

    return {
        "account": account_masked,
        "period": period,
        "opening_balance": opening_balance,
        "closing_balance": closing_balance,
        "n_txn": len(txns),
        "span_days": span_days,
        "income": income,
        "outflow": outflow,
        "self_transfers": self_transfers,
        "investments": investments,
        "true_spend": true_spend,
        "net": net,
        "savings_rate": savings_rate,
        "avg_daily_spend": avg_daily_spend,
        "categories": categories,
        "daily": daily,
        "monthly": monthly,
        "top10": top10,
        "review": review,
        "txns": txn_dicts,
    }
