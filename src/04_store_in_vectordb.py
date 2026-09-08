"""
Step 4: Storing in ChromaDB
============================

USECASE: TechNova Knowledge Base Q&A
We store all chunk embeddings in ChromaDB — a local, free vector database.
This lets us quickly find the most relevant chunks for any question.

ChromaDB runs in-process (no server needed) and saves data to disk,
so we don't have to re-embed every time we restart.

Run:
    python src/04_store_in_vectordb.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    get_gemini_client, load_documents, chunk_documents,
    get_collection, DB_DIR,
)


if __name__ == "__main__":
    print("=" * 60)
    print("STEP 4: Storing in ChromaDB")
    print("=" * 60)

    # Initialize
    client = get_gemini_client()
    api_key = client._api_key

    # Load and chunk documents
    docs = load_documents()
    chunks = chunk_documents(docs)
    print(f"\nLoaded {len(chunks)} chunks from {len(docs)} document(s)")

    # Connect to ChromaDB and get our collection
    collection = get_collection(api_key)

    # Prepare data for ChromaDB
    # ChromaDB needs: unique IDs, document text, and metadata
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [
        {"source": chunk["source"], "chunk_index": chunk["chunk_index"]}
        for chunk in chunks
    ]

    # Clear any existing data (fresh start)
    try:
        collection.delete(ids=collection.get()["ids"])
        print("Cleared previous data from collection")
    except Exception:
        pass  # Collection might be empty on first run

    # Add all chunks to ChromaDB
    # ChromaDB will automatically embed the text using our Gemini function
    collection.add(ids=ids, documents=texts, metadatas=metadatas)

    print(f"Stored {collection.count()} chunks in ChromaDB")
    print(f"Database location: {DB_DIR}\n")

    # Test with a query
    print("=" * 60)
    print("Test query:")
    print("=" * 60)

    query = "How many vacation days do engineers get?"
    results = collection.query(query_texts=[query], n_results=2)

    print(f"\nQuery: '{query}'")
    print("Top 2 results:\n")

    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    )):
        print(f"  Result {i + 1} (distance: {dist:.4f}):")
        print(f"  Source: {meta['source']}")
        print(f"  Text: {doc[:150]}...\n")

    print("The vector database is now ready for retrieval!")
