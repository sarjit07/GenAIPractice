#!/usr/bin/env python3
"""Correct a miscategorized merchant, permanently.

The fragment is the text after "· " in the report's Description column
(e.g. the row "UPI · Blinkit" -> fragment "Blinkit"). A correction applies to
every transaction with that merchant fragment, past and future runs, not just
one dated transaction — it overrides the rules and the LLM unconditionally.

Usage:
    python scripts/correct.py "Blinkit" "Shopping"
    python scripts/correct.py "Blinkit" "Shopping" --reason "This one was electronics, not groceries"
    python scripts/correct.py --remove "Blinkit"      # revert to automatic classification
    python scripts/correct.py --list                  # show every correction currently applied

Re-run cli.py after this to regenerate the report with the correction applied.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from expense_agent import cache as cache_mod
from expense_agent import config


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("fragment", nargs="?", help='Merchant fragment, e.g. "Blinkit"')
    parser.add_argument("category", nargs="?", help="One of: " + ", ".join(config.ALL_CATEGORIES))
    parser.add_argument("--reason", default="Manually corrected.")
    parser.add_argument("--remove", metavar="FRAGMENT", help="Remove a correction, reverting to automatic classification")
    parser.add_argument("--list", action="store_true", help="List every correction currently applied")
    parser.add_argument("--cache-path", default=config.DEFAULT_CACHE_PATH)
    args = parser.parse_args()

    mc = cache_mod.MerchantCache(args.cache_path)

    if args.list:
        manual = mc.entries(source="manual")
        if not manual:
            print("No manual corrections yet.")
            return 0
        width = max(len(f) for f in manual)
        for frag, entry in sorted(manual.items()):
            print(f"  {frag:<{width}}  ->  {entry.category}")
        return 0

    if args.remove:
        if mc.remove(args.remove):
            mc.save()
            print(f"Removed the correction for '{args.remove}'. It will be classified automatically next run.")
        else:
            print(f"No manual correction found for '{args.remove}'.")
        return 0

    if not args.fragment or not args.category:
        parser.error("fragment and category are required, unless --remove or --list is used")

    if args.category not in config.ALL_CATEGORIES:
        print(f"'{args.category}' is not a known category. Choose one of:")
        for c in config.ALL_CATEGORIES:
            print(f"  {c}")
        return 1

    mc.set(args.fragment, cache_mod.CachedClassification(
        category=args.category, confidence="high", reason=args.reason, source="manual",
    ))
    mc.save()
    print(f"'{args.fragment}' will now always be classified as '{args.category}'.")
    print("Re-run cli.py to regenerate the report with this correction applied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
