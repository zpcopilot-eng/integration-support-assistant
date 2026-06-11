"""Index docs/ markdown files into AgentBase Memory for the search_docs tool.

Usage:
    python3 scripts/index_docs.py
"""

import os
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


def main() -> None:
    client = MemoryClient()

    records = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        rel_path = path.relative_to(ROOT)
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        records.append(f"[Nguồn: {rel_path}]\n\n{content}")

    print(f"Indexing {len(records)} documents into memory {MEMORY_ID} (namespace {DOCS_NAMESPACE})")
    client.insert_memory_records_directly(
        id=MEMORY_ID,
        namespace=DOCS_NAMESPACE,
        request=MemoryRecordInsertDirectlyRequest(memoryRecords=records),
    )
    print("Done.")


if __name__ == "__main__":
    main()
