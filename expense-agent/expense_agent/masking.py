"""Identifier masking — applied at parse time, never at render time.

Masking here means every downstream stage (categorization, the LLM, the cache,
the rendered HTML) only ever sees already-masked text. There is no later point
in the pipeline where an unmasked value could leak.
"""

import re

_TAIL_KEEP = 4


def mask_tail(value: str, keep: int = _TAIL_KEEP) -> str:
    """Mask everything but the last `keep` characters."""
    value = str(value)
    if len(value) <= keep:
        return value
    return "X" * (len(value) - keep) + value[-keep:]


# UPI/IMPS reference numbers and similar — any bare run of 8+ digits.
_RE_LONG_DIGITS = re.compile(r"\b\d{8,}\b")
# Partially-masked account tokens the bank export already started, e.g. X601325.
_RE_X_PREFIXED = re.compile(r"\bX\d{5,}\b")
# ACH mandate / UMRN-style alphanumeric blobs (must contain a digit to avoid
# catching plain merchant names in caps, e.g. "FEDERALBANKLTD").
_RE_ALNUM_BLOB = re.compile(r"\b(?=[A-Z0-9]*\d)[A-Z0-9]{12,}\b")
# IFSC codes: 4 letters, a 0, then 6 alphanumerics.
_RE_IFSC = re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b")


def mask_narration(text: str) -> str:
    """Mask reference numbers / account tokens / IFSC inside a transaction narration.

    Counterparty names are deliberately left untouched — they are not in the
    masked identifier class (account number, customer ID, card number, IFSC),
    and a spending report without them is not useful.
    """
    text = _RE_LONG_DIGITS.sub(lambda m: mask_tail(m.group(0)), text)
    text = _RE_X_PREFIXED.sub(lambda m: mask_tail(m.group(0)), text)
    text = _RE_ALNUM_BLOB.sub(lambda m: mask_tail(m.group(0)), text)
    text = _RE_IFSC.sub(lambda m: mask_tail(m.group(0)), text)
    return text


def mask_account_number(account_no: str) -> str:
    return mask_tail(account_no)
