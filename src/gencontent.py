import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node
def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            text = line[2:].strip()
            return text


    raise Exception("No title provided")




def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        md_contents = f.read()
        

    with open(template_path, "r") as f:
        template = f.read()


    content_html = markdown_to_html_node(md_contents)
    content_html = content_html.to_html()

    title = extract_title(md_contents)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content_html)

    os.makedirs(os.path.dirname(dest_path), exist_ok= True)

    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            dest_path = os.path.join(dest_dir_path, item)
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(item_path, template_path, dest_path)
        else:
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item))