import gradio as gr
import json
from functions import process_text_to_json

STYLE_DEFINITIONS = {
    "noun": "color: black; font-weight: bold;",
    "adjective": "color: gray;",
    "verb": "color: black; font-weight: bold;",
    "stop_word": "color: gray;",
}

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
    if text_file is None:
        return ""
    with open(text_file.name, 'r') as txt_f:
        text = txt_f.read()

    json_data = json.loads(process_text_to_json(text))
    styles = json_data
    style_definitions = STYLE_DEFINITIONS

    styled_text = apply_styles(text, styles, style_definitions, selected_styles)
    return styled_text

with gr.Blocks(theme='JohnSmith9982/small_and_pretty') as demo:
    text_input = gr.File(label="Text File")
    style_checkbox = gr.CheckboxGroup(label="Select Styles to Apply", choices=["noun", "adjective", "verb", "stop_word"], value=["noun", "adjective", "verb", "stop_word"])
    output = gr.HTML()

    text_input.change(process_text_and_apply_styles, inputs=[text_input, style_checkbox], outputs=output)
    style_checkbox.change(process_text_and_apply_styles, inputs=[text_input, style_checkbox], outputs=output)

if __name__ == "__main__":
    demo.launch()