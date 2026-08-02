"""Console summary — the CLI equivalent of the spec's "final summary in chat" step.

Never prints a raw/unmasked transaction row. Headline numbers only, plus
whatever caveat the data itself forces (short window, one transaction skewing
an average, a partial month).
"""

def _inr(n: float) -> str:
    return f"Rs {n:,.2f}"


def print_summary(state: dict) -> None:
    if state.get("halted"):
        print("\n=== Report NOT generated ===")
        for e in state.get("errors", []):
            print(f"  - {e}")
        print("\nNo file was written. Fix the issue above and re-run.")
        return

    m = state["metrics"]
    cache_stats = state.get("cache_stats", {})

    print("\n=== Statement report ===")
    print(f"Account {m['account']} · {m['period']} · {m['n_txn']} transactions over {m['span_days']} days")
    print(f"Balance: {_inr(m['opening_balance'])} -> {_inr(m['closing_balance'])}")
    print()
    print(f"Total outflow:        {_inr(m['outflow'])}")
    print(f"  of which transfers: {_inr(m['self_transfers'])}")
    print(f"  of which invested:  {_inr(m['investments'])}")
    print(f"Spend (excl. both):   {_inr(m['true_spend'])}")
    print(f"Income:               {_inr(m['income'])}")
    savings = "not computable (no income this period)" if m["savings_rate"] is None else f"{m['savings_rate']}%"
    print(f"Savings rate:         {savings}")
    print()
    print("Top categories:")
    for c in m["categories"][:5]:
        print(f"  {c['cat']:<20} {_inr(c['amt']):>16}   {c['pct']}%   ({c['n']} txn)")

    review_n = len(m["review"])
    if review_n:
        print(f"\n{review_n} transaction(s) need manual review — filed under a best guess, not certain.")
    else:
        print("\nEverything classified with high confidence — nothing needs review.")

    if cache_stats:
        print(
            f"\nLLM: {cache_stats.get('calls', 0)} call(s), "
            f"{cache_stats.get('hits', 0)} cache hit(s)."
        )

    print(f"\nMasked: account number, UPI/IMPS reference numbers, ACH mandate IDs, IFSC codes (last 4 shown).")
    print("Not masked: counterparty names (kept — the report needs them).")

    if m["span_days"] <= 10:
        print(
            f"\nCaveat: only a {m['span_days']}-day window — too short to read as a spending pattern, "
            f"especially if the top categories above are one-off transactions."
        )
    if len(m["monthly"]) > 1:
        print("Caveat: the statement spans partial months — the month split is a windowed total, not a trend.")

    print(f"\nReport written to: {state.get('output_path')}")
