---
name: qdrant
description: Guides the use of Qdrant vector database for storing, searching, and retrieving vector embeddings for AI workflows.
---

# Qdrant

## Instructions
1. Set up a Qdrant instance and configure collections for storing embeddings.
2. Convert data into vector embeddings using AI models.
3. Insert embeddings into Qdrant with metadata for context.
4. Query the vector database efficiently using similarity search.
5. Optimize indexing and collection parameters for performance.
6. Integrate Qdrant with backend services or AI pipelines.
7. Monitor database health and query performance.
8. Document collections, schema, and query strategies.

## Examples
- Creating a collection:
  ```python
  client.recreate_collection(
      collection_name="documents",
      vector_size=1536,
      distance="Cosine"
  )
  ```

- Inserting a vector:
  ```python
  client.upsert(
      collection_name="documents",
      points=[{"id":1,"vector":embedding,"payload":{"title":"Doc1"}}]
  )
  ```

- Searching for similar vectors:
  ```python
  results = client.search(
      collection_name="documents",
      query_vector=query_embedding,
      top=5
  )
  ```