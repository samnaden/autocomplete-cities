import functools
import math
from difflib import SequenceMatcher


@functools.lru_cache(maxsize=int(math.pow(2, 16)))
def get_similarity_score(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()
