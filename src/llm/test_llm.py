from llama_cpp import Llama
import os

MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    )
)

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=8,
)

response = llm(
    "Say hello in one sentence.",
    max_tokens=50,
    stop=["</s>"]
)

print(response["choices"][0]["text"])
