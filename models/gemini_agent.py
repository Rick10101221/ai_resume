import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import (
    GenerateContentConfig,
    GenerateContentConfigOrDict,
    GenerateContentResponse,
    HttpOptions,
)
from typing import List, Optional


class GeminiAgent:
    def __init__(self, model: str, system_instruction: str = None):
        load_dotenv()

        self.model = model
        self.client = genai.Client(
            api_key = os.getenv('GOOGLE_API_KEY'), 
            http_options = HttpOptions(api_version = 'v1alpha')
        )
        self.chat_session = None
        self._initializeChat(system_instruction)


    def _initializeChat(self, system_instruction: str) -> None:
        self.chat_session = self.client.chats.create(
            model = self.model,
            config = GenerateContentConfig(
                system_instruction = system_instruction
            )
        )


    def get_conversation_history(self) -> List:
        """Get the full conversation history"""
        return self.chat_session.get_history() if self.chat_session else []


    def sendMessage(self, message: str, config: Optional[GenerateContentConfigOrDict] = None) -> GenerateContentResponse:
        # try:
        response = self.chat_session.send_message(message, config)
        return response
        # except Exception as e:
        #     raise RuntimeError(f"Failed to get response from Gemini API: {e}.")

        
__all__ = ['GeminiAgent']