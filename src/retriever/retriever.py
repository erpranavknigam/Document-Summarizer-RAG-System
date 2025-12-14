from typing import Dict

class Retriever:
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 3) -> Dict:
        if query.strip() == "":
            raise ValueError("Query cannot be empty")

        query_embedding = self.embedder.embed_query(query.strip())

        results = self.vector_store.query(query_embedding, top_k)
        return results
