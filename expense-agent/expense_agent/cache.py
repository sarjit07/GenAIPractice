"""Merchant-fragment -> category cache.

This is what keeps local-LLM call volume near zero after the first run or two:
once a merchant fragment has been classified, every future statement reuses the
result instead of hitting the model again.
"""

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


def normalize(fragment: str) -> str:
    return re.sub(r"\s+", " ", fragment.strip().upper())


@dataclass
class CachedClassification:
    category: str
    confidence: str
    reason: str
    source: str  # "llm" | "rule" | "manual" — "manual" is a hard override, see rules.apply_manual_override


class MerchantCache:
    def __init__(self, path: str):
        self.path = Path(path)
        self._data: dict[str, dict] = {}
        self._dirty = False
        if self.path.exists():
            try:
                self._data = json.loads(self.path.read_text())
            except json.JSONDecodeError:
                self._data = {}

    @staticmethod
    def _build(entry: dict) -> CachedClassification | None:
        # This file is meant to be hand-editable (manual corrections), so a
        # missing/extra key shouldn't crash the pipeline — degrade gracefully
        # rather than raise on a typo'd or partially-edited entry.
        try:
            return CachedClassification(
                category=entry["category"],
                confidence=entry.get("confidence", "high"),
                reason=entry.get("reason", ""),
                source=entry.get("source", "rule"),
            )
        except KeyError:
            return None

    def get(self, fragment: str) -> CachedClassification | None:
        entry = self._data.get(normalize(fragment))
        return self._build(entry) if entry else None

    def set(self, fragment: str, result: CachedClassification) -> None:
        self._data[normalize(fragment)] = asdict(result)
        self._dirty = True

    def remove(self, fragment: str) -> bool:
        """Delete a cache entry. Returns True if something was actually removed."""
        key = normalize(fragment)
        if key in self._data:
            del self._data[key]
            self._dirty = True
            return True
        return False

    def entries(self, source: str | None = None) -> dict[str, CachedClassification]:
        """All entries, keyed by normalized fragment; optionally filtered by source."""
        out = {}
        for key, entry in self._data.items():
            built = self._build(entry)
            if built and (source is None or built.source == source):
                out[key] = built
        return out

    def save(self) -> None:
        if not self._dirty:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2, sort_keys=True))
        self._dirty = False

    def __len__(self) -> int:
        return len(self._data)
