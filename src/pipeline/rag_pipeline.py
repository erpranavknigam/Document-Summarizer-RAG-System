class RAGPipeline:
    def __init__(self, retriever, prompt_builder, llm_client):
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client
        
    def run(self, query: str, mode: str = "answer", top_k: int = 3) -> str:
        if query.strip() == "":
            raise ValueError("Query must be provided")
        
        mode = mode.strip().lower()
        if mode not in ["answer", "summary"]:
            raise ValueError("Mode can only be answer or summary")
        
        try:
            retrieved = self.retriever.retrieve(query, top_k)
        except Exception as e:
            print(f"Error in retrieval: {e}")
            return f"Error during retrieval: {str(e)[:100]}..."
        
        if not retrieved["documents"] or not retrieved["documents"][0]:
            return "Not found in the document"
        
        chunks = []
        
        documents = retrieved["documents"][0]
        metadatas = retrieved["metadatas"][0]
        
        for i, text in enumerate(documents):
            meta = metadatas[i]
            chunks.append({
                "id": i + 1,
                "text": text,
                "source_file": meta["source_file"]
            })
            
        prompt = self.prompt_builder.build_prompt(
            chunks = chunks,
            mode = mode,
            query = query
        )
        
        response = self.llm_client.generate(prompt, max_tokens=512)
        
        return response