#!/usr/bin/env python3
"""Download any Hugging Face model and run it locally with vLLM (Metal-accelerated on Apple Silicon
via the vllm-metal plugin: https://github.com/vllm-project/vllm-metal).

Usage:
    python run_hf_model.py <hf_repo_id> [--prompt "..."] [--max-tokens N] [--token HF_TOKEN]

Examples:
    python run_hf_model.py Qwen/Qwen2.5-0.5B-Instruct
    python run_hf_model.py meta-llama/Llama-3.2-3B-Instruct --prompt "What is a reducer in LangGraph?"
"""
import argparse
import os

from huggingface_hub import snapshot_download
from vllm import LLM, SamplingParams


def download_model(repo_id: str, token: str | None) -> str:
    print(f"Downloading '{repo_id}' from the Hugging Face Hub (cached under ~/.cache/huggingface)...")
    local_path = snapshot_download(repo_id=repo_id, token=token)
    print(f"Model files ready at: {local_path}")
    return local_path


def run(local_path: str, prompt: str, max_tokens: int, temperature: float) -> str:
    print("Loading model into vLLM...")
    llm = LLM(model=local_path)
    sampling_params = SamplingParams(temperature=temperature, max_tokens=max_tokens)

    try:
        # Chat-formatted models (most instruct models) — uses the tokenizer's chat template.
        outputs = llm.chat([{"role": "user", "content": prompt}], sampling_params)
    except Exception:
        # Base / non-chat models — fall back to raw completion.
        outputs = llm.generate([prompt], sampling_params)

    return outputs[0].outputs[0].text.strip()


def main():
    # parser = argparse.ArgumentParser(description="Download a Hugging Face model and run it on vLLM.")
    # parser.add_argument("model", help="Hugging Face repo id, e.g. Qwen/Qwen2.5-0.5B-Instruct")
    # parser.add_argument("--prompt", default="Explain what an AI agent is, in two sentences.")
    # parser.add_argument("--max-tokens", type=int, default=200)
    # parser.add_argument("--temperature", type=float, default=0.7)
    # parser.add_argument(
    #     "--token",
    #     default=os.environ.get("HF_TOKEN"),
    #     help="Hugging Face access token for gated models (or set the HF_TOKEN env var)",
    # )
    # args = parser.parse_args()
    model = 'mistralai/Mistral-7B-Instruct-v0.2'
    token = 'hf_xxx'
    prompt = "Explain what an AI agent is, in two sentences."
    max_tokens = 200
    temperature = 0.7
    print(f"Downloading model {model} from the Hugging Face Hub (cached under ~/.cache/huggingface)...")
    local_path = download_model(model, token)
    response = run(local_path, prompt, max_tokens, temperature)

    print("\n--- Prompt ---")
    print(prompt)
    print("\n--- Response ---")
    print(response)


if __name__ == "__main__":
    main()
