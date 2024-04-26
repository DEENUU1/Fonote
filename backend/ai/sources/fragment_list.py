from dataclasses import dataclass
from .fragment import Fragment
from typing import List


@dataclass
class FragmentList:
    type_: str
    fragments: List[Fragment]
