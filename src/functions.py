import json
from typing import TYPE_CHECKING

import spacy

if TYPE_CHECKING:
    from spacy.tokens import Doc

# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")


HighlightElement = dict[str, int | str]


def create_highlight_structure(text: str) -> list[HighlightElement]:
    doc: Doc = nlp(text)
    highlight_structure: list[HighlightElement] = []

    for token in doc:
        if token.is_stop:
            element_type: str = "stop_word"
        elif token.pos_ == "NOUN":
            element_type = "noun"
        elif token.pos_ == "VERB":
            element_type = "verb"
        elif token.pos_ == "ADJ":
            element_type = "adjective"
        else:
            continue

        element: HighlightElement = {
            "start": token.idx,
            "end": token.idx + len(token),
            "type": element_type,
            "token": token.text,
        }
        highlight_structure.append(element)

    return highlight_structure


# Function to process text and return JSON
def process_text_to_json(text: str) -> str:
    highlight_structure: list[HighlightElement] = create_highlight_structure(text)
    return json.dumps(highlight_structure, indent=2)
