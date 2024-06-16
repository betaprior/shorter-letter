import json
from typing import TYPE_CHECKING

import spacy
from openai import OpenAI
import os
from src.guiding_principles import get_principles

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


if TYPE_CHECKING:
    from spacy.tokens import Doc

# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")


HighlightElement = dict[str, int | str]


def create_highlight_structure(text: str) -> list[HighlightElement]:
    doc: Doc = nlp(text)
    highlight_structure: list[HighlightElement] = []
    markdown_symbols = ["#", "*", "_", "`", "[", "]", "(", ")"]
    for token in doc:
        if token.text in markdown_symbols:
            continue
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


def get_text_summary(text: str) -> str:
    principles = get_principles()
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": f"You are a helpful assistant that summarizes text. And use these guiding principles about strong informative text: {principles}"
        },
        {
            "role": "user",
            "content": f"Give extensive summary. Length should be roughly half of the original text.:\n\n{text}"
        }
    ],
    model="gpt-4o"
    )

    return chat_completion.choices[0].message.content

