from pandasai.llm.base import LLM
from pandasai.helpers.logger import Logger
from typing import Optional
import google.generativeai as genai

class GoogleGemini(LLM):
    def __init__(self, api_key: str, model: str = "models/gemini-1.5-pro-001", verbose: bool = False):
        self.api_key = api_key
        self.model = model
        self.verbose = verbose
        self._logger = Logger(verbose=verbose)
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model)

    @property
    def type(self) -> str:
        return "google_gemini"

    def chat(self, messages: list[dict]) -> str:
        chat = self._model.start_chat(history=[])
        full_response = chat.send_message(messages[-1]["content"])
        return full_response.text

    def call(self, instruction: str, context: Optional[str] = None) -> str:
        prompt = f"{context}\n\n{instruction}" if context else instruction
        response = self._model.generate_content(prompt)
        return response.text
