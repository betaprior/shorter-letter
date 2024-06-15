import pytest
import json
from deepdiff import DeepDiff
from typing import List, Dict, Union
from src.functions import create_highlight_structure

HighlightElement = Dict[str, Union[int, str]]

@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "The quick brown fox jumps over the lazy dog.",
            [{'start': 0, 'end': 3, 'type': 'stop_word', 'token': 'The'},
 {'start': 4, 'end': 9, 'type': 'adjective', 'token': 'quick'},
 {'start': 10, 'end': 15, 'type': 'adjective', 'token': 'brown'},
 {'start': 16, 'end': 19, 'type': 'noun', 'token': 'fox'},
 {'start': 20, 'end': 25, 'type': 'verb', 'token': 'jumps'},
 {'start': 26, 'end': 30, 'type': 'stop_word', 'token': 'over'},
 {'start': 31, 'end': 34, 'type': 'stop_word', 'token': 'the'},
 {'start': 35, 'end': 39, 'type': 'adjective', 'token': 'lazy'},
 {'start': 40, 'end': 43, 'type': 'noun', 'token': 'dog'}]
        ),
        (
            "Python is a powerful programming language.",
            [{'start': 7, 'end': 9, 'type': 'stop_word', 'token': 'is'},
 {'start': 10, 'end': 11, 'type': 'stop_word', 'token': 'a'},
 {'start': 12, 'end': 20, 'type': 'adjective', 'token': 'powerful'},
 {'start': 21, 'end': 32, 'type': 'noun', 'token': 'programming'},
 {'start': 33, 'end': 41, 'type': 'noun', 'token': 'language'}]
        ),
        (
            "She sells sea shells by the sea shore.",
            [{'start': 0, 'end': 3, 'type': 'stop_word', 'token': 'She'},
 {'start': 4, 'end': 9, 'type': 'verb', 'token': 'sells'},
 {'start': 10, 'end': 13, 'type': 'noun', 'token': 'sea'},
 {'start': 14, 'end': 20, 'type': 'noun', 'token': 'shells'},
 {'start': 21, 'end': 23, 'type': 'stop_word', 'token': 'by'},
 {'start': 24, 'end': 27, 'type': 'stop_word', 'token': 'the'},
 {'start': 28, 'end': 31, 'type': 'noun', 'token': 'sea'},
 {'start': 32, 'end': 37, 'type': 'noun', 'token': 'shore'}]
        )
    ]
)
def test_create_highlight_structure(text: str, expected: List[HighlightElement]):
    # assert create_highlight_structure(text) == expected
    result = create_highlight_structure(text)

    for element in result:
        start_index = element["start"]
        end_index = element["end"]

        assert text[start_index:end_index] == element["token"]

    assert DeepDiff(result, expected) == {}
