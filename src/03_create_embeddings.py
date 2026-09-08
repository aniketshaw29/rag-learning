"""
Step 3: Creating Embeddings with Gemini
========================================

USECASE: TechNova Knowledge Base Q&A
We convert each chunk into a numerical vector (embedding) using
Gemini's embedding model. Similar meanings produce similar vectors,
which is how we find relevant chunks for a question.

Run:
    python src/03_create_embeddings.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
from utils import (
    get_gemini_client, load_documents, chunk_documents,
    get_embedding, get_embeddings_batch,
)


if __name__ == "__main__":
    print("=" * 60)
    print("STEP 3: Creating Embeddings")
    print("=" * 60)

    # Initialize Gemini client
    client = get_gemini_client()
    print("Gemini client initialized\n")

    # Load and chunk documents
    docs = load_documents()
    chunks = chunk_documents(docs)
    texts = [chunk["text"] for chunk in chunks]

    print(f"Creating embeddings for {len(chunks)} chunks...")
    embeddings = get_embeddings_batch(client, texts)
    print("Done!\n")

    # Show embedding details
    for i, (chunk, embedding) in enumerate(zip(chunks[:3], embeddings[:3])):
        print(f"Chunk {i + 1} (from {chunk['source']}):")
        print(f"  Text: {chunk['text'][:80].replace(chr(10), ' ')}...")
        print(f"  Embedding dimension: {len(embedding)}")
        print(f"  First 5 values: {[round(v, 4) for v in embedding[:5]]}")
        print()

    print(f"... ({len(embeddings) - 3} more embeddings created)\n")

    # ─── Bonus: demonstrate similarity ───────────────────────────────
    print("=" * 60)
    print("BONUS: How similarity search works")
    print("=" * 60)

    def cosine_similarity(a, b):
        """How similar are two vectors? 1.0 = identical, 0.0 = unrelated."""
        a, b = np.array(a), np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    # Test with a few TechNova-related queries
    test_queries = [
        "What is the vacation policy for engineers?",
        "What programming languages does NovaCode support?",
        "How do I respond to a P1 incident?",
    ]

    for query in test_queries:
        q_emb = get_embedding(client, query)
        scores = [(cosine_similarity(q_emb, emb), chunk)
                  for emb, chunk in zip(embeddings, chunks)]
        scores.sort(reverse=True)  # Highest similarity first

        print(f"\nQuery: '{query}'")
        print("Top 2 matches:")
        for score, chunk in scores[:2]:
            preview = chunk["text"][:80].replace("\n", " ")
            print(f"  [{score:.4f}] {chunk['source']}: {preview}...")
