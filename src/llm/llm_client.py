import os
import logging
from dotenv import load_dotenv

load_dotenv()
try:
    from google import genai
    from google.genai.errors import ClientError
except ImportError:
    genai = None
    ClientError = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from llama_cpp import Llama


class LLMClient:
    def __init__(
        self,
        model_path: str,
        n_ctx: int = 2048,
        n_threads: int = 8,
        gemini_model: str = "models/gemini-2.5-flash",
        openai_model: str = "gpt-4o-mini",
    ):
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        
        # 1. Initialize OpenAI
        self.openai_client = None
        self.openai_model = openai_model
        if OpenAI and os.getenv("OPENAI_API_KEY"):
            try:
                self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                logging.info("LLM: OpenAI initialized")
            except Exception as e:
                logging.warning(f"OpenAI init failed: {e}")

        # 2. Initialize Gemini
        self.gemini_client = None
        self.gemini_model = gemini_model
        if genai and os.getenv("GEMINI_API_KEY"):
            try:
                self.gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
                logging.info("LLM: Gemini initialized")
            except Exception as e:
                logging.warning(f"Gemini init failed: {e}")

        # 3. Initialize Local (Always as fallback)
        self.llm = None
        try:
            self.llm = Llama(
                model_path=model_path,
                n_ctx=n_ctx,
                n_threads=n_threads,
                verbose=False,
            )
            logging.info("LLM: Local Mistral initialized")
        except Exception as e:
            logging.error(f"Local LLM init failed: {e}")

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
        # 1. Try OpenAI
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model=self.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return response.choices[0].message.content
            except Exception as e:
                logging.warning(f"OpenAI failed → fallback: {e}")

        # 2. Try Gemini
        if self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model=self.gemini_model,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    ) if hasattr(genai.types, 'GenerateContentConfig') else None
                )
                return response.text
            except Exception as e:
                logging.warning(f"Gemini failed → fallback: {e}")

        # 3. Fallback to Local
        if self.llm:
            output = self.llm(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>"],
            )
            return output["choices"][0]["text"]
        
        raise RuntimeError("All LLM providers failed. Please check your API keys or local model path.")
