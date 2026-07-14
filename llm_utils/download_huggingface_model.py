#!/usr/bin/env python3
"""Download the full set of artifact files for a Hugging Face model repo into a local
folder (not the hidden ~/.cache/huggingface cache) — every file: weights, config,
tokenizer, README, license, everything.

Usage:
    python download_model.py <hf_repo_id> [--out-dir DIR] [--token HF_TOKEN]

Example:
    python download_model.py mistralai/Mistral-7B-v0.1
    # -> downloads into ./models/Mistral-7B-v0.1/
"""
import argparse
import os

from huggingface_hub import snapshot_download


def main():
    parser = argparse.ArgumentParser(description="Download all files of a Hugging Face model repo locally.")
    parser.add_argument("model", help="Hugging Face repo id, e.g. mistralai/Mistral-7B-v0.1")
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Local folder to download into (default: ./models/<repo-name>/)",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("HF_TOKEN"),
        help="Hugging Face access token for gated models (or set the HF_TOKEN env var)",
    )
    args = parser.parse_args()

    out_dir = args.out_dir or os.path.join("models", args.model.split("/")[-1])
    os.makedirs(out_dir, exist_ok=True)

    print(f"Downloading ALL files from '{args.model}' into: {out_dir}")
    local_path = snapshot_download(
        repo_id=args.model,
        local_dir=out_dir,
        token=args.token,
    )
    print(f"\nDone. Files are at: {local_path}")

    print("\nDownloaded files:")
    for root, _dirs, files in os.walk(local_path):
        for f in files:
            full = os.path.join(root, f)
            size_mb = os.path.getsize(full) / 1e6
            rel = os.path.relpath(full, local_path)
            print(f"  {rel:<45} {size_mb:>10,.1f} MB")


if __name__ == "__main__":
    main()
