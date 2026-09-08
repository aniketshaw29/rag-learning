"""
Step 6: Generating Answers with Gemini
========================================

USECASE: TechNova Knowledge Base Q&A
The final step! We take the retrieved chunks and pass them to Gemini
as context, then ask it to answer the employee's question.

The prompt tells Gemini to ONLY use the provided context — this
prevents hallucination and keeps answers grounded in real data.

Run:
    python src/06_generate_answer.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils import get_gemini_client, retrieve_context


# ──────────────────────────────────────────────────────────────────────
# Generation configuration
# ──────────────────────────────────────────────────────────────────────

MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """You are TechNova's internal knowledge assistant. Answer the
employee's question using ONLY the context provided below. If the context does
not contain enough information to answer, say "I don't have enough information
to answer that — please check with your manager or HR."

Do not make up information. Base your answer strictly on the context.
If relevant, cite the source document.

---
CONTEXT:
{context}
---
"""


def format_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a numbered context string."""
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(f"[{i}] (Source: {chunk['source']})\n{chunk['text']}")
    return "\n\n".join(parts)


def generate_answer(question: str, n_results: int = 3) -> dict:
    """
    Complete RAG generation:
      1. Retrieve relevant chunks
      2. Format as context
      3. Send to Gemini with grounded prompt
      4. Return answer + sources
    """
    client = get_gemini_client()

    # Step 1: Retrieve
    chunks = retrieve_context(question, n_results=n_results)
    context = format_context(chunks)

    # Step 2: Generate
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

    sources = list(set(c["source"] for c in chunks))
    return {
        "question": question,
        "answer": response.text,
        "sources": sources,
        "chunks_used": len(chunks),
    }


if __name__ == "__main__":
    print("=" * 60)
    print("STEP 6: Generating Answers (Full RAG)")
    print("=" * 60)

    # Ask real TechNova questions
    questions = [
        "How many vacation days do engineers get per year?",
        "What is NovaCode and how much does it cost?",
        "What do I do when a P1 incident is detected?",
        "What's the tech stack for the AI/ML team?",
        "How does the learning and development budget work?",
    ]

    for question in questions:
        print(f"\n{'═' * 60}")
        print(f"Q: {question}")
        print("═" * 60)

        result = generate_answer(question)

        print(f"\nA: {result['answer']}")
        print(f"\nSources: {', '.join(result['sources'])}")
        print(f"Chunks used: {result['chunks_used']}")
