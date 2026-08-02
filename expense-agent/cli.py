#!/usr/bin/env python3
"""Entrypoint: python cli.py <csv> [--holder-name NAME] [--no-llm] [...]

Two-process setup: this talks HTTP to a vLLM OpenAI-compatible server that must
already be running (see README.md). Use --no-llm to run the deterministic rule
engine only, with no network calls at all — useful for testing the pipeline
without a server up.
"""

import argparse
import os
import sys

from dotenv import load_dotenv

from expense_agent import config
from expense_agent.graph import run_pipeline


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", help="Path to the Axis Bank statement CSV")
    parser.add_argument(
        "--holder-name", default=os.environ.get("HOLDER_NAME"),
        help="Account holder's name, used to help detect self-transfers",
    )
    parser.add_argument(
        "--no-llm", action="store_true",
        help="Skip the LLM entirely; resolve ambiguous transactions with a rule-based fallback",
    )
    parser.add_argument(
        "--vllm-base-url", default=os.environ.get("VLLM_BASE_URL", config.DEFAULT_VLLM_BASE_URL),
    )
    parser.add_argument(
        "--vllm-model", default=os.environ.get("VLLM_MODEL", config.DEFAULT_VLLM_MODEL),
    )
    parser.add_argument(
        "--cache-path", default=os.environ.get("CACHE_PATH", config.DEFAULT_CACHE_PATH),
    )
    parser.add_argument(
        "--output", default=os.environ.get("OUTPUT_PATH", "outputs/statement-report.html"),
        help="Where to write the report (default: outputs/statement-report.html)",
    )
    args = parser.parse_args()

    result = run_pipeline(
        csv_path=args.csv_path,
        holder_name=args.holder_name,
        no_llm=args.no_llm,
        vllm_base_url=args.vllm_base_url,
        vllm_model=args.vllm_model,
        cache_path=args.cache_path,
        output_path=args.output,
    )

    return 1 if result.get("halted") else 0


if __name__ == "__main__":
    sys.exit(main())
