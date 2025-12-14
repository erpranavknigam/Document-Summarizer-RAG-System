from dotenv import load_dotenv
load_dotenv()
from src.retriever.retriever import Retriever
from src.summarizer.prompt_builder import PromptBuilder
from src.llm.llm_client import LLMClient
from src.vectorspace.vector_store import VectorStore
from src.embeddings.embedder import Embedder
from src.pipeline.rag_pipeline import RAGPipeline


MODEL_PATH = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

embedder = Embedder(EMBEDDING_MODEL)
vector_store = VectorStore()
retriever = Retriever(embedder, vector_store)
prompt_builder = PromptBuilder()
llm_client = LLMClient(MODEL_PATH, n_ctx=2048, n_threads=8)

rag = RAGPipeline(retriever, prompt_builder, llm_client)

while True:
    query = input("\nAsk a question (or 'exit'): ")
    if query.lower() == "exit":
        break

    mode = input("Mode (answer/summary): ").strip().lower()
    print("\n--- RESPONSE ---\n")
    print(rag.run(query, mode=mode))
