"""
Interactive Chat with the TechNova Knowledge Base
===================================================

A simple command-line interface to chat with your RAG system.
Run ingestion first (once), then ask questions interactively.

Usage:
    # First, build the knowledge base:
    python src/chat.py --ingest

    # Then ask questions:
    python src/chat.py "How much vacation do engineers get?"
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    get_gemini_client, load_documents, chunk_documents,
    get_collection,
)

MODEL = "gemini-2.5-flash"
N_RESULTS = 3

SYSTEM_PROMPT = """You are TechNova's internal knowledge assistant. Answer the
employee's question using ONLY the context below. If the context does not
contain enough information, say "I don't have enough information to answer that."

Do not make up information. Base your answer strictly on the context.

---
CONTEXT:
{context}
---
"""


def ingest(api_key: str):
    """Load, chunk, embed, and store all documents."""
    print("Building knowledge base...")
    docs = load_documents()
    chunks = chunk_documents(docs)
    collection = get_collection(api_key)

    # Fresh start
    try:
        collection.delete(ids=collection.get()["ids"])
    except Exception:
        pass

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]
    collection.add(ids=ids, documents=texts, metadatas=metadatas)
    print(f"Indexed {len(chunks)} chunks from {len(docs)} documents")
    print("Ready to answer questions!\n")


def ask(collection, client, question: str):
    """Retrieve + generate answer for a single question."""
    # Retrieve
    results = collection.query(query_texts=[question], n_results=N_RESULTS)
    chunks = [
        {"text": d, "source": m, "distance": dist}
        for d, m, dist in zip(
            results["documents"][0], results["metadatas"][0], results["distances"][0]
        )
    ]

    # Generate
    context = "\n\n".join(
        f"[{i}] (Source: {c['source']})\n{c['text']}" for i, c in enumerate(chunks, 1)
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
    return response.text, sorted(set(c["source"] for c in chunks))


def main():
    parser = argparse.ArgumentParser(description="Chat with the TechNova knowledge base")
    parser.add_argument("--ingest", action="store_true", help="Build the knowledge base first")
    parser.add_argument("--question", "-q", help="Ask a single question, then exit")
    args = parser.parse_args()

    client = get_gemini_client()
    collection = get_collection(client._api_key)

    if args.ingest:
        ingest(client._api_key)

    # Single question mode
    if args.question:
        answer, sources = ask(collection, client, args.question)
        print(f"\nQ: {args.question}\n")
        print(f"A: {answer}\n")
        print(f"Sources: {', '.join(sources)}")
        return

    # Interactive mode
    print("\nTechNova Knowledge Assistant — type 'quit' to exit\n")

    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if question.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        if not question:
            continue

        answer, sources = ask(collection, client, question)
        print(f"\nAssistant: {answer}")
        print(f"\n(Sources: {', '.join(sources)})")


if __name__ == "__main__":
    main()
