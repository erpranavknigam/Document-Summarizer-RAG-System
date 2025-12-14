import numpy as np
from typing import List, Dict
import chromadb


class VectorStore:
    def __init__(self, persist_directory: str = "vector_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)

        try:
            self.collection = self.client.get_or_create_collection(
                name="document_chunks",
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Error getting collection: {e}")
            # If there's a dimension mismatch or other error, delete and recreate
            try:
                self.client.delete_collection("document_chunks")
                self.collection = self.client.create_collection(
                    name="document_chunks",
                    metadata={"hnsw:space": "cosine"}
                )
            except Exception as e2:
                 print(f"Error recreating collection: {e2}")
                 raise e2

    def add_embeddings(self, chunks: List[Dict], embeddings: np.ndarray) -> bool:
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings count must match")

        ids = [str(chunk["id"]) for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]

        metadatas=[{"source_file": chunk["source_file"]} for chunk in chunks]

        if isinstance(embeddings, np.ndarray):
            embeddings_list = embeddings.tolist()
        else:
            embeddings_list = embeddings

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings_list
        )

        return True

    def query(self, query_embedding: list, top_k: int = 3):
        results = self.collection.query(
            query_embeddings=[query_embedding],  # already list
            n_results=top_k
        )

        return results
