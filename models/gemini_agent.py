import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import List


class GeminiAgent:
    def __init__(self, model: str = 'gemini-1.5-flash', system_instruction: str = None):
        load_dotenv()

        self.model = model
        self.client = genai.Client(
            api_key = os.getenv('GOOGLE_API_KEY'), 
            http_options = types.HttpOptions(api_version = 'v1alpha')
        )
        self.chat_session = None
        self._initializeChat(system_instruction)


    def _initializeChat(self, system_instruction: str = None) -> None:
        self.chat_session = self.client.chats.create(
            model = self.model,
            config = types.GenerateContentConfig(
                system_instruction = system_instruction
            )
        )


    def get_conversation_history(self) -> List:
        """Get the full conversation history"""
        return self.chat_session.get_history() if self.chat_session else []


    def sendMessage(self, message: str) -> str:
        try:
            response = self.chat_session.send_message(message)
            print(f'Response: {response}')
            print(f'Response text: {response.text}')
            return response.text
        except Exception as e:
            raise RuntimeError(f"{e} Failed to get response from Gemini API")
        
__all__ = ['GeminiAgent']