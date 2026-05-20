---
name: chroma
description: Self-hosted open-source embedding database for semantic search, RAG, and document retrieval — store embeddings and metadata, perform vector and full-text search, filter by metadata
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks to store document embeddings for semantic search
  - User wants to build a RAG (retrieval-augmented generation) system
  - User needs a local vector database with metadata filtering
  - User asks about persistent storage for embeddings
  - User wants to query documents by similarity or metadata filters
related_skills:
  - whisper
  - searxng-search
---

# Chroma — Open-Source Embedding Database

## Description

Chroma is an open-source embedding database for building AI applications with memory. It stores document embeddings alongside metadata, supports vector similarity search, full-text search, and rich metadata filtering. It runs entirely locally with an in-process client or as a server, scaling from notebook prototypes to production deployments. Apache 2.0 license.

This skill covers local inference only — no cloud API keys required. Default embeddings use the local `sentence-transformers` library (model: `all-MiniLM-L6-v2`).

## Prerequisites

- Python 3.8+
- `pip install chromadb` (includes sentence-transformers for default embeddings)
- Optional: Sentence Transformers downloads ~80 MB model on first use

## Steps

### 1. Install and create a collection

```bash
pip install chromadb
```

```python
import chromadb

# In-memory client (data lost on process exit)
client = chromadb.Client()

# Persistent client (data saved to disk)
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get a collection
collection = client.create_collection(name="my_collection")
# or: collection = client.get_or_create_collection("my_collection")
```

### 2. Add documents with metadata

```python
collection.add(
    documents=["This is document 1", "This is document 2"],
    metadatas=[
        {"source": "web", "category": "tutorial"},
        {"source": "pdf", "category": "report", "page": 5}
    ],
    ids=["id1", "id2"]
)
```

### 3. Query by similarity

```python
# Basic similarity search
results = collection.query(
    query_texts=["machine learning tutorial"],
    n_results=5
)

print(results["documents"])    # Matching documents
print(results["metadatas"])   # Metadata for each
print(results["distances"])   # Similarity scores
print(results["ids"])         # Document IDs
```

### 4. Filter by metadata

```python
# Exact match
results = collection.query(
    query_texts=["Python programming"],
    where={"source": "web"}
)

# Comparison operators: $gt, $gte, $lt, $lte, $ne
results = collection.query(
    query_texts=["advanced topics"],
    where={"page": {"$gte": 10}}
)

# Logical operators: $and, $or
results = collection.query(
    query_texts=["query"],
    where={
        "$and": [
            {"category": "tutorial"},
            {"difficulty": {"$lte": 3}}
        ]
    }
)
```

### 5. Update and delete documents

```python
# Update content and metadata
collection.update(
    ids=["id1"],
    documents=["Updated content"],
    metadatas=[{"source": "updated"}]
)

# Delete by IDs or filter
collection.delete(ids=["id1", "id2"])
collection.delete(where={"source": "outdated"})
```

### 6. Custom embedding function (local model)

```python
from chromadb import Documents, EmbeddingFunction, Embeddings

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Your local embedding logic here
        # e.g., use sentence-transformers, or any local model
        import sentence_transformers
        model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
        return model.encode(input).tolist()

my_ef = MyEmbeddingFunction()
collection = client.create_collection(
    name="custom_docs",
    embedding_function=my_ef
)
```

### 7. Run as a server (production)

```bash
# Start Chroma server
chroma run --path ./chroma_db --port 8000
```

```python
import chromadb
from chromadb.config import Settings

client = chromadb.HttpClient(
    host="localhost",
    port=8000,
    settings=Settings(anonymized_telemetry=False)
)

# Use identically to in-process client
collection = client.get_or_create_collection("my_docs")
```

### 8. Performance tips

```python
# Batch operations — add multiple documents at once
collection.add(
    documents=[f"Document {i}" for i in range(100)],
    ids=[f"id_{i}" for i in range(100)]
)

# Use persistent client for data survival across restarts
client = chromadb.PersistentClient(path="./chroma_db")

# Regular backups — copy the chroma_db directory
# cp -r ./chroma_db ./chroma_db_backup
```

## Pitfalls

1. **Default in-memory client loses data** — Always use `PersistentClient(path="./chroma_db")` for data that needs to survive process restart. The default `Client()` is ephemeral.
2. **Embedding model download on first use** — The default `all-MiniLM-L6-v2` model (~80 MB) downloads on first use. If running in an air-gapped environment, pre-download it or use a custom embedding function with a locally available model.
3. **IDs must be unique per collection** — Calling `add()` with a duplicate ID raises an error. Use `upsert()` instead if you want to overwrite existing documents.
4. **Metadata values must be simple types** — Only `str`, `int`, `float`, and `bool` are supported in metadata. Nested objects, lists, or arrays will cause errors at insert time.
5. **Collection size can grow unexpectedly** — Monitor collection count with `collection.count()`. Large collections may need server mode for better resource management.

## Verification

1. **Client connects**: Run `python3 -c "import chromadb; client = chromadb.Client(); print(len(client.list_collections()))"` and confirm it prints `0` (no collections yet).
2. **Add and query works**: Run the add + query example from Steps 2-3 and confirm results contain the added document with a distance score.
3. **Persistent storage works**: Create a `PersistentClient`, add a document, restart Python, reconnect with the same path, and verify the collection and document still exist.