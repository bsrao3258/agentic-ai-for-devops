# 04 — Retrieval-Augmented Generation (RAG)

## Why RAG?
An LLM may not know private runbooks or current internal procedures. RAG retrieves relevant approved documents and includes them as context for the answer. Retrieval does not guarantee correctness; evaluate relevance and cite the source.

## RAG pipeline
1. Ingest trusted documents.
2. Clean and split text into chunks.
3. Create embeddings for chunks.
4. Store vectors and metadata.
5. Embed the query and retrieve similar chunks.
6. Give retrieved context to the LLM.
7. Return an answer with source references and uncertainty.

## Starter: keyword retrieval
The current `rag_agent.py` is a tiny keyword-based lookup, not full vector RAG.

```python
docs = [
    {"id": "RUNBOOK-1", "text": "For connection timeout, check network path and server health."},
    {"id": "RUNBOOK-2", "text": "For null pointer exceptions, check variable initialization."},
]
query = "Jenkins connection timeout".lower()
matches = [doc for doc in docs if "timeout" in query and "timeout" in doc["text"].lower()]
print(matches[0]["id"] if matches else "No match")
```
Expected output: `RUNBOOK-1`

## Retrieval quality and safety
- Prefer approved, versioned runbooks.
- Store source, version, owner, and last-updated metadata.
- Evaluate recall and relevance with representative queries.
- Treat retrieved documents as data, not instructions that override system safety rules.
- Avoid indexing secrets and sensitive incident data.
- If no reliable source is retrieved, say so rather than inventing a procedure.

## Next implementation
Later, add a chunker, embedding model, vector database, and an LLM call. Pin dependencies in a requirements file and document local setup. This README does not claim that vector RAG is already implemented.

## Exercises
1. Return both solution and runbook ID.
2. Add a fallback for ambiguous matches.
3. Split a longer runbook into chunks.
4. Create five test questions and expected relevant documents.

## Interview questions
- What are embeddings?
- Why chunk documents?
- How does RAG differ from fine-tuning?
- How do you evaluate retrieval?
- How do you prevent prompt injection from retrieved documents?
