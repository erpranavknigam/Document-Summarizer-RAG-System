import sys
import os

# Add project root to sys.path to allow running as script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ingest.file_router import ExtractorRouter
from src.preprocess.text_preprocessor import TextPreprocessor
from src.embeddings.embedder import Embedder
from src.vectorspace.vector_store import VectorStore

class Indexer:
    def __init__(self, data_dir="data/raw", model_path="all-MiniLM-L6-v2"):
        self.data_dir = data_dir
        self.extractor = ExtractorRouter()
        self.preprocessor = TextPreprocessor()
        self.embedder = Embedder(model_path)
        self.vector_store = VectorStore()

    def index_all(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Created data directory: {self.data_dir}")
            return

        files = os.listdir(self.data_dir)
        if not files:
            print("No files found to index.")
            return

        print(f"Found {len(files)} files. Starting indexing...")

        for filename in files:
            file_path = os.path.join(self.data_dir, filename)

            if not os.path.isfile(file_path):
                continue

            print(f"Processing {filename}...")
            try:
                extractor = self.extractor.get_extractor(file_path)
                text = extractor.extract(file_path)

                if not text.strip():
                    print(f"Warning: No text extracted from {filename}")
                    continue

                chunks = self.preprocessor.chunk_text(text, source_file=filename)
                embeddings = self.embedder.embed_chunks(chunks)
                self.vector_store.add_embeddings(chunks, embeddings)
                print(f"Indexed {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

        print("✅ Indexing completed.")

if __name__ == "__main__":
    indexer = Indexer()
    indexer.index_all()
