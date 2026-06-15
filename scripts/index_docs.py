"""Index docs/ markdown files into AgentBase Memory for the search_docs tool.

Each file is split into chunks by heading (## or ###) so retrieval and
citations can point at a specific section, e.g. [Nguồn: faq/faq.md#cau-hoi-1].
Content before the first heading is indexed as its own chunk citing just the
file path (no anchor).

Usage:
    python3 scripts/index_docs.py
"""

import os
import re
from pathlib import Path

from dotenv import load_dotenv
from greennode_agentbase.memory import MemoryClient
from greennode_agentbase.memory.models import MemoryRecordInsertDirectlyRequest

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"

MEMORY_ID = os.environ["MEMORY_ID"]
DOCS_MEMORY_STRATEGY_ID = os.environ["DOCS_MEMORY_STRATEGY_ID"]
DOCS_NAMESPACE = f"/strategies/{DOCS_MEMORY_STRATEGY_ID}/actors/shared"

HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")


def slugify(heading: str) -> str:
    """Approximate GitHub-style heading anchors."""
    slug = heading.lower().strip()
    slug = re.sub(r"[^\w\- ]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def chunk_file(content: str, rel_path: Path) -> list[str]:
    """Split a markdown file into chunks, one per heading (## or ###)."""
    lines = content.splitlines()

    sections: list[tuple[str | None, list[str]]] = []
    current_heading: str | None = None
    current_lines: list[str] = []
    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            sections.append((current_heading, current_lines))
            current_heading = match.group(2).strip()
            current_lines = [line]
        else:
            current_lines.append(line)
    sections.append((current_heading, current_lines))

    seen_slugs: dict[str, int] = {}
    chunks = []
    for heading, section_lines in sections:
        text = "\n".join(section_lines).strip()
        if not text:
            continue

        if heading is None:
            source = str(rel_path)
        else:
            slug = slugify(heading)
            count = seen_slugs.get(slug, 0)
            seen_slugs[slug] = count + 1
            if count:
                slug = f"{slug}-{count}"
            source = f"{rel_path}#{slug}"

        chunks.append(f"[Nguồn: {source}]\n\n{text}")

    return chunks


def main() -> None:
    client = MemoryClient()

    records = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        rel_path = path.relative_to(ROOT)
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        records.extend(chunk_file(content, rel_path))

    print(f"Indexing {len(records)} chunks into memory {MEMORY_ID} (namespace {DOCS_NAMESPACE})")
    client.insert_memory_records_directly(
        id=MEMORY_ID,
        namespace=DOCS_NAMESPACE,
        request=MemoryRecordInsertDirectlyRequest(memoryRecords=records),
    )
    print("Done.")


if __name__ == "__main__":
    main()
