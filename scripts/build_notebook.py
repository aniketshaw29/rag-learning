"""
Builds the RAG learning Jupyter notebook programmatically.
Run: python scripts/build_notebook.py

This keeps the notebook source in a plain Python script so it's
easy to read and version-control, rather than a giant JSON file.
"""

from pathlib import Path

import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata["kernelspec"] = {
    "name": "python3",
    "display_name": "Python 3 (rag-learning)",
    "language": "python",
}
nb.metadata["language_info"] = {"name": "python"}

cells = []

# ── Title ──────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""\
# Build RAG with Gemini — Interactive Walkthrough

**Usecase: "Ask TechNova"** — an internal knowledge-base assistant for a
fictional software company. Employees ask questions and get grounded answers
from company documents.

This notebook walks through RAG step by step. Work through each section,
run the cells, and watch the pipeline come together.

> **Note:** Steps 1–2 run offline. Steps 3–6 need your Gemini API key set
> in `.env`. To build the full knowledge base, run cells in order once
> through, then experiment freely.
"""))

# ── Setup ──────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""\
## 0. Setup

Run this cell once. It adds the project `src/` to the path and imports
our shared helpers. Everything we've built lives in `src/utils.py`.
"""))

cells.append(nbf.v4.new_code_cell("""\
import sys
from pathlib import Path

# Add the project src/ folder to the import path.
# Works whether the notebook is opened from notebooks/ or the project root.
PROJECT_ROOT = Path.cwd() / ".." if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str((PROJECT_ROOT / "src").resolve()))

from utils import (
    get_gemini_client,
    load_documents,
    chunk_documents,
    split_text,
    get_embedding,
    get_embeddings_batch,
    get_collection,
    retrieve_context,
    DATA_DIR,
)

print("Imports OK")
print(f"Data directory: {DATA_DIR}")
"""))

# ── Step 1 ─────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""\
## Step 1: Load Documents

The knowledge base is a set of markdown files in `data/`.
Loading turns each file into a **Document** with content + metadata.
"""))

cells.append(nbf.v4.new_code_cell("""\
docs = load_documents()
print(f"Loaded {len(docs)} documents:\\n")
for i, doc in enumerate(docs, 1):
    print(f"  {i}. {doc.metadata['source']}  ({len(doc.content)} chars)")
"""))

cells.append(nbf.v4.new_markdown_cell("""\
Each document has `content` (the text) and `metadata` (filename, path, size).
Let's peek at one.
"""))

cells.append(nbf.v4.new_code_cell("""\
doc = docs[2]  # the HR policies file
print("Source:", doc.metadata["source"])
print("Metadata:", doc.metadata)
print("\\nFirst 400 chars:\\n")
print(doc.content[:400])
"""))

# ── Step 2 ─────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""\
## Step 2: Chunking

Documents are too big to pass entirely to an LLM. We split them into smaller
**chunks** so retrieval is precise. We keep a small overlap so context isn't
lost at the boundaries.
"""))

cells.append(nbf.v4.new_code_cell("""\
chunks = chunk_documents(docs)
print(f"Split into {len(chunks)} chunks\\n")

# Show the first few chunks from the HR policies file
for i, c in enumerate([c for c in chunks if c["source"] == "03_hr_policies.md"][:3], 1):
    print(f"--- Chunk {i} (len {len(c['text'])}) ---")
    print(c["text"][:120].replace("\\n", " "))
    print()
"""))

cells.append(nbf.v4.new_code_cell("""\
# Experiment: see how chunk size changes the result
small = chunk_documents(docs, chunk_size=200, chunk_overlap=50)
large = chunk_documents(docs, chunk_size=1000, chunk_overlap=200)

print(f"chunk_size=200 -> {len(small)} chunks")
print(f"chunk_size=500 -> {len(chunks)} chunks")
print(f"chunk_size=1000 -> {len(large)} chunks")
print("\\nSmaller chunks = more, smaller pieces. Bigger chunks = fewer, larger pieces.")
print("There's a tradeoff between precision and context!")
"""))

# ── Step 3 ─────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""\
## Step 3: Embeddings with Gemini

An **embedding** is a vector of numbers that captures text meaning.
Similar meanings -> similar vectors. We use Gemini's embedding model.

> You need your API key in `.env` for this step onward.
"""))

cells.append(nbf.v4.new_code_cell("""\
client = get_gemini_client()

# Embed a single phrase
embedding = get_embedding(client, "How many vacation days do engineers get?")
print(f"Embedding dimension: {len(embedding)}")
print(f"First 5 values: {[round(v,4) for v in embedding[:5]]}")
"""))

cells.append(nbf.v4.new_code_cell("""\
# Visualize embedding similarity
import numpy as np

def cosine_sim(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

texts = [
    "How many vacation days do engineers get?",
    "What is the PTO policy for engineering staff?",
    "NovaCode supports Python and TypeScript",
]
embs = get_embeddings_batch(client, texts)

print("Similarity between phrases:")
for i in range(len(texts)):
    for j in range(i+1, len(texts)):
        print(f"  [{cosine_sim(embs[i], embs[j]):.3f}] {texts[i][:35]}... vs {texts[j][:35]}...")
"""))

cells.append(nbf.v4.new_markdown_cell("""\
Notice the two *vacation/PTO* sentences score high similarity — they mean the
same thing even though the words differ. That's the power of semantic search.
"""))

# ── Step 4 ─────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""\
## Step 4: Store in ChromaDB

We store all chunk embeddings in **ChromaDB** — a free, local vector database.
This lets us search by meaning very fast.
"""))

cells.append(nbf.v4.new_code_cell("""\
# Load, chunk, and store the whole knowledge base
docs = load_documents()
chunks = chunk_documents(docs)

collection = get_collection(client._api_key)

# Fresh start each time we re-run indexing
try:
    collection.delete(ids=collection.get()["ids"])
except Exception:
    pass

ids = [f"chunk_{i}" for i in range(len(chunks))]
texts = [c["text"] for c in chunks]
metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]

collection.add(ids=ids, documents=texts, metadatas=metadatas)
print(f"Stored {collection.count()} chunks in ChromaDB")
"""))

# ── Step 5 ─────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""\
## Step 5: Retrieval

To answer a question, we embed it and ask ChromaDB for the closest chunks.
This is the **R** in RAG.
"""))

cells.append(nbf.v4.new_code_cell("""\
results = retrieve_context("How do I respond to a P1 incident?", n_results=2)

for i, r in enumerate(results, 1):
    print(f"Result {i} (distance {r['distance']:.4f}) from {r['source']}:")
    print(f"  {r['text'][:160].replace(chr(10),' ')}...\\n")
"""))

cells.append(nbf.v4.new_markdown_cell("""\
Try your own question below. Notice how it correctly pulls from the
relevant document — this is semantic retrieval, not keyword search.
"""))

cells.append(nbf.v4.new_code_cell("""\
question = "What are the engineering salary bands?"
for r in retrieve_context(question, n_results=2):
    print(f"[{r['source']}] {r['text'][:140].replace(chr(10),' ')}...\\n")
"""))

# ── Step 6 ─────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""\
## Step 6: Generation (Full RAG)

Finally, we pass the retrieved chunks to Gemini as context, and it answers
*grounded* in our documents — reducing hallucination.
"""))

cells.append(nbf.v4.new_code_cell("""\
MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = \"\"\"You are TechNova's internal knowledge assistant. Answer the
employee's question using ONLY the context below. If the context does not
contain enough information, say "I don't have enough information to answer that."

Do not make up information. Base your answer strictly on the context.

---
CONTEXT:
{context}
---
\"\"\"

def rag_answer(question, n_results=3):
    chunks = retrieve_context(question, n_results=n_results)
    context = "\\n\\n".join(
        f"[{i}] (Source: {c['source']})\\n{c['text']}"
        for i, c in enumerate(chunks, 1)
    )
    response = client.models.generate_content(
        model=MODEL,
        contents=[{"role": "user", "parts": [
            {"text": SYSTEM_PROMPT.format(context=context)},
            {"text": f"\\n\\nEmployee question: {question}"},
        ]}],
    )
    return response.text, sorted(set(c["source"] for c in chunks))
"""))

cells.append(nbf.v4.new_code_cell("""\
answer, sources = rag_answer("How much does NovaCode cost per month?")
print("Q: How much does NovaCode cost per month?\\n")
print("A:", answer)
print("\\nSources:", sources)
"""))

# ── Experiment ─────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""\
## Playground

Ask anything about TechNova. This uses the full RAG pipeline:
retrieve the relevant chunks, then generate a grounded answer.
"""))

cells.append(nbf.v4.new_code_cell("""\
question = "What is the remote work policy?"   # <-- change this
answer, sources = rag_answer(question)
print(f"Q: {question}\\n")
print(f"A: {answer}\\n")
print(f"Sources: {sources}")
"""))

cells.append(nbf.v4.new_markdown_cell("""\
## What You Learned

1. **Load** documents into `Document` objects
2. **Chunk** them for precise, prompt-friendly retrieval
3. **Embed** text into vectors with Gemini
4. **Store** vectors in ChromaDB
5. **Retrieve** relevant chunks by semantic similarity
6. **Generate** grounded answers with a context-injected prompt

That's RAG! Now try adding your own `.md` files to `data/` and re-run the
indexing cell — the system will answer questions about them too.
"""))

nb.cells = cells

out = Path(__file__).parent.parent / "notebooks" / "rag_walkthrough.ipynb"
out.parent.mkdir(exist_ok=True)
nbf.write(nb, str(out))
print(f"Wrote {out}")
