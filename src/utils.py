"""
Shared utilities for the RAG learning project.

This module contains common classes and functions used across all steps.
Each step script imports from here instead of duplicating code.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
import chromadb


# ──────────────────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_DIR = PROJECT_ROOT / "chroma_db"


# ──────────────────────────────────────────────────────────────────────
# Gemini client
# ──────────────────────────────────────────────────────────────────────

def get_gemini_client() -> genai.Client:
    """
    Create and return a Gemini API client.
    Loads the API key from the .env file in the project root.
    """
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. "
            "Copy .env.example to .env and add your Gemini API key."
        )
    return genai.Client(api_key=api_key)


# ──────────────────────────────────────────────────────────────────────
# Document class
# ──────────────────────────────────────────────────────────────────────

class Document:
    """
    A container for a document's content and metadata.

    Attributes:
        content:  The raw text read from the file.
        metadata: A dictionary with info like source filename and path.
    """

    def __init__(self, content: str, metadata: dict):
        self.content = content
        self.metadata = metadata

    def __repr__(self):
        preview = self.content[:80].replace("\n", " ")
        source = self.metadata.get("source", "unknown")
        return f"Document(source='{source}', preview='{preview}...')"


# ──────────────────────────────────────────────────────────────────────
# Loading documents
# ──────────────────────────────────────────────────────────────────────

def load_documents(directory: Path = DATA_DIR) -> list[Document]:
    """
    Load all .md and .txt files from a directory.

    Each file becomes a Document with its content and metadata
    (filename, path, size).
    """
    documents = []
    for file_path in sorted(directory.iterdir()):
        if file_path.suffix in (".md", ".txt"):
            content = file_path.read_text(encoding="utf-8")
            metadata = {
                "source": file_path.name,
                "path": str(file_path),
                "size_bytes": file_path.stat().st_size,
            }
            documents.append(Document(content=content, metadata=metadata))
    return documents


# ──────────────────────────────────────────────────────────────────────
# Chunking
# ──────────────────────────────────────────────────────────────────────

def split_text(text: str, chunk_size: int = 500,
               chunk_overlap: int = 100) -> list[str]:
    """
    Split text into overlapping chunks.

    Strategy:
      1. Split by double newlines (paragraphs)
      2. If a paragraph is too long, split by single newlines
      3. Merge small pieces until we approach chunk_size
      4. Add overlap from the end of the previous chunk
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
            current_chunk = (current_chunk + "\n\n" + paragraph).strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            if len(paragraph) > chunk_size:
                lines = paragraph.split("\n")
                current_chunk = ""
                for line in lines:
                    if len(current_chunk) + len(line) + 1 <= chunk_size:
                        current_chunk = (current_chunk + "\n" + line).strip()
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = line
            else:
                if chunks and chunk_overlap > 0:
                    overlap_text = chunks[-1][-chunk_overlap:]
                    current_chunk = overlap_text + "\n\n" + paragraph
                else:
                    current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def chunk_documents(documents: list[Document],
                    chunk_size: int = 500,
                    chunk_overlap: int = 100) -> list[dict]:
    """
    Chunk a list of documents. Each chunk tracks its source file.
    """
    all_chunks = []
    for doc in documents:
        text_chunks = split_text(doc.content, chunk_size, chunk_overlap)
        for idx, chunk_text in enumerate(text_chunks):
            all_chunks.append({
                "text": chunk_text,
                "source": doc.metadata["source"],
                "chunk_index": idx,
            })
    return all_chunks


# ──────────────────────────────────────────────────────────────────────
# Embeddings
# ──────────────────────────────────────────────────────────────────────

EMBEDDING_MODEL = "gemini-embedding-2"


def get_embedding(client: genai.Client, text: str) -> list[float]:
    """Convert a single piece of text into an embedding vector."""
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )
    return result.embeddings[0].values


def get_embeddings_batch(client: genai.Client,
                         texts: list[str]) -> list[list[float]]:
    """Embed multiple texts at once."""
    results = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
    )
    return [emb.values for emb in results.embeddings]


# ──────────────────────────────────────────────────────────────────────
# ChromaDB embedding function wrapper
# ──────────────────────────────────────────────────────────────────────

class GeminiEmbeddingFunction(chromadb.EmbeddingFunction):
    """
    Wraps Gemini's embedding API so ChromaDB can use it for
    embedding queries and documents.
    """

    def __init__(self, api_key: str, model: str = EMBEDDING_MODEL):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def __call__(self, input: list[str]) -> list[list[float]]:
        results = self.client.models.embed_content(
            model=self.model,
            contents=input,
        )
        return [emb.values for emb in results.embeddings]


# ──────────────────────────────────────────────────────────────────────
# Vector database helpers
# ──────────────────────────────────────────────────────────────────────

def get_vector_db():
    """Connect to the ChromaDB persistent database."""
    return chromadb.PersistentClient(path=str(DB_DIR))


def get_collection(api_key: str):
    """Get (or create) the main document collection."""
    db = get_vector_db()
    embedding_fn = GeminiEmbeddingFunction(api_key=api_key)
    return db.get_or_create_collection(
        name="technova_knowledge",
        embedding_function=embedding_fn,
    )


# ──────────────────────────────────────────────────────────────────────
# Retrieval
# ──────────────────────────────────────────────────────────────────────

def retrieve_context(query: str, n_results: int = 3,
                     source_filter: str = None) -> list[dict]:
    """
    Retrieve the most relevant chunks for a given question.

    Args:
        query:          The user's question (e.g., "What is the PTO policy?")
        n_results:      How many top chunks to return
        source_filter:  Optional — only search in a specific source file

    Returns:
        List of dicts with 'text', 'source', and 'distance'
    """
    client = get_gemini_client()
    collection = get_collection(client._api_key)

    query_kwargs = {"query_texts": [query], "n_results": n_results}
    if source_filter:
        query_kwargs["where"] = {"source": source_filter}

    results = collection.query(**query_kwargs)

    retrieved = []
    for doc, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved.append({
            "text": doc,
            "source": meta["source"],
            "distance": distance,
        })
    return retrieved
