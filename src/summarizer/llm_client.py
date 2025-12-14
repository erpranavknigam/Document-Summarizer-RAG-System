from llama_cpp import Llama

class LLMClient:
    def __init__(self, model_path):
        self.llm = Llama(model_path=model_path, n_ctx=2048, n_threads=8)

    def generate(self, prompt):
        out = self.llm(prompt, max_tokens=512, temperature=0.2)
        return out["choices"][0]["text"].strip()
