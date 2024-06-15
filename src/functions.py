import re
from typing import TYPE_CHECKING

import nltk

nltk.download("words")
import spacy
from nltk.corpus import words

if TYPE_CHECKING:
    from spacy.tokens import Doc

# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")


HighlightElement = dict[str, int | str]


def is_valid_word(token: str) -> bool:
    # Regex to detect potential HTML tags
    tag_pattern = re.compile(r"<[^>]+>")
    if tag_pattern.match(token):
        return False
    return token.lower() in words.words()


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

        if is_valid_word(token.text):
            element: HighlightElement = {
                "start": token.idx,
                "end": token.idx + len(token),
                "type": element_type,
                "token": token.text,
            }

            highlight_structure.append(element)

    return highlight_structure
