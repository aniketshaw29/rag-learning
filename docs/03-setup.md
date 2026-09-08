# Setup Guide

Follow these steps to get the RAG project running on your machine.

## Prerequisites

- Python 3.10 or higher
- A Google Gemini API key (free tier available)

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

# Activate it
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
# Step 1: Load documents from the data/ folder
python src/01_load_documents.py

# Step 2: Split documents into chunks
python src/02_chunk_documents.py

# Step 3: Create embeddings with Gemini
python src/03_create_embeddings.py

# Step 4: Store embeddings in ChromaDB
python src/04_store_in_vectordb.py

# Step 5: Retrieve relevant chunks for a question
python src/05_retrieve_context.py

# Step 6: Generate an answer with Gemini
python src/06_generate_answer.py

# Or run the complete pipeline end-to-end
python src/full_rag_pipeline.py
```

## Project Structure

```
rag-learning/
├── docs/                          # Learning material (you are here)
│   ├── 01-what-is-rag.md
│   ├── 02-how-rag-works.md
│   ├── 03-setup.md
│   └── 04-glossary.md
├── src/                           # Python scripts (run these)
│   ├── 01_load_documents.py
│   ├── 02_chunk_documents.py
│   ├── 03_create_embeddings.py
│   ├── 04_store_in_vectordb.py
│   ├── 05_retrieve_context.py
│   ├── 06_generate_answer.py
│   └── full_rag_pipeline.py
├── data/                          # Sample documents to query
│   ├── python_basics.md
│   └── machine_learning_intro.md
├── .env.example                   # API key template
├── .gitignore
├── requirements.txt
└── README.md
```
