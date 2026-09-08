# How RAG Works - The Pipeline

A RAG system has two phases: **Indexing** (preparing your data) and
**Querying** (answering questions). Here is each step.

## Phase 1: Indexing (one-time setup)

This happens before any questions are asked. You prepare your knowledge base.

### Step 1: Load Documents

Read your source files (markdown, PDF, text, etc.) into memory. Each file
becomes a "document" object with its content and metadata (filename, path).

```
python_basics.md  -->  Document(content="...", metadata={"source": "python_basics.md"})
ml_intro.md       -->  Document(content="...", metadata={"source": "ml_intro.md"})
```

### Step 2: Chunk Documents

Documents are often too large to fit in an LLM prompt. We split them into
smaller pieces called **chunks**. Each chunk is a few hundred characters long,
with some overlap so context is not lost at boundaries.

```
"Python is a programming language created in 1991 by Guido van Rossum.
 It supports multiple paradigms..."

         -->  Chunk 1: "Python is a programming language created in 1991..."
         -->  Chunk 2: "1991 by Guido van Rossum. It supports multiple..."
         -->  Chunk 3: "multiple paradigms including OOP and functional..."
```

### Step 3: Create Embeddings

An **embedding** is a list of numbers (a vector) that captures the meaning of
text. Similar meanings produce similar vectors. We use Gemini's embedding model
for this.

```
"Python was created in 1991"  -->  [0.023, -0.156, 0.892, ...]  (3072 numbers)
"Guido van Rossum invented Python"  -->  [0.019, -0.148, 0.887, ...]  (similar!)
"The cat sat on the mat"  -->  [0.891, 0.234, -0.567, ...]  (very different)
```

### Step 4: Store in Vector Database

We store each chunk and its embedding in a **vector database** (ChromaDB in
our case). This lets us quickly find chunks similar to any query.

```
Vector DB:
  +-----------+---------------------+-------------------+
  | Chunk ID  | Text Content        | Embedding Vector  |
  +-----------+---------------------+-------------------+
  | 1         | "Python is a..."   | [0.023, -0.156..] |
  | 2         | "1991 by Guido..." | [0.019, -0.148..] |
  | 3         | "multiple..."      | [0.021, -0.151..] |
  +-----------+---------------------+-------------------+
```

## Phase 2: Querying (every time a question is asked)

### Step 5: Retrieve Relevant Chunks

When a user asks a question:

1. Convert the question to an embedding (same model as Step 3)
2. Search the vector database for the closest matching chunks
3. Return the top-k most relevant chunks

```
Question: "When was Python created?"
Query Embedding: [0.025, -0.152, 0.890, ...]

Vector DB finds:
  Chunk 1 (score: 0.95): "Python is a programming language created in 1991..."
  Chunk 2 (score: 0.82): "1991 by Guido van Rossum..."
```

### Step 6: Generate Answer

Pass the retrieved chunks and the question to Gemini as a prompt:

```
System: Answer using ONLY the context below. If unsure, say so.

Context:
- "Python is a programming language created in 1991..."
- "1991 by Guido van Rossum..."

User: When was Python created?
```

Gemini responds: "Python was created in 1991 by Guido van Rossum."

## Visual Summary

```
                    INDEXING (one-time)
                    ==================
  [Documents] --> [Chunk] --> [Embed] --> [Vector DB]
                                           stored

                    QUERYING (each question)
                    ========================
  [Question] --> [Embed] --> [Search DB] --> [Top Chunks]
                                                    |
                                                    v
                                        [Gemini generates answer]
```
