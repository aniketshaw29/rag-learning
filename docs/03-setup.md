# Setup Guide

Follow these steps to get the RAG project running on your machine.

## Prerequisites

- Python 3.10 or higher
- A Google Gemini API key (free tier available)

## What We're Building

This project teaches RAG by building a real usecase:
**a "Ask TechNova" knowledge-base assistant** that lets employees ask
natural-language questions about company policies, products, and teams.

The training documents are in `data/` (company overview, HR policies,
engineering teams, NovaCode product, incident response). Your RAG system
will retrieve the relevant info and answer grounded questions about them.

## 1. Get a Gemini API Key

1. Go to https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

## 2. Create a Virtual Environment

```bash
# Navigate to the project
cd rag-learning

# Create virtual environment
python3 -m venv venv

# Activate it (every time you open a new terminal)
# macOS / Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Set Up Your API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and paste your API key
# GEMINI_API_KEY=your_actual_key_here
```

## 5. Run the Scripts (in order)

Each script teaches one step of the RAG pipeline. Run them in order:

```bash
# Step 1: Load the TechNova documents
python src/01_load_documents.py

# Step 2: Split into chunks
python src/02_chunk_documents.py

# Step 3: Create embeddings with Gemini
python src/03_create_embeddings.py

# Step 4: Store in ChromaDB vector database
python src/04_store_in_vectordb.py

# Step 5: Retrieve relevant chunks for questions
python src/05_retrieve_context.py

# Step 6: Generate grounded answers with Gemini
python src/06_generate_answer.py
```

Or run the complete pipeline in one script:

```bash
python src/full_rag_pipeline.py
```

Or chat interactively:

```bash
# Build the knowledge base once:
python src/chat.py --ingest

# Then ask questions:
python src/chat.py -q "How much vacation do engineers get?"
python src/chat.py  # interactive mode
```

## Vector Database Choice

We use **ChromaDB** — it's free, open-source, and the standard choice for
learning/prototyping:

- **Runs in-process** — no server to install or configure
- **Persists to disk** — embeddings survive restarts
- **Fast similarity search** — uses cosine distance under the hood
- **Easy to swap** later for production DBs (Pinecone, Weaviate, pgvector)

No separate installation needed (it's pip-installed via requirements.txt).

## Project Structure

```
rag-learning/
├── docs/                          # Learning material (start here)
│   ├── 01-what-is-rag.md
│   ├── 02-how-rag-works.md
│   ├── 03-setup.md
│   └── 04-glossary.md
├── data/                          # TechNova training documents (the knowledge base)
│   ├── 01_company_overview.md
│   ├── 02_engineering_teams.md
│   ├── 03_hr_policies.md
│   ├── 04_novacode_product.md
│   └── 05_incident_response.md
├── src/                           # Python scripts (run these in order)
│   ├── utils.py                   # Shared helpers (loading, chunking, ChromaDB)
│   ├── 01_load_documents.py
│   ├── 02_chunk_documents.py
│   ├── 03_create_embeddings.py
│   ├── 04_store_in_vectordb.py
│   ├── 05_retrieve_context.py
│   ├── 06_generate_answer.py
│   ├── chat.py                    # Interactive ask-your-questions mode
│   └── full_rag_pipeline.py       # Everything in one script
├── .env.example                   # API key template
├── .gitignore
├── requirements.txt
└── README.md
```

## Sample Questions to Try

Try asking your RAG assistant these:

- "How many vacation days do engineers get per year?"
- "What does NovaCode cost and what features does it include?"
- "What's the tech stack for the Platform team?"
- "How do I respond to a P2 incident?"
- "Who is the VP of Engineering?"
- "What are the engineering salary bands?"
