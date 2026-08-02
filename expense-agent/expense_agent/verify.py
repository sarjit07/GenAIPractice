"""Grep-style checks run on the rendered HTML before it is allowed to reach the
final output path. This is a content check, not a visual one — opening the file
in a browser (light + dark) is still the real check for layout, per the README.
"""

import re

_RE_LONG_DIGITS = re.compile(r"(?<!\w)\d{8,}(?!\w)")
_RE_IFSC = re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b")
_RE_EXTERNAL_REF = re.compile(
    r'(?:src|href)\s*=\s*["\'](https?:)?//(?!localhost|127\.0\.0\.1)[^"\']+["\']',
    re.IGNORECASE,
)


def verify_html(html: str, raw_account_number: str | None = None) -> tuple[bool, list[str]]:
    findings: list[str] = []

    long_digit_hits = _RE_LONG_DIGITS.findall(html)
    if long_digit_hits:
        findings.append(f"{len(long_digit_hits)} unmasked run(s) of 8+ digits found")

    ifsc_hits = _RE_IFSC.findall(html)
    if ifsc_hits:
        findings.append(f"{len(ifsc_hits)} unmasked IFSC-shaped token(s) found")

    external_hits = _RE_EXTERNAL_REF.findall(html)
    if external_hits:
        findings.append(f"{len(external_hits)} external src/href reference(s) found — report must be self-contained")

    if raw_account_number and raw_account_number in html:
        findings.append("the raw (unmasked) account number literally appears in the output")

    return (len(findings) == 0), findings
