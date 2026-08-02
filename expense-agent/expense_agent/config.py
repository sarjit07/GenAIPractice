"""Fixed constants: category taxonomy, keyword rules, LLM schema, validated palette.

Keeping these in one module means the deterministic rule engine (rules.py) and the
LLM classifier (llm_client.py) agree on the exact same category spelling — a typo'd
category string in one place silently splits a category in the report.
"""

# ---------------------------------------------------------------------------
# Category taxonomy
# ---------------------------------------------------------------------------

# Categories the ordered rules resolve deterministically — never offered to the LLM.
# (Investments/Rent/Self-Transfers have unambiguous structural signals: mandate
# narrations, a "rent" remark, and the /P2V/ self-link marker respectively. Giving
# the LLM a slot to guess these only invites it to steal transactions that belong
# here by construction.)
RULE_ONLY_CATEGORIES = ["Investments", "Rent", "Self Transfers"]

# Categories the LLM may choose between, for transactions the rules can't place.
LLM_CATEGORIES = [
    "Groceries",
    "Food & Dining",
    "Utilities",
    "Transport",
    "Healthcare",
    "Entertainment",
    "Shopping",
    "ATM Withdrawals",
    "Bank Charges",
    "Salary/Income",
    "Transfers (P2P)",
    "Uncategorized",
]

ALL_CATEGORIES = RULE_ONLY_CATEGORIES + LLM_CATEGORIES

CONFIDENCE_LEVELS = ["high", "medium", "low"]

# ---------------------------------------------------------------------------
# Ordered keyword rules — order is load-bearing, see rules.py
# ---------------------------------------------------------------------------

INVESTMENT_KEYWORDS = [
    "zerodha", "indian clearing corp", "groww", "mutual fund", "smallcase",
    "nps ", "kuvera", "coin dcx", "icccl",
]

MERCHANT_KEYWORDS = [
    # (category, [keywords], strength) — "strong" resolves outright,
    # "weak" is ambiguous enough to route through the LLM instead.
    ("Groceries", ["blinkit", "zepto", "bigbasket", "instamart", "dmart", "grofers",
                   "reliance fresh", "more retail", "spencer", "licious",
                   "country delight"], "strong"),
    ("Food & Dining", ["zomato", "swiggy", "dominos", "mcdonald", "starbucks", "cafe",
                        "coffee", "restaurant", "biryani", "bakery", "kitchen",
                        "eatery", "burger", "pizza", "chai"], "strong"),
    ("Food & Dining", ["the roots"], "weak"),  # name-shaped, not a certain restaurant match
    ("Utilities", ["airtel", "jio", "vodafone", "vi ltd", "bses", "electricity",
                   "tata power", "adani elec", "nagar niga", "municipal", "broadband",
                   "act fibernet", "gas ltd", "indane", "water board", "recharge",
                   "dth", "tata sky"], "strong"),
    ("Transport", ["uber", "ola ", "rapido", "irctc", "metro", "indigo", "spicejet",
                   "vistara", "fuel", "hpcl", "iocl", "bpcl", "petrol", "fastag",
                   "parking", "redbus"], "strong"),
    ("Healthcare", ["clinic", "hospital", "pharma", "apollo", "medplus", "diagnostic",
                     "pathology", "dental", "1mg", "netmeds", "practo", "lab "], "strong"),
    ("Entertainment", ["playo", "bookmyshow", "netflix", "spotify", "prime video",
                        "hotstar", "pvr", "inox", "gaming", "steam",
                        "youtube prem"], "strong"),
    ("Shopping", ["amazon", "flipkart", "myntra", "ajio", "nykaa", "decathlon", "ikea",
                  "croma", "reliance digital", "meesho", "tata cliq"], "strong"),
    ("ATM Withdrawals", ["cwdr", "atm-cash", "atm cash", "nfs/cash"], "strong"),
    ("Bank Charges", ["charges", "chrg", "gst @", "int.coll", "penalty",
                       "annual fee", "amc "], "strong"),
    ("Salary/Income", ["salary", "sal-", "payroll"], "strong"),
]

RENT_TOKEN = "rent"
SELF_TRANSFER_MARKER = "/p2v/"

# ---------------------------------------------------------------------------
# LLM classification schema (vLLM guided_json target)
# ---------------------------------------------------------------------------

CLASSIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"enum": LLM_CATEGORIES},
        "confidence": {"enum": CONFIDENCE_LEVELS},
        # maxLength here is enforced by the grammar constraint itself, at the
        # token level — the generation gets cut off exactly at this length,
        # mid-word if that's where it lands, with no chance for our own
        # word-boundary trim in llm_client._truncate_at_word() to help (it
        # never sees anything longer than this). So this is set generously,
        # and the actual cosmetic 140-char display cap is applied in Python
        # afterwards, where a word boundary can be found.
        "reason": {"type": "string", "maxLength": 220},
    },
    "required": ["category", "confidence", "reason"],
    "additionalProperties": False,
}

CLASSIFY_SYSTEM_PROMPT = (
    "You classify a single Indian bank-statement merchant-name fragment into exactly one "
    "category from this fixed list: " + ", ".join(LLM_CATEGORIES) + ". "
    "You are given only the merchant name fragment — no amount, date, or account data. "
    "If the fragment gives no real signal, choose Uncategorized with confidence low. "
    "Respond with JSON matching the required schema only."
)

# ---------------------------------------------------------------------------
# Validated chart palette — hex values copied verbatim from the reference report,
# which already ran these through the dataviz skill's palette validator (light AND
# dark mode, adjacent + wrap-around pairs). This standalone pipeline has no access
# to that validator, so the palette is frozen here rather than re-derived.
# ---------------------------------------------------------------------------

PALETTE_LIGHT = {
    "s1": "#2a78d6", "s2": "#eb6834", "s3": "#1baf7a",
    "s4": "#eda100", "s5": "#e87ba4", "s6": "#008300",
}
PALETTE_DARK = {
    "s1": "#3987e5", "s2": "#d95926", "s3": "#199e70",
    "s4": "#c98500", "s5": "#d55181", "s6": "#008300",
}

# ---------------------------------------------------------------------------
# Non-spend categories — excluded from the headline "spend" figure but included
# in "total outflow" (see metrics.py)
# ---------------------------------------------------------------------------

NON_SPEND_CATEGORIES = {"Self Transfers", "Investments"}

DEFAULT_CACHE_PATH = ".cache/merchant_categories.json"
DEFAULT_VLLM_BASE_URL = "http://localhost:8000/v1"
DEFAULT_VLLM_MODEL = "expense-cat"
