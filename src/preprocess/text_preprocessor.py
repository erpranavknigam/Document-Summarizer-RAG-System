import re
from typing import List, Dict
import nltk

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class TextPreprocessor:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def clean_text(self, text: str) -> str:
        if not text or text.strip() == "":
            raise ValueError("Input text is empty")

        text = re.sub(r'\s+', ' ', text)
        text = text.replace("\n", " ").strip()

        return text

    def chunk_text(self, text: str, source_file: str = None) -> List[Dict]:
        text = self.clean_text(text)
        sentences = sent_tokenize(text)

        chunks = []
        current_chunk = []
        chunk_id = 1

        for sentence in sentences:
            sentence = sentence.strip()

            
            if sum(len(s) for s in current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk.append(sentence)
            else:
                chunks.append({
                    "id": f"{source_file}_chunk_{chunk_id}",
                    "text": " ".join(current_chunk),
                    "source_file": source_file
                })
                chunk_id += 1

                if self.overlap > 0 and len(current_chunk) > 0:
                    overlap_sentences = []
                    current_overlap_len = 0
                    for s in reversed(current_chunk):
                        if current_overlap_len + len(s) > self.overlap:
                            break
                        overlap_sentences.insert(0, s)
                        current_overlap_len += len(s)
                    current_chunk = overlap_sentences + [sentence]
                else:
                    current_chunk = [sentence]

        if current_chunk:
            chunks.append({
                "id": f"{source_file}_chunk_{chunk_id}",
                "text": " ".join(current_chunk),
                "source_file": source_file
            })

        return chunks


if __name__ == "__main__":
    sample_text = """
    This is a sample document. It has multiple sentences.
    We will use it to test our TextPreprocessor.
    Each sentence should be included in chunks correctly.
    """

    preprocessor = TextPreprocessor(chunk_size=50, overlap=1)
    chunks = preprocessor.chunk_text(sample_text, source_file="sample.pdf")

    for c in chunks:
        print(f"{c['id']} → {c['text']}\n")
