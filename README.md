# Document Summarizer & RAG System

A powerful Retrieval Augmented Generation (RAG) application designed to ingest documents, store their embeddings, and allow users to query or summarize them using various Large Language Models (LLMs).

## Features

*   **Retrieval Augmented Generation (RAG):** Combines semantic search with LLM generation to provide accurate answers based on your documents.
*   **Flexible LLM Support:**
    *   **Local:** Run completely offline using GGUF models (e.g., Mistral 7B) via `llama.cpp`.
    *   **Cloud:** Seamlessly switch to OpenAI (GPT-4o-mini) or Google Gemini (Gemini 2.5 Flash) by simply adding API keys.
*   **Flexible Embeddings:**
    *   **Local:** Uses `all-MiniLM-L6-v2` via `sentence-transformers` for fast, offline embeddings.
    *   **Cloud:** Supports OpenAI (`text-embedding-3-small`) and Google Gemini (`embedding-001`) embeddings.
*   **Vector Database:** Utilizes **ChromaDB** for efficient storage and retrieval of document vectors.
*   **Interactive CLI:** Easy-to-use command-line interface for asking questions and generating summaries.

## Prerequisites

*   Python 3.10 or higher
*   (Optional) C++ Compiler (Visual Studio Build Tools on Windows, Xcode on macOS, gcc on Linux) for building `llama-cpp-python` if using local models.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd document-summarizer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.lock
    ```

4.  **(Optional) Setup Local Model:**
    *   Create a `models` directory.
    *   Download a GGUF model (e.g., [Mistral-7B-Instruct-v0.2-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF)) and place it in `models/`.
    *   Update `MODEL_PATH` in `main.py` if necessary.

5. **File Placements**
    *   Create a `data` directory.
    *   Create a `raw` directory inside `data`.
    *   Put your documents in `data/raw`.
    *   Now execute `python src/indexing/indexing.py` to index your documents.
    
## Configuration

Create a `.env` file in the root directory to configure API keys. The system automatically detects available keys and switches providers (Cloud > Local).

```env
# Optional: For OpenAI LLM & Embeddings
OPENAI_API_KEY=sk-...

# Optional: For Google Gemini LLM & Embeddings
GEMINI_API_KEY=AIza...
```

## Usage

1.  **Run the application:**
    ```bash
    python main.py
    ```

2.  **Interact:**
    *   **Query:** Type your question when prompted.
    *   **Mode:** Choose between `answer` (specific answer) or `summary` (summarization).
    *   **Exit:** Type `exit` to quit.

## Project Structure

*   `src/`: Core application source code.
    *   `indexing/`: Handles indexing of documents.
    *   `embeddings/`: Handles text embedding generation (Local/OpenAI/Gemini).
    *    `ingest/`: Handles ingestion of documents.
    *   `llm/`: LLM client wrappers and fallback logic.
    *   `vectorspace/`: ChromaDB interaction for storing/retrieving vectors.
    *   `retriever/`: Logic for finding relevant document chunks.
    *   `pipeline/`: Orchestrates the RAG process.
    *   `preprocess/`: Handles preprocessing of documents.
    *   `summarizer/`: Handles summarization of documents.
*   `models/`: Directory for storing local GGUF models.
*   `vector_db/`: Persistent storage for ChromaDB.
*   `main.py`: Entry point for the application.
*   `data/`: Directory for storing documents.
    *   `raw/`: Directory for storing raw documents.
    *   `processed/`: Directory for storing processed documents.

## Troubleshooting

*   **`llama-cpp-python` installation issues:** Ensure you have the correct build tools installed for your OS. You may need to install the pre-built wheel for your specific platform if compilation fails.
*   **API Errors:** Check your `.env` file and ensure your API keys are valid and have quota available.
