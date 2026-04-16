from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag.vectorstore import DEFAULT_COLLECTIONS, initialize_collections


def main() -> None:
    initialize_collections()
    print("ChromaDB setup complete.")
    print("Collections initialized:")
    for name in DEFAULT_COLLECTIONS:
        print(f"- {name}")


if __name__ == "__main__":
    main()
