from typing import Optional

from groq import Groq
from django.conf import settings
from .llm import LLM
import logging

logger = logging.getLogger(__name__)


class GroqLLM(LLM):
    """A class representing a Groq-based Large Language Model (LLM).

    Inherits from LLM.

    Attributes:
        client (Groq): An instance of the Groq class for interacting with the Groq API.
        model (str): The name of the language model used for processing text.
    """

    def __init__(self):
        """Initialize the GroqLLM object."""
        super().__init__(chunk_size=8000, chunk_overlap=100)
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model: str = "llama3-8b-8192"

    def get_response(self, result_type: str, input_data: str, language: str) -> Optional[str]:
        """Generate a response based on the given input data.

        Args:
            result_type (str): The type of result to generate.
            input_data (str): The input data to process.
            language (str): The language for the response.

        Returns:
            Optional[str]: The generated response as a string, or None if an error occurs.
        """
        try:
            llm_response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"Response must be in {language} language."
                    },
                    {
                        "role": "system",
                        "content": f"Format response as a MD file."
                    },
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
            content = llm_response.choices[0].message.content
            return content

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None

    def generate(self, result_type: str, input_data: str, language: str) -> Optional[str]:
        """Generate results for the given input data.

        Args:
            result_type (str): The type of result to generate.
            input_data (str): The input data to process.
            language (str): The language for the response.

        Returns:
            Optional[str]: The generated results as a string, or None if an error occurs.
        """
        chunks = self.split_text_to_chunks(input_data)

        result = ""

        for chunk in chunks:
            response = self.get_response(result_type, chunk.page_content, language)
            if response:
                result += response + "\n\n"

        return result


