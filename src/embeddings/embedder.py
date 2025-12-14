import os
import logging
from typing import List, Dict
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import google.generativeai as genai
    from google.generativeai import embeddings
except ImportError:
    genai = None
    embeddings = None


class Embedder:
    def __init__(
        self,
        model_path: str = "all-MiniLM-L6-v2",
        openai_model: str = "text-embedding-3-small",
        gemini_model: str = "models/embedding-001",
    ):
        self.local_model = SentenceTransformer(model_path)

        self.openai_client = None
        self.openai_model = openai_model

        self.gemini_enabled = False
        self.gemini_model = gemini_model

        if OpenAI and os.getenv("OPENAI_API_KEY"):
            self.openai_client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            logging.info("Embeddings: OpenAI enabled")

        elif genai and embeddings and os.getenv("GEMINI_API_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.gemini_enabled = True
            logging.info("Embeddings: Gemini enabled")

        else:
            logging.info("Embeddings: Local MiniLM")

    def _embed_texts(self, texts: List[str]) -> List[List[float]]:
        if self.openai_client:
            try:
                response = self.openai_client.embeddings.create(
                    model=self.openai_model,
                    input=texts,
                )
                return [d.embedding for d in response.data]
            except Exception as e:
                logging.warning(f"OpenAI failed → fallback: {e}")

        if self.gemini_enabled:
            try:
                return [
                    embeddings.embed_content(
                        model=self.gemini_model,
                        content=text,
                        task_type="retrieval_document",
                    )["embedding"]
                    for text in texts
                ]
            except Exception as e:
                logging.warning(f"Gemini failed → fallback: {e}")

        return self.local_model.encode(texts).tolist()


    def embed_chunks(self, chunks: List[Dict]):
        texts = [chunk["text"] for chunk in chunks]
        return self._embed_texts(texts)
    def __init__(
        self,
        model_path: str = "all-MiniLM-L6-v2",
        openai_model: str = "text-embedding-3-small",
        gemini_model: str = "models/embedding-001",
    ):
        self.local_model = SentenceTransformer(model_path)

        self.openai_client = None
        self.openai_model = openai_model

        self.gemini_enabled = False
        self.gemini_model = gemini_model

        if OpenAI and os.getenv("OPENAI_API_KEY"):
            self.openai_client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            logging.info("Embeddings: OpenAI enabled")

        elif genai and embeddings and os.getenv("GEMINI_API_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.gemini_enabled = True
            logging.info("Embeddings: Gemini enabled")

        else:
            logging.info("Embeddings: Local MiniLM")

    def _embed_texts(self, texts: List[str]) -> List[List[float]]:
        if self.openai_client:
            try:
                response = self.openai_client.embeddings.create(
                    model=self.openai_model,
                    input=texts,
                )
                return [d.embedding for d in response.data]
            except Exception as e:
                logging.warning(f"OpenAI failed → fallback: {e}")

        if self.gemini_enabled:
            try:
                return [
                    embeddings.embed_content(
                        model=self.gemini_model,
                        content=text,
                        task_type="retrieval_document",
                    )["embedding"]
                    for text in texts
                ]
            except Exception as e:
                logging.warning(f"Gemini failed → fallback: {e}")

        return self.local_model.encode(texts).tolist()


    def embed_chunks(self, chunks: List[Dict]):
        texts = [chunk["text"] for chunk in chunks]
        return self._embed_texts(texts)

    def embed_query(self, query: str):
        return self._embed_texts([query])[0]
