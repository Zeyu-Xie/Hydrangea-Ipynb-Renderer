from bs4 import BeautifulSoup as bs4
import json
import os
import markdown
from Config import main_config
import re
from jinja2 import Template


def _remove_ansi_escape(text):
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def cell_to_markdown(cell):

    cell_type = cell.get("cell_type", "")
    source_list = cell.get("source", [])
    outputs = cell.get("outputs", [])

    # Case 1: Markdown Cell
    if cell_type == "markdown":
        return "".join(source_list)
    # Case 2: Code Cell
    elif cell_type == "code":
        # Part 1: Source Code
        markdown_content = "```python\n" + "".join(source_list) + "\n```"
        # Part 2: Outputs
        for output in outputs:
            if "output_type" not in output:
                continue
            markdown_content += "\n\n---"
            # Output Type: excute_result or display_data
            if (
                output["output_type"] == "execute_result"
                or output["output_type"] == "display_data"
            ):
                if "text/plain" in output["data"]:
                    markdown_content += (
                        "\n\n```" + "\n".join(output["data"]["text/plain"]) + "```"
                    )
                if "image/png" in output["data"]:
                    markdown_content += f'\n\n<img src="data:image/png;base64,{output["data"]["image/png"]}" />'
                if "image/jpeg" in output["data"]:
                    markdown_content += f'\n\n<img src="data:image/jpeg;base64,{output["data"]["image/jpeg"]}" />'
            # Output Type: stream
            elif output["output_type"] == "stream":
                if isinstance(output["text"], list):
                    markdown_content += "\n\n```\n" + "".join(output["text"]) + "```"
                else:
                    markdown_content += "\n\n```" + output["text"] + "```"
            # Output Type: error
            elif output["output_type"] == "error":
                markdown_content += _remove_ansi_escape(
                    "\n\n```\n" + "\n".join(output["traceback"]) + "\n```"
                )
        return markdown_content


def markdown_to_html(markdown_content, i):
    # Convert markdown to html
    html_content = markdown.markdown(
        markdown_content, extensions=["fenced_code", "codehilite", "extra"]
    )
    html_bs4 = bs4(html_content, "html.parser")
    # Create a bs4 object with section tag
    html_section = bs4("", "html.parser")
    section = html_section.new_tag("section", **{"class": "cell", "id": f"cell-{i}"})
    html_section.append(section)
    # Add the html content to the section tag
    section.extend(html_bs4)
    return html_section


def add_head(html_bs4, title):
    # Create a head tag
    html_bs4 = bs4("", "html.parser")
    html_head = html_bs4.new_tag("head")
    html_bs4.append(html_head)
    # Add title
    html_title = html_bs4.new_tag("title")
    html_title.string = title
    html_head.append(html_title)
    # Add meta tags
    html_meta = html_bs4.new_tag("meta")
    html_meta["charset"] = "utf-8"
    html_head.append(html_meta)
    return html_bs4


def add_body(html_bs4, html_list):
    # Create a body tag
    html_body = html_bs4.new_tag("body")
    html_bs4.append(html_body)
    # Add sections
    for html_section in html_list:
        html_body.append(html_section)
    return html_bs4


def add_css_content(html_bs4, css_path):
    # Create / Get the head tag
    html_head = html_bs4.new_tag("head") if html_bs4.head is None else html_bs4.head
    if html_bs4.head is None:
        html_bs4.insert(0, html_head)
    # Create a style tag
    css = html_bs4.new_tag("style")
    html_head.append(css)
    # Add CSS content
    css_template = open(
        os.path.join(os.path.dirname(__file__), css_path),
        "r",
        encoding="utf-8",
    ).read()
    css.string = Template(css_template).render(
        style_contentWidth=main_config.config["style"]["content_width"],
        style_pageSpace = main_config.config["style"]["page_space"],
        style_codeWrap = (
            "white-space: pre-wrap;" if main_config.config["style"]["code_wrap"] else ""
        ),
        style_allowTextSelect=(
            """
-webkit-user-select: text !important;
user-select: text !important;
"""
            if main_config.config["style"]["allow_text_select"]
            else ""
        ),
        style_showScrollbar=(
            """
::-webkit-scrollbar {
  display: none;
  width: 0;
  height: 0;
}

html, body {
  scrollbar-width: none;
  -ms-overflow-style: none;
  overflow: -moz-scrollbars-none;
}
""" if not main_config.config["style"]["show_scrollbar"] else ""
        ),
    )
    return html_bs4


class Ipynb_Converter:

    def convert(self, path):
        """
        Convert an ipynb file to an html string.
        :param path: The path of the ipynb file.
        :return: The HTML string.
        """

        # Read the ipynb file
        try:
            with open(path, "r", encoding="utf-8") as file:
                ipynb_json = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading file {path}: {e}")
            return ""
        cell_list = ipynb_json.get("cells", [])

        # Parse each cell
        html_section_list = []
        for i, cell in enumerate(cell_list):
            # Cell to Markdown
            markdown_content = cell_to_markdown(cell)
            # Markdown to section HTML
            html_section = markdown_to_html(markdown_content, i)
            html_section_list.append(html_section)

        # Create a bs4 object
        html_bs4 = bs4("", "html.parser")

        # Add Head
        html_bs4 = add_head(html_bs4, os.path.basename(path))

        # Add Body
        html_bs4 = add_body(html_bs4, html_section_list)

        # Add current CSS theme to head
        html_bs4 = add_css_content(
            html_bs4, main_config.config["theme"]["current_theme"]
        )

        # Add current fundamental style to head
        html_bs4 = add_css_content(
            html_bs4, main_config.config["theme"]["fundamental_style"]
        )

        # Return the HTML
        return html_bs4.prettify()


main_ipynb_converter = Ipynb_Converter()

__all__ = ["ipynb_converter"]
