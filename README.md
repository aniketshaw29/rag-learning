# RAG Learning Project (with Gemini)

Learn how **Retrieval-Augmented Generation (RAG)** works from scratch by
building a real system in Python using **Google Gemini**.

## The Usecase: "Ask TechNova"

This project builds an internal **knowledge-base assistant** for a fictional
company, **TechNova Inc.** (a software company making AI developer tools).

Employees should be able to ask natural questions like:
- "How many vacation days do engineers get?"
- "What's the incident response process for a P2 issue?"
- "How much does NovaCode cost?"

...and get grounded answers pulled from the company's documents — instead of
asking them to search through long HR PDFs and internal wikis.

## How RAG Works (the 6 steps)

```
INDEXING (one-time)                    QUERYING (per question)
===================                    ========================
[Load docs] → [Chunk] → [Embed]        [Embed question] → [Search DB]
                        → [ChromaDB]          ↓
                                      [Relevant chunks] → [Gemini answers]
```

The project is split into 6 step scripts (plus a full pipeline) so you can
learn one concept at a time:

| Step | Script | What you learn |
|------|--------|----------------|
| 1 | `src/01_load_documents.py` | Reading files into "documents" |
| 2 | `src/02_chunk_documents.py` | Splitting text into searchable chunks |
| 3 | `src/03_create_embeddings.py` | Turning text into vectors with Gemini |
| 4 | `src/04_store_in_vectordb.py` | Storing vectors in ChromaDB |
| 5 | `src/05_retrieve_context.py` | Finding relevant chunks (Retrieval) |
| 6 | `src/06_generate_answer.py` | Gemini generating grounded answers |

There's also an **interactive Jupyter notebook** (`notebooks/rag_walkthrough.ipynb`)
that walks through every step with runnable cells, and an **offline demo**
(`tests/demo_retrieval.py`) that shows retrieval working **without an API key**
using a lightweight TF-IDF stand-in for embeddings.

## Quick Start

```bash
# 1. Create virtual env and install
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Add your Gemini key
cp .env.example .env   # then edit .env with your key

# 3. (Optional) See retrieval work without an API key
python tests/demo_retrieval.py

# 4. Run the full pipeline
python src/full_rag_pipeline.py

# Or run steps one at a time:
python src/01_load_documents.py
python src/02_chunk_documents.py
# ... on through 06

# 5. Chat interactively
python src/chat.py --ingest
python src/chat.py -q "How much vacation do engineers get?"

# 6. Or learn in the notebook
python -m ipykernel install --user --name rag-learning  # once
jupyter notebook                                         # open notebooks/
```

## Tech Stack

- **Gemini** (via `google-genai`) — embeddings + answer generation
- **ChromaDB** — free, local, open-source vector database
- **Python 3.10+**

## Documentation

Start with the `docs/` folder:

- `docs/01-what-is-rag.md` — What RAG is and why it matters
- `docs/02-how-rag-works.md` — The full pipeline, step by step
- `docs/03-setup.md` — Setup instructions
- `docs/04-glossary.md` — Key terms

## License

This project is for learning purposes. Sample data is fictional.
