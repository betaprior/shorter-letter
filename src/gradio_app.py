import gradio as gr
import json

STYLE_DEFINITIONS = {
    "stop_word": "opacity: 0.5;",
    "noun": "font-weight: bold; color: blue;",
}

def apply_styles(text, styles, style_definitions):
    styled_text = ""
    last_end = 0
    
    for style in styles:
        start = style['start']
        end = style['end']
        style_class = style['type']
        style_def = style_definitions.get(style_class, "")

        styled_text += text[last_end:start]

        styled_text += f'<span style="{style_def}">{text[start:end]}</span>'

        last_end = end

    styled_text += text[last_end:]
    
    return styled_text

def load_and_apply_styles(text_file, json_file):

    with open(text_file.name, 'r') as txt_f, open(json_file.name, 'r') as json_f:
        text = txt_f.read()
        json_content = json_f.read()

    json_data = json.loads(json_content)
    styles = json_data['styles']
    style_definitions = STYLE_DEFINITIONS

    styled_text = apply_styles(text, styles, style_definitions)
    return styled_text

text_input = gr.File(label="Text File")
json_input = gr.File(label="JSON File")
output = gr.HTML()

interface = gr.Interface(
    fn=load_and_apply_styles,
    inputs=[text_input, json_input],
    outputs=output,
    title="Text Styler",
    description="Upload a text file and a JSON file with styling information."
)

if __name__ == "__main__":
    interface.launch()
