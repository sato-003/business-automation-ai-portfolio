"""Public demonstration: plan names from invented metadata, without reading files."""

from dataclasses import dataclass
from datetime import date
import re
import unicodedata


@dataclass(frozen=True)
class Document:
    scanned_on: date
    category: str
    subject: str
    confidence: float


def safe_part(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "", value)
    value = re.sub(r"\s+", "_", value).strip(" ._")
    return value[:40] or "未設定"


def propose_name(document: Document, existing: set[str]) -> tuple[str, bool]:
    """Return a collision-free candidate and whether a person should review it."""
    review = document.confidence < 0.8 or not document.subject.strip()
    category = safe_part(document.category)
    subject = safe_part(document.subject) if document.subject.strip() else "件名不明"
    stem = f"{document.scanned_on.isoformat()}_{category}_{subject}"
    candidate = f"{stem}.pdf"
    suffix = 1
    while candidate in existing:
        candidate = f"{stem}_{suffix}.pdf"
        suffix += 1
    return candidate, review


if __name__ == "__main__":
    samples = [
        Document(date(2026, 11, 1), "議事録", "架空プロジェクトの打合せ", 0.96),
        Document(date(2026, 11, 1), "議事録", "架空プロジェクトの打合せ", 0.96),
        Document(date(2026, 11, 2), "案内", "", 0.55),
    ]
    existing: set[str] = set()
    for item in samples:
        name, needs_review = propose_name(item, existing)
        existing.add(name)
        print(f"{name}  {'要確認' if needs_review else '確認候補'}")
