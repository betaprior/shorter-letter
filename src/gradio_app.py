import gradio as gr
import json
from functions_old import create_highlight_structure
import html2text
import requests

h = html2text.HTML2Text()
h.ignore_links = True

STYLE_DEFINITIONS = {
    "noun": "color: black; font-weight: bold;",
    "adjective": "color: gray;",
    "verb": "color: black; font-weight: bold;",
    "stop_word": "color: gray;",
}

precomputed_styles = None
text_content = None

def apply_styles(text, styles, style_definitions, selected_styles):
    styled_text = ""
    last_end = 0

    for style in styles:
        start = style['start']
        end = style['end']
        style_class = style['type']

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

with gr.Blocks(theme='JohnSmith9982/small_and_pretty') as demo:
    user_input = gr.Textbox(value="https://www.paulgraham.com/die.html", label="User Input", placeholder="Enter url here...")
    run_button = gr.Button(value="Run")
    style_checkbox = gr.CheckboxGroup(label="Select Styles to Apply", choices=["noun", "adjective", "verb", "stop_word"], value=["noun", "adjective", "verb", "stop_word"], visible=False)
    output = gr.Markdown()

    run_button.click(fn=fetch_text_and_apply_styles, inputs=[user_input, style_checkbox], outputs=[output, style_checkbox])
    style_checkbox.change(fn=update_styles, inputs=style_checkbox, outputs=output)

if __name__ == "__main__":
    demo.launch()