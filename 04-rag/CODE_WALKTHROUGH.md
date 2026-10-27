# RAG — Line-by-Line Code Walkthrough

## Keyword retrieval example

```python
docs = [
    {"id": "RUNBOOK-1", "text": "For timeout, check network path and server health."},
    {"id": "RUNBOOK-2", "text": "For null pointer, check variable initialization."},
]
query = "Jenkins connection timeout".lower()
matches = [doc for doc in docs if "timeout" in query and "timeout" in doc["text"].lower()]
print(matches[0]["id"] if matches else "No match")
```

- `docs` is a list of dictionaries; each dictionary stores a runbook identifier and its text.
- `id` identifies the source so a result can be traced back to a runbook.
- `query` stores the user's question in lowercase.
- The list comprehension loops over each `doc` in `docs`.
- The first condition checks whether the query contains the word `timeout`.
- The second condition checks whether the current document contains `timeout`.
- Matching documents are collected in a new list named `matches`.
- `matches[0]` retrieves the first match; `["id"]` extracts its identifier.
- The conditional expression after `print` uses the ID if a match exists, otherwise it prints `No match`.

Expected output: `RUNBOOK-1`.

## The examples.py scoring function
- `RUNBOOKS` stores example documents and their tags.
- `def retrieve(query: str) -> list[dict]:` declares the function and provides type hints.
- `query.lower().split()` makes a lowercase list of whitespace-separated words; `set(...)` removes duplicate words.
- For each document, tags are combined and converted to a set.
- `words & tags` computes the intersection: words present in both sets.
- `len(...)` counts the overlap and acts as a simple relevance score.
- Documents with a nonzero score are stored as `(score, doc)` pairs.
- `sort(..., reverse=True)` puts higher scores first.
- The final list comprehension returns only documents, dropping the scores.

This is a toy lexical matcher. It is not semantic vector search, has no embedding model, and does not generate an LLM answer. Real RAG adds document chunking, embeddings, a vector store, retrieval evaluation, prompt construction, and source-grounded generation.

## Practice
Try a query with no matching tags. Add a source title and version to each runbook and include those fields in the returned result.
