from typing import Optional

from groq import Groq
from django.conf import settings


class GroqLLM:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model: str = "llama3-8b-8192"

    def get_response(self, result_type: str, input_data: str) -> Optional[str]:
        try:
            llm_response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an assistant responsible for processing transcriptions of videos and podcasts."
                                   f" Do {result_type} based on the given text",
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
            print(e)
            # TODO add logger
            return None



