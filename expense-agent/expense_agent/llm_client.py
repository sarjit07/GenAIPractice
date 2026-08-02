"""The one place this pipeline calls the LLM.

Everything else in the graph only ever calls `classify_merchant()` — the rest of
the codebase never touches LangChain/OpenAI types directly.

Grammar-constrained decoding guarantees the *shape* of the response, not its
correctness — so the response is still validated against the category/
confidence enums before being trusted, and any failure (network, timeout,
malformed response, out-of-enum value) degrades to a deterministic
low-confidence Uncategorized result rather than raising into the graph. A
silent crash here should never take down report generation.

Structured output is requested via the standard OpenAI `response_format:
{"type": "json_schema", ...}` field, not vLLM's older `guided_json` /
`extra_body` mechanism. That was the first thing tried here, and on the vLLM
build this was developed against (0.25.1 + the vllm-metal Apple Silicon
plugin) it was silently a no-op — a `guided_json` payload with an enum of
made-up nonsense values had zero effect on the output, confirmed by testing
directly against the server with curl. `response_format` with a JSON Schema,
by contrast, correctly constrained the same test to the nonsense enum and
included every `required` field. Since `response_format` is a first-class
OpenAI API field (not a vendor extra), both LangChain's `ChatOpenAI` and the
raw `openai` client pass it through natively — no `extra_body` needed either.
If you're on a different vLLM version and see `guided_json` actually work,
that's a fine thing to add back as a secondary attempt, but don't remove this
path without re-testing with curl first, the way this bug was found.

We still deliberately do NOT use LangChain's `.with_structured_output()` —
that helper compiles to tool/function-calling on many models, a different
mechanism from a self-hosted server's JSON Schema constrained decoding, and
not guaranteed to be what actually reaches the wire.
"""

import json
import logging
from dataclasses import dataclass

from . import config

logger = logging.getLogger(__name__)

_RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "expense_classification",
        "schema": config.CLASSIFY_SCHEMA,
        "strict": True,
    },
}


@dataclass
class ClassificationResult:
    category: str
    confidence: str
    reason: str


def classify_merchant(
    fragment: str,
    candidate_hint: str | None = None,
    base_url: str | None = None,
    model: str | None = None,
    timeout: float = 15.0,
) -> ClassificationResult:
    base_url = base_url or config.DEFAULT_VLLM_BASE_URL
    model = model or config.DEFAULT_VLLM_MODEL
    messages = _build_messages(fragment, candidate_hint)

    try:
        return _classify_via_langchain(messages, base_url, model, timeout)
    except Exception as e:
        logger.warning(
            "LangChain structured-output path failed (%s); falling back to the raw openai client", e
        )
        try:
            return _classify_via_openai(messages, base_url, model, timeout)
        except Exception as e2:
            logger.warning(
                "vLLM classification failed entirely (%s); falling back to Uncategorized/low", e2
            )
            return ClassificationResult(
                "Uncategorized", "low", f"LLM call failed, needs manual review: {e2}"
            )


def _build_messages(fragment: str, candidate_hint: str | None) -> list[dict]:
    user = fragment
    if candidate_hint:
        user += f"\n(a keyword match weakly suggested \"{candidate_hint}\" — confirm or override)"
    return [
        {"role": "system", "content": config.CLASSIFY_SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]


def _truncate_at_word(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(".,;: ") + "…"


def _parse_response(text: str) -> ClassificationResult:
    data = json.loads(text)
    category = data["category"]
    confidence = data["confidence"]
    reason = _truncate_at_word(str(data.get("reason", "")), 140)
    if category not in config.LLM_CATEGORIES:
        raise ValueError(f"model returned an out-of-enum category: {category!r}")
    if confidence not in config.CONFIDENCE_LEVELS:
        raise ValueError(f"model returned an out-of-enum confidence: {confidence!r}")
    return ClassificationResult(category, confidence, reason)


def _classify_via_langchain(messages, base_url, model, timeout) -> ClassificationResult:
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        base_url=base_url, api_key="not-needed", model=model,
        timeout=timeout, temperature=0,
    )
    bound = llm.bind(response_format=_RESPONSE_FORMAT)
    response = bound.invoke(messages)
    content = response.content if isinstance(response.content, str) else str(response.content)
    return _parse_response(content)


def _classify_via_openai(messages, base_url, model, timeout) -> ClassificationResult:
    from openai import OpenAI

    client = OpenAI(base_url=base_url, api_key="not-needed", timeout=timeout)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        response_format=_RESPONSE_FORMAT,
    )
    return _parse_response(response.choices[0].message.content)
