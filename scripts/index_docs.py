"""Index zalopay-integration-docs/ markdown files into AgentBase Memory for the search_docs tool.

Each file is split into chunks by heading (## or ###) so retrieval and
citations can point at a specific section, e.g.
[Nguồn: zalopay-integration-docs/faq/faq.md#cau-hoi-1]. Content before the
first heading is indexed as its own chunk citing just the file path (no anchor).

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
DOCS_DIR = ROOT / "zalopay-integration-docs"

MEMORY_ID = os.environ["MEMORY_ID"]
DOCS_MEMORY_STRATEGY_ID = os.environ["DOCS_MEMORY_STRATEGY_ID"]
DOCS_NAMESPACE = f"/strategies/{DOCS_MEMORY_STRATEGY_ID}/actors/shared"

HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")

# Most files start with a "Nguồn: https://docs.zalopay.vn/..." line pointing at the
# original docs.zalopay.vn page. That line lives in the pre-heading chunk, so on its
# own it's not retrievable alongside a specific section. Extract it once per file and
# attach it to every chunk so search_docs results always carry the original web URL.
SOURCE_URL_RE = re.compile(r"^Ngu[oồ]n:\s*(https://\S+)", re.MULTILINE)

# Sections that only contain doc-site navigation/meta links (prev/next page,
# "see also" links to other pages on docs.zalopay.vn) rather than integration
# content. Indexing them adds low-value chunks that can crowd out useful
# results in search_docs.
SKIP_HEADINGS = {"navigation", "navigation structure", "key navigation", "related resources"}


def slugify(heading: str) -> str:
    """Approximate GitHub-style heading anchors."""
    slug = heading.lower().strip()
    slug = re.sub(r"[^\w\- ]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def chunk_file(content: str, rel_path: Path) -> list[str]:
    """Split a markdown file into chunks, one per heading (## or ###)."""
    source_url_match = SOURCE_URL_RE.search(content)
    source_url = source_url_match.group(1) if source_url_match else None

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
        if heading is not None and heading.lower() in SKIP_HEADINGS:
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

        header = f"[Nguồn: {source}]"
        if source_url:
            header += f"\n[Trang tài liệu gốc: {source_url}]"
        chunks.append(f"{header}\n\n{text}")

    return chunks


# Number of records sent per insert call. The memory API embeds each record
# synchronously, so a single request with all ~200 chunks exceeds the
# client's default 30s HTTP timeout. Smaller batches keep each call fast.
BATCH_SIZE = 20


# Upper bound for listing existing records to purge. The memory API has no
# bulk-delete or upsert-by-key, so a full resync deletes everything in the
# namespace first to avoid unbounded duplicate growth across repeated runs.
LIST_LIMIT = 2000


def purge_namespace(client: MemoryClient) -> None:
    """Delete all existing records in DOCS_NAMESPACE before re-indexing."""
    existing = client.list_memory_records(id=MEMORY_ID, namespace=DOCS_NAMESPACE, limit=LIST_LIMIT)
    if not existing:
        return
    print(f"Deleting {len(existing)} existing records from {DOCS_NAMESPACE}")
    for record in existing:
        client.delete_memory_record(id=MEMORY_ID, memoryRecordId=record["id"])


def main() -> None:
    client = MemoryClient()

    records = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        rel_path = path.relative_to(ROOT)
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        records.extend(chunk_file(content, rel_path))

    purge_namespace(client)

    print(f"Indexing {len(records)} chunks into memory {MEMORY_ID} (namespace {DOCS_NAMESPACE})")
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i : i + BATCH_SIZE]
        print(f"  batch {i // BATCH_SIZE + 1}: records {i + 1}-{i + len(batch)}")
        client.insert_memory_records_directly(
            id=MEMORY_ID,
            namespace=DOCS_NAMESPACE,
            request=MemoryRecordInsertDirectlyRequest(memoryRecords=batch),
        )
    print("Done.")


if __name__ == "__main__":
    main()
