import gradio as gr
import html2text
import requests

from src.functions_old import create_highlight_structure

h = html2text.HTML2Text()
h.ignore_links = True

STYLE_DEFINITIONS = {
    "noun": "color: navy; font-weight: bold;",  # Dark blue for better contrast
    "adjective": "color: orange;",  # Medium orange for visibility
    "verb": "color: red; font-weight: bold;",  # Bright red for emphasis
    "stop_word": "color: lightgray;",  # Light gray to deemphasize stop words
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


with gr.Blocks(theme="JohnSmith9982/small_and_pretty", css=custom_css) as demo:
    user_input = gr.Textbox(
        value="https://www.paulgraham.com/die.html", label="User Input", placeholder="Enter url here..."
    )
    run_button = gr.Button(value="Run")
    style_checkbox = gr.CheckboxGroup(
        label="Select Styles to Apply",
        choices=["noun", "adjective", "verb", "stop_word"],
        value=["noun", "adjective", "verb", "stop_word"],
        visible=False,
    )
    output = gr.Markdown()

    run_button.click(
        fn=fetch_text_and_apply_styles, inputs=[user_input, style_checkbox], outputs=[output, style_checkbox]
    )
    style_checkbox.change(fn=update_styles, inputs=style_checkbox, outputs=output)

if __name__ == "__main__":
    demo.launch()
