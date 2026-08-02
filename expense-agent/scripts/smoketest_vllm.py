#!/usr/bin/env python3
"""Quick sanity check for the vLLM server, run before the full pipeline.

Checks: the server is up and lists a model, and one guided_json call actually
returns valid, schema-conforming JSON. Run this first when debugging — it's
much faster than tracing the failure through the whole graph.

    python scripts/smoketest_vllm.py [--base-url http://localhost:8000/v1] [--model expense-cat]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from expense_agent import config, llm_client


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=config.DEFAULT_VLLM_BASE_URL)
    parser.add_argument("--model", default=config.DEFAULT_VLLM_MODEL)
    args = parser.parse_args()

    print(f"1) Checking {args.base_url}/models ...")
    try:
        from openai import OpenAI

        client = OpenAI(base_url=args.base_url, api_key="not-needed", timeout=10.0)
        models = client.models.list()
        names = [m.id for m in models.data]
        print(f"   OK — server is up. Models available: {names}")
        if args.model not in names:
            print(f"   WARNING: '{args.model}' is not in that list — check --served-model-name on the server.")
    except Exception as e:
        print(f"   FAILED: {e}")
        print("   Is the vLLM server running? See README.md for the `vllm serve` command.")
        return 1

    print(f"\n2) Guided-decoding call against '{args.model}' ...")
    try:
        result = llm_client.classify_merchant(
            "SOME RANDOM CAFE", candidate_hint=None,
            base_url=args.base_url, model=args.model,
        )
        print(f"   OK — got: category={result.category!r} confidence={result.confidence!r} reason={result.reason!r}")
        if result.category == "Uncategorized" and "LLM call failed" in result.reason:
            print("   WARNING: that's the failure fallback, not a real model response — see the error above it.")
            return 1
    except Exception as e:
        print(f"   FAILED: {e}")
        return 1

    print("\nAll checks passed — the server is ready for the full pipeline.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
