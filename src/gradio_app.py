import gradio as gr
import json
from functions_old import create_highlight_structure
import html2text

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

def process_text_and_apply_styles(text_file, selected_styles):
    global precomputed_styles, text_content

    if text_file is not None:
        with open(text_file.name, 'r') as txt_f:
            text_content = txt_f.read()
        text_content = h.handle(text_content)
        precomputed_styles = create_highlight_structure(text_content)
    
    if precomputed_styles is None or text_content is None:
        return ""
    
    styled_text = apply_styles(text_content, precomputed_styles, STYLE_DEFINITIONS, selected_styles)
    print(styled_text)
    return styled_text

with gr.Blocks(theme='JohnSmith9982/small_and_pretty') as demo:
    text_input = gr.File(label="Text File")
    style_checkbox = gr.CheckboxGroup(label="Select Styles to Apply", choices=["noun", "adjective", "verb", "stop_word"], value=["noun", "adjective", "verb", "stop_word"])
    output = gr.Markdown()

    def update_styles(file, styles):
        return process_text_and_apply_styles(file, styles)

    text_input.change(fn=update_styles, inputs=[text_input, style_checkbox], outputs=output)
    style_checkbox.change(fn=update_styles, inputs=[text_input, style_checkbox], outputs=output)

if __name__ == "__main__":
    demo.launch()
