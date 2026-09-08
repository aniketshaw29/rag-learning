"""
Step 2: Chunking Documents
===========================

USECASE: TechNova Knowledge Base Q&A
The company documents are too large to pass entirely to an LLM.
We split them into smaller chunks so retrieval is precise and
each chunk fits comfortably in the context window.

Run:
    python src/02_chunk_documents.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils import load_documents, chunk_documents


# Chunking configuration — these values affect retrieval quality
CHUNK_SIZE = 500      # Max characters per chunk
CHUNK_OVERLAP = 100   # Characters to overlap between chunks


if __name__ == "__main__":
    print("=" * 60)
    print("STEP 2: Chunking Documents")
    print("=" * 60)

    # Load documents
    docs = load_documents()
    print(f"\nLoaded {len(docs)} document(s)")

    # Chunk them
    chunks = chunk_documents(docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    print(f"Split into {len(chunks)} chunks")
    print(f"Chunk size: {CHUNK_SIZE} chars, overlap: {CHUNK_OVERLAP} chars\n")

    # Show chunks grouped by source file
    sources = {}
    for chunk in chunks:
        src = chunk["source"]
        if src not in sources:
            sources[src] = []
        sources[src].append(chunk)

    for source, source_chunks in sources.items():
        print(f"--- {source} ({len(source_chunks)} chunks) ---")
        for i, chunk in enumerate(source_chunks[:3], 1):  # Show first 3
            preview = chunk["text"][:100].replace("\n", " ")
            print(f"  Chunk {i}: {preview}...")
        if len(source_chunks) > 3:
            print(f"  ... and {len(source_chunks) - 3} more chunks")
        print()

    # Show why chunking matters
    print("=" * 60)
    print("Why chunking matters:")
    print("-" * 60)
    print("Each chunk becomes one searchable unit in the vector database.")
    print("Smaller chunks = more precise retrieval.")
    print("Overlap ensures context is not lost at boundaries.")
    print(f"\nExample: Asking 'What is the PTO policy for engineers?' will")
    print(f"retrieve only the HR policies chunks, not the entire document.")
