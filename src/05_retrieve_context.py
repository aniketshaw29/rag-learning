"""
Step 5: Retrieving Relevant Context
=====================================

USECASE: TechNova Knowledge Base Q&A
When an employee asks a question like "What's our incident response
process?", we search the vector database for the most relevant chunks
and return them as context.

This is the "R" in RAG — Retrieval.

Run:
    python src/05_retrieve_context.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils import retrieve_context


if __name__ == "__main__":
    print("=" * 60)
    print("STEP 5: Retrieving Relevant Context")
    print("=" * 60)

    # Test with TechNova-related questions
    queries = [
        "How many vacation days do engineers get?",
        "What tech stack does the Platform team use?",
        "What should I do when a P1 incident happens?",
        "How much does NovaCode Pro cost?",
        "Who leads the AI/ML team?",
    ]

    for query in queries:
        print(f"\n{'─' * 60}")
        print(f"Query: {query}")
        print("─" * 60)

        results = retrieve_context(query, n_results=2)

        for i, result in enumerate(results, 1):
            print(f"\n  Result {i} (distance: {result['distance']:.4f}):")
            print(f"  Source: {result['source']}")
            print(f"  Text: {result['text'][:150]}...")

    # Demo: filtering by source
    print(f"\n{'═' * 60}")
    print("Filtered search (HR policies only):")
    print("═" * 60)

    results = retrieve_context(
        "What is the learning budget?",
        n_results=2,
        source_filter="03_hr_policies.md",
    )

    for i, result in enumerate(results, 1):
        print(f"\n  Result {i}:")
        print(f"  Source: {result['source']}")
        print(f"  Text: {result['text'][:150]}...")
