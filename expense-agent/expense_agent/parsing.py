"""Axis Bank CSV parsing.

Axis exports are three zones: a metadata preamble, the transaction block, and a
long tail of legal boilerplate + a legend. `pandas.read_csv()` cannot handle this
directly — the header row must be located dynamically, and the transaction block
must be sliced out by testing each row, not by a fixed row count.
"""

import csv
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from . import masking

_DATE_RE = re.compile(r"^\d{2}-\d{2}-\d{4}$")
_ACCOUNT_RE = re.compile(r"Account No\s*-\s*([0-9A-Za-z]+)")
_PERIOD_RE = re.compile(r"From\s*:\s*([\d-]+)\s*To\s*:\s*([\d-]+)")


@dataclass
class RawTransaction:
    date: str          # ISO yyyy-mm-dd
    day_label: str      # "25 Jul"
    month_label: str    # "Jul 2026"
    narration_masked: str
    debit: float
    credit: float
    balance: float


@dataclass
class ParsedStatement:
    account_masked: str
    period: str
    opening_balance: float
    closing_balance: float
    transactions: list = field(default_factory=list)


class StatementParseError(Exception):
    pass


def _find_header_row(rows: list[list[str]]) -> int:
    """Scan for the row containing both TRAN DATE and DR — the real header.

    Never hardcode a skiprows count; the preamble length varies by export.
    """
    for i, row in enumerate(rows):
        cells = [c.strip().upper() for c in row]
        if "TRAN DATE" in cells and any(c in ("DR", "DEBIT") for c in cells):
            return i
    raise StatementParseError("Could not locate the 'Tran Date' / 'DR' header row")


def _extract_preamble_meta(rows: list[list[str]], header_idx: int) -> tuple[str, str]:
    account_masked = "unknown"
    period = ""
    for row in rows[:header_idx]:
        line = ",".join(row)
        m = _ACCOUNT_RE.search(line)
        if m:
            account_masked = masking.mask_account_number(m.group(1))
        m = _PERIOD_RE.search(line)
        if m:
            period = f"{m.group(1)} to {m.group(2)}"
    return account_masked, period


def _parse_amount(cell: str) -> float:
    """Parse a rupee amount cell.

    The empty-amount cell in Axis exports is a single space `" "`, not `""` —
    naive `float()` raises on it, and a naive truthiness check (`if not x`) lets
    it slip past, since `" "` is truthy. Both must be handled explicitly here,
    once, so nothing downstream has to remember this.
    """
    cleaned = (cell or "").strip().replace(",", "")
    if not cleaned:
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _parse_date(cell: str) -> datetime:
    return datetime.strptime(cell.strip(), "%d-%m-%Y")


def parse_statement_csv(csv_path: str) -> ParsedStatement:
    path = Path(csv_path)
    if not path.exists():
        raise StatementParseError(f"CSV not found: {csv_path}")

    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))

    header_idx = _find_header_row(rows)
    header = [c.strip().upper() for c in rows[header_idx]]
    try:
        c_date = header.index("TRAN DATE")
        c_narr = header.index("PARTICULARS")
        c_dr = header.index("DR")
        c_cr = header.index("CR")
        c_bal = header.index("BAL")
    except ValueError as e:
        raise StatementParseError(f"Header row is missing an expected column: {e}")

    account_masked, period = _extract_preamble_meta(rows, header_idx)

    transactions: list[RawTransaction] = []
    for row in rows[header_idx + 1:]:
        if len(row) <= max(c_date, c_narr, c_dr, c_cr, c_bal):
            continue
        date_cell = row[c_date].strip()
        if not _DATE_RE.match(date_cell):
            # First row that isn't a dated transaction row marks the end of the
            # transaction block (legal boilerplate / legend follows).
            break

        debit = _parse_amount(row[c_dr])
        credit = _parse_amount(row[c_cr])
        balance = _parse_amount(row[c_bal])
        if debit == 0.0 and credit == 0.0:
            continue

        dt = _parse_date(date_cell)
        narration_masked = masking.mask_narration(row[c_narr].strip())

        transactions.append(RawTransaction(
            date=dt.strftime("%Y-%m-%d"),
            day_label=dt.strftime("%d %b"),
            month_label=dt.strftime("%b %Y"),
            narration_masked=narration_masked,
            debit=round(debit, 2),
            credit=round(credit, 2),
            balance=round(balance, 2),
        ))

    if not transactions:
        raise StatementParseError("No transaction rows found after the header")

    transactions.sort(key=lambda t: t.date)

    first = transactions[0]
    opening_balance = round(first.balance + first.debit - first.credit, 2)
    closing_balance = transactions[-1].balance

    return ParsedStatement(
        account_masked=account_masked,
        period=period,
        opening_balance=opening_balance,
        closing_balance=closing_balance,
        transactions=transactions,
    )
