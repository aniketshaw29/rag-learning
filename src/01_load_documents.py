"""
Step 1: Loading Documents
=========================

USECASE: TechNova Knowledge Base Q&A
We have markdown files containing company info — policies, product docs,
team structure, and incident playbooks. Our RAG system will let employees
ask natural language questions and get grounded answers.

This script loads all the training documents from the data/ folder
and shows what we're working with.

Run:
    python src/01_load_documents.py
"""

import sys
from pathlib import Path

# Add src/ to the path so we can import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils import load_documents, DATA_DIR


if __name__ == "__main__":
    print("=" * 60)
    print("STEP 1: Loading Documents")
    print("=" * 60)
    print(f"\nData directory: {DATA_DIR}\n")

    # Load all documents
    docs = load_documents()

    print(f"Found {len(docs)} document(s) in the knowledge base:\n")
    for i, doc in enumerate(docs, 1):
        print(f"  {i}. {doc.metadata['source']}")
        print(f"     Size: {doc.metadata['size_bytes']} bytes")
        print(f"     Content: {len(doc.content)} characters")
        # Show first 2 lines as preview
        preview = doc.content.split("\n")[:2]
        for line in preview:
            print(f"     > {line.strip()}")
        print()

    total_chars = sum(len(d.content) for d in docs)
    print(f"Total content: {total_chars:,} characters across {len(docs)} files")
    print("\nThese documents are our knowledge base — the source of truth")
    print("that the RAG system will search through to answer questions.")
