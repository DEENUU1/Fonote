from typing import Optional

from groq import Groq
from django.conf import settings
from .llm import LLM
import logging

logger = logging.getLogger(__name__)


class GroqLLM(LLM):
    def __init__(self):
        super().__init__(chunk_size=8000, chunk_overlap=100)
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model: str = "llama3-8b-8192"

    def get_response(self, result_type: str, input_data: str) -> Optional[str]:
        try:
            llm_response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an assistant responsible for processing transcriptions of videos and "
                                   f"podcasts. Do {result_type} based on the given text",
                    },
                    {
                        "role": "user",
                        "content": input_data
                    }
                ],
                model=self.model,
            )
            return llm_response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None

    def generate(self, result_type: str, input_data: str) -> Optional[str]:
        chunks = self.split_text_to_chunks(input_data)

        result = ""

        for chunk in chunks:
            response = self.get_response(result_type, chunk)
            if response:
                result += response + "\n\n"

        return result



