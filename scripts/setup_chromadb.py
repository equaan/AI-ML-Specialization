from __future__ import annotations

from backend.rag.vectorstore import DEFAULT_COLLECTIONS, initialize_collections


def main() -> None:
    initialize_collections()
    print("ChromaDB setup complete.")
    print("Collections initialized:")
    for name in DEFAULT_COLLECTIONS:
        print(f"- {name}")


if __name__ == "__main__":
    main()
