from abc import ABC, abstractmethod

from langchain.text_splitter import CharacterTextSplitter

from typing import Optional


class LLM(ABC):
    def __init__(self, chunk_size: int = 8000, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text_to_chunks(self, text: str):
        text_splitter = CharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

        split_text = text_splitter.create_documents([text])
        return split_text

    @abstractmethod
    def generate(self, result_type: str, input_data: str) -> Optional[str]:
        raise NotImplementedError
