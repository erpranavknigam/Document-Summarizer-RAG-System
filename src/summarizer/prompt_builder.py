from typing import List, Dict, Optional

class PromptBuilder:
    def __init__(self):
        pass
    
    def build_prompt(self, chunks: List[Dict], mode: str, query: Optional[str] = None) -> str:
        system_prompt = """
                        You are a helpful AI assistant.

                        You MUST answer using ONLY the information provided in the document context below.
                        You MUST NOT use any external knowledge, assumptions, or prior information.

                        If the answer to the question is not explicitly found in the provided context,
                        you MUST respond with exactly:
                        "Not found in the document."

                        You MUST strictly follow the output format instructions.
                        Do NOT add explanations, notes, or extra commentary beyond what is requested.
                        """
        
        context_block = "--- DOCUMENT CONTEXT START ---"
        chunk_list = []
        for chunk in chunks:
            chunk_id = chunk.get("id")
            source_file = chunk.get("source_file") or "unknown"
            text = chunk.get("text") or ""
            chunk_list.append(f"### CHUNK {chunk_id}\nSource: {source_file}\n{text.strip() if text else ''}\n---")
            
        joined_chunks = "\n".join(chunk_list)
        
        context_block += "\n" + joined_chunks
        
        context_block += "\n" + "--- DOCUMENT CONTEXT END ---" 

        
        task_instructions = ""
        
        mode = mode.lower().strip()
        
        if mode not in ("answer", "summary"):
            raise ValueError("Mode must be either 'answer' or 'summary'")
        
        if mode == "answer":
            task_instructions = """
                You MUST answer the user query directly using ONLY the provided context.
                Do NOT hallucinate or add information from outside the context.
                If the answer is not found, respond exactly: "Not found in the document."
                Provide the answer in a concise, single paragraph that meets the user’s needs.
            """
        else:
            task_instructions = """
                You MUST answer in bullet points.
                Each bullet point MUST NOT exceed 3 lines.
                Cover key ideas only; do NOT repeat information.
                Use ONLY the provided context; do NOT add external information.
                If relevant information is not found, respond exactly: "Not found in the document."
            """
        
        final_prompt = system_prompt + "\n" + context_block + "\n" + f"Mode: {mode}\n" + f"Query: {query}\n" + task_instructions
        return final_prompt.strip()
    
    
if __name__ == "__main__":
    chunks = [
        {"id": 1, "text": "This is the first chunk of text from the document.", "source_file": "sample1.pdf"},
        {"id": 2, "text": "This is the second chunk with some important information.", "source_file": "sample2.docx"},
        {"id": 3, "text": "Final chunk containing key summary points.", "source_file": "sample1.pdf"},
    ]

    builder = PromptBuilder()
    query = "What key points are in the document?"
    final_prompt = builder.build_prompt(chunks, mode="answer", query=query)
    print(final_prompt)
    
    summary_prompt = builder.build_prompt(chunks, mode="summary")
    print(summary_prompt)

