from abc import ABC, abstractmethod

from langchain.text_splitter import CharacterTextSplitter

from typing import Optional


class LLM(ABC):
    """Abstract base class representing a Large Language Model (LLM).

    Attributes:
        chunk_size (int): The size of each chunk for splitting text.
        chunk_overlap (int): The amount of overlap between consecutive text chunks.
    """

    def __init__(self, chunk_size: int = 8000, chunk_overlap: int = 100):
        """Initialize the LLM object.

        Args:
            chunk_size (int, optional): The size of each chunk for splitting text. Defaults to 8000.
            chunk_overlap (int, optional): The amount of overlap between consecutive text chunks. Defaults to 100.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text_to_chunks(self, text: str):
        """Split the input text into chunks.

        Args:
            text (str): The input text to split.

        Returns:
            List[str]: A list of text chunks.
        """
        text_splitter = CharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

        split_text = text_splitter.create_documents([text])
        return split_text

    @abstractmethod
    def generate(self, result_type: str, input_data: str, language: str) -> Optional[str]:
        """Generate results for the given input data.

        This method must be implemented by subclasses.

        Args:
            result_type (str): The type of result to generate.
            input_data (str): The input data to process.
            language (str): The language for the response.

        Returns:
            Optional[str]: The generated results as a string, or None if an error occurs.
        """
        raise NotImplementedError
