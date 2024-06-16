import gradio as gr
import html2text
import requests
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

from src.functions_old import create_highlight_structure

h = html2text.HTML2Text()
h.ignore_links = True

STYLE_DEFINITIONS = {
    "noun": "color: navy; font-weight: bold;",  # Dark blue for better contrast
    "adjective": "color: orange;",  # Medium orange for visibility
    "verb": "color: red; font-weight: bold;",  # Bright red for emphasis
    "stop_word": "color: lightgray;",  # Light gray to deemphasize stop words
}


STYLE_DEFINITIONS_SENTENCE = {
    "top": "color: red; font-weight: bold;",  # Bright red for emphasis
    "bottom": "color: lightgray;",  # Light gray to deemphasize stop words
}

custom_css = """
body {
    font-family: 'Verdana', sans-serif;
    font-size: 16px; /* Adjust the size as needed */
    color: #333333; /* Optional: Adjust the color if needed */
}

p {
    font-family: 'Verdana', sans-serif;
    font-size: 24px; /* Adjust the size as needed */
    color: #333333; /* Optional: Adjust the color if needed */
}

em {
    font-style: italic;
    color: #888888; /* Optional: Adjust the color if needed */
}
"""

precomputed_styles = None
text_content = None


def apply_styles(text, styles, style_definitions, selected_styles):
    styled_text = ""
    last_end = 0

    for style in styles:
        start = style["start"]
        end = style["end"]
        style_class = style["type"]

        if style_class in selected_styles:
            style_def = style_definitions.get(style_class, "")
            styled_text += text[last_end:start]
            styled_text += f'<span style="{style_def}">{text[start:end]}</span>'
            last_end = end

    styled_text += text[last_end:]

    return styled_text


def fetch_text_and_apply_styles(url, selected_styles):
    global precomputed_styles, text_content

    if url is not None:
        response = requests.get(url)
        text_content = h.handle(response.text)
        precomputed_styles = create_highlight_structure(text_content)

    if precomputed_styles is None or text_content is None:
        return "", gr.update(visible=True)

    styled_text = apply_styles(text_content, precomputed_styles, STYLE_DEFINITIONS, selected_styles)
    return styled_text, gr.update(visible=True)


def update_styles(selected_styles):
    if precomputed_styles is None or text_content is None:
        return ""

    styled_text = apply_styles(text_content, precomputed_styles, STYLE_DEFINITIONS, selected_styles)
    return styled_text

def get_sentence_embeddings(doc):
    nlpdoc = nlp(doc)
    sentences = [sent.text for sent in nlpdoc.sents]
    return sentences, model.encode(sentences)

def get_closest_to_summary(orig, summary, invert=False):
    summary_embedding = model.encode(summary)
    sentence_embeddings = get_sentence_embeddings(orig)
    rankings = cosine_similarity(sentence_embeddings, [summary_embedding]).T[0]
    # get top indexes
    if invert:
        rankings = -rankings
    return np.argsort(-rankings)

def get_top_n_sentences(orig, summary, n, invert=False):
    ranked_sent_idxs = get_closest_to_summary(orig, summary)
    if invert:
        ranked_sent_idxs = ranked_sent_idxs[::-1]
    nlpdoc = nlp(orig)
    orig_sentences = [sent.text for sent in nlpdoc.sents]
    return [orig_sentences[i] for i in ranked_sent_idxs[:n]]

def get_cosine_similarity(orig, summary):
    summary_embedding = model.encode(summary)
    sentences, sentence_embeddings = get_sentence_embeddings(orig)
    return sentences, cosine_similarity(sentence_embeddings, [summary_embedding]).T[0]


from src.tmp import summary as die_summary

def fetch_text_style_by_sentence_relevance(url, style_definitions):
    if url is None:
        return "", gr.update(visible=True)

    response = requests.get(url)
    text_content = h.handle(response.text)
    summary = die_summary
    sentences, relevances = get_cosine_similarity(text_content, summary)
    quantiles = np.quantile(relevances, [0.25, 0.5, 0.75, 1.0])
    quantile_labels = np.searchsorted(quantiles, relevances, side='right')

    styled_text = []
    for i, sentence in enumerate(sentences):
        if quantile_labels[i] == 3:
            style_def = style_definitions.get("top", "")
            styled_text.append(f'<span style="{style_def}">{sentence}</span>')
        elif quantile_labels[i] == 0:
            style_def = style_definitions.get("bottom", "")
            styled_text.append(f'<span style="{style_def}">{sentence}</span>')
        else:
            styled_text.append(f"{sentence}")

    return " ".join(styled_text)

with gr.Blocks(theme="JohnSmith9982/small_and_pretty", css=custom_css) as demo:
    user_input = gr.Textbox(
        value="https://www.paulgraham.com/die.html", label="User Input", placeholder="Enter url here..."
    )
    run_button = gr.Button(value="Run")
    output = gr.Markdown()

    def get_styled_text(url):
        return fetch_text_style_by_sentence_relevance(url, STYLE_DEFINITIONS_SENTENCE)

    run_button.click(
        fn=get_styled_text, inputs=[user_input], outputs=[output]
    )

if __name__ == "__main__":
    demo.launch()
