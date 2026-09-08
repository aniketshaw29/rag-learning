"""
Offline RAG Retrieval Demo
===========================

This script demonstrates the FULL retrieval concept WITHOUT needing
a Gemini API key. It uses a simple, self-contained text-similarity
method (TF-IDF + cosine similarity) so you can see how retrieval works
on day one, before you ever touch the embedding API.

The real pipeline swaps this simple embedder for Gemini's embeddings,
but the retrieval idea is identical: convert text to a vector,
compare with document vectors, return the closest matches.

Run:
    python tests/demo_retrieval.py
"""

import sys
from pathlib import Path
import math
import re
from collections import Counter

# Add src/ so we can reuse the load + chunk helpers
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from utils import load_documents, chunk_documents


# ──────────────────────────────────────────────────────────────────────
# A mini "embedding" using TF-IDF (no external model needed)
# ──────────────────────────────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    """Split text into lowercase word tokens."""
    return re.findall(r"[a-z0-9]+", text.lower())


def build_vocab(texts: list[str]) -> dict:
    """Create a word -> index map from all documents."""
    vocab = {}
    for text in texts:
        for token in tokenize(text):
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab


def tfidf_vector(text: str, vocab: dict, doc_freq: dict, num_docs: int) -> list[float]:
    """
    Convert text into a TF-IDF weight vector.

    TF-IDF gives higher weight to words that are important to THIS document
    and rare across the whole corpus — a decent lightweight stand-in for
    embeddings in a demo.
    """
    vector = [0.0] * len(vocab)
    counts = Counter(tokenize(text))
    total = sum(counts.values())

    for token, count in counts.items():
        if token not in vocab:
            continue
        idx = vocab[token]
        # TF: term frequency in this text
        tf = count / total if total else 0
        # IDF: inverse doc frequency (how rare/important the word is)
        df = doc_freq.get(token, 1)
        idf = math.log((num_docs + 1) / (df + 1)) + 1
        vector[idx] = tf * idf
    return vector


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """How similar two vectors are: 1.0 = identical, 0.0 = unrelated."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


# ──────────────────────────────────────────────────────────────────────
# Build the knowledge base vectors
# ──────────────────────────────────────────────────────────────────────

def index_chunks(chunks: list[dict]):
    """
    Build TF-IDF vectors for every chunk.
    Returns a lookup so we can search by semantic similarity.
    """
    texts = [c["text"] for c in chunks]

    # Vocabulary + document frequency (how many chunks contain each word)
    vocab = build_vocab(texts)
    doc_freq = Counter()
    for text in texts:
        for token in set(tokenize(text)):
            doc_freq[token] += 1

    num_docs = len(texts)

    # Build a vector for every chunk
    vectors = [tfidf_vector(t, vocab, doc_freq, num_docs) for t in texts]
    return vocab, vectors


def search(query: str, vectors: list[list[float]], chunks: list[dict],
           vocab: dict, doc_freq: Counter, n_results: int = 3) -> list[dict]:
    """
    Embed the query and return the closest chunks.
    This mirrors what `retrieve_context` does with real embeddings.
    """
    num_docs = len(chunks)
    q_vec = tfidf_vector(query, vocab, doc_freq, num_docs)

    scored = []
    for i, vec in enumerate(vectors):
        score = cosine_similarity(q_vec, vec)
        scored.append((score, chunks[i]))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [
        {"score": s, **c}
        for s, c in scored[:n_results]
    ]


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("OFFLINE RAG RETRIEVAL DEMO")
    print("(Uses TF-IDF instead of Gemini — no API key needed)")
    print("=" * 60)

    # Load + chunk the TechNova knowledge base
    docs = load_documents()
    chunks = chunk_documents(docs)
    print(f"\nIndexed {len(chunks)} chunks from {len(docs)} documents\n")

    # Build index
    vocab, vectors = index_chunks(chunks)

    # Recompute document frequency for the search function
    doc_freq = Counter()
    for text in [c["text"] for c in chunks]:
        for token in set(tokenize(text)):
            doc_freq[token] += 1

    # Ask questions
    questions = [
        "How many vacation days do engineers get?",
        "What is NovaCode Pricing?",
        "How do I handle a P1 incident?",
        "What technology does the Platform team use?",
    ]

    for question in questions:
        print(f"\n{'─' * 60}")
        print(f"Q: {question}")
        print("─" * 60)

        results = search(question, vectors, chunks, vocab, doc_freq, n_results=2)

        for i, r in enumerate(results, 1):
            preview = r["text"][:120].replace("\n", " ")
            print(f"  {i}. [score {r['score']:.3f}] {r['source']}: {preview}...")

    print("\n" + "=" * 60)
    print("This shows the RETRIEVAL step works. Replace the TF-IDF")
    print("'embeddings' with Gemini embeddings (src/03) for real")
    print("semantic search. The pipeline stays the same!")
    print("=" * 60)
    print("\nNote: the 'Platform team tech stack' query returned imperfect")
    print("results above. That's because TF-IDF matches KEYWORDS, not meaning.")
    print("Gemini embeddings understand that 'technology stack' ≈ 'tech")
    print("stack' ≈ 'languages and tools', so it finds the right chunk better.")
    print("This is exactly why real RAG uses deep embeddings!")
