import gradio as gr
import json

import requests
from bs4 import BeautifulSoup

text_input = gr.File(label="Text File")
json_input = gr.File(label="JSON File")
user_input = gr.Textbox(value="https://www.paulgraham.com/die.html", label="User Input", placeholder="Enter url here...")
output = gr.HTML()
user_input2 = gr.Textbox(value="https://www.paulgraham.com/die.html", label="User Input", placeholder="Enter url here...")
output2 = gr.HTML()

import html2text
h = html2text.HTML2Text()
h.ignore_links = True
from markdown2 import Markdown
markdowner = Markdown()

def process_url_paragraphs(url):
    # text = get_paragraphs_from_url(url)
    response = requests.get(url)
    result = h.handle(response.text)
    html_from_md = markdowner.convert(result)
    print(html_from_md)
    return html_from_md

test_parser = gr.Interface(
    fn=process_url_paragraphs,
    inputs=[user_input2],
    outputs=output2,
    title="Text Styler",
    description="Upload a text file and a JSON file with styling information."
)

if __name__ == "__main__":
    test_parser.launch()
