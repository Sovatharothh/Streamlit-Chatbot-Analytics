from pandasai.llm.base import LLM

class GoogleGemini(LLM):
    def __init__(self, api_key: str, model: str = "models/gemini-1.5-pro-001"):
        self.api_key = api_key
        self.model = model
        super().__init__()

    @property
    def type(self) -> str:
        return "google_gemini"

    def chat(self, prompt: str) -> str:
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model)
        chat = model.start_chat()
        response = chat.send_message(prompt)
        return response.text
