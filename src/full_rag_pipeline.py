"""
Full RAG Pipeline — TechNova Knowledge Base Q&A
===============================================

This script runs the ENTIRE RAG pipeline end-to-end:
  1. Load documents from data/
  2. Chunk them into small pieces
  3. Create embeddings with Gemini
  4. Store in ChromaDB (vector database)
  5. Retrieve relevant chunks for a question
  6. Generate an answer, grounded in the retrieved context

Run:
    python src/full_rag_pipeline.py

You'll see the output of each stage, then it asks a set of questions
from the TechNova knowledge base.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    get_gemini_client, load_documents, chunk_documents,
    get_collection, DB_DIR,
)

# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

MODEL = "gemini-2.5-flash"       # Gemini model for generating answers
CHUNK_SIZE = 500                  # Max characters per chunk
CHUNK_OVERLAP = 100               # Overlap between chunks
N_RESULTS = 3                     # How many chunks to retrieve per query

SYSTEM_PROMPT = """You are TechNova's internal knowledge assistant. Answer the
employee's question using ONLY the context below. If the context does not
contain enough information, say "I don't have enough information to answer that."

Do not make up information. Base your answer strictly on the context.

---
CONTEXT:
{context}
---
"""


# ──────────────────────────────────────────────────────────────────────
# Pipeline stages
# ──────────────────────────────────────────────────────────────────────

def stage_indexing(api_key: str):
    """Stage 1-4: Load, chunk, embed, and store documents."""
    print("\n" + "=" * 60)
    print("STAGE 1: Indexing (load → chunk → embed → store)")
    print("=" * 60)

    # 1. Load
    docs = load_documents()
    print(f"  1. Loaded {len(docs)} document(s)")

    # 2. Chunk
    chunks = chunk_documents(docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    print(f"  2. Split into {len(chunks)} chunks")

    # 3-4. Store (ChromaDB embeds automatically via our Gemini function)
    collection = get_collection(api_key)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]

    # Fresh start
    try:
        collection.delete(ids=collection.get()["ids"])
    except Exception:
        pass

    collection.add(ids=ids, documents=texts, metadatas=metadatas)
    print(f"  4. Embedded & stored {collection.count()} chunks in ChromaDB")
    return collection


def retrieve(collection, question: str, n_results: int = N_RESULTS):
    """Stage 5: Find the most relevant chunks."""
    results = collection.query(query_texts=[question], n_results=n_results)
    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        chunks.append({"text": doc, "source": meta["source"], "distance": dist})
    return chunks


def generate(client, question: str, chunks: list[dict]):
    """Stage 6: Generate a grounded answer with Gemini."""
    context = "\n\n".join(
        f"[{i}] (Source: {c['source']})\n{c['text']}"
        for i, c in enumerate(chunks, 1)
    )
    system_msg = SYSTEM_PROMPT.format(context=context)
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            {"role": "user", "parts": [
                {"text": system_msg},
                {"text": f"\n\nEmployee question: {question}"},
            ]},
        ],
    )
    return response.text


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("TechNova Knowledge Base — Full RAG Pipeline")
    print("=" * 60)

    # Initialize Gemini
    client = get_gemini_client()
    print("Gemini client initialized")
    print(f"Database will be stored at: {DB_DIR}")

    # Run indexing
    collection = stage_indexing(client._api_key)

    print("\n" + "=" * 60)
    print("STAGE 2: Querying (retrieve → generate)")
    print("=" * 60)

    # Ask questions that a TechNova employee might ask
    questions = [
        "What are the engineering salary bands?",
        "What is the incident response process for a P2 issue?",
        "How much does NovaCode cost per month?",
        "Who leads the NovaTest team?",
        "What is TechNova's revenue for 2024?",
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{'─' * 60}")
        print(f"QUESTION {i}: {question}")
        print("─" * 60)

        # Retrieve relevant context
        chunks = retrieve(collection, question)
        print(f"  Retrieved {len(chunks)} relevant chunks")

        # Generate grounded answer
        answer = generate(client, question, chunks)
        print(f"  Answer: {answer}")
        print(f"  Sources: {', '.join(sorted(set(c['source'] for c in chunks)))}")

    print("\n" + "=" * 60)
    print("Pipeline complete!")
    print("=" * 60)
