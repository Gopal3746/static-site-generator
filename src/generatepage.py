import os
import shutil

from block_markdown import markdown_to_html_node, extract_title

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    dir_name = os.path.dirname(dest_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(template)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    for name in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, name)
        dest = os.path.join(dest_dir_path, name)
        if os.path.isfile(src):
            if src.endswith(".md"):
                generate_page(src, template_path, os.path.splitext(dest)[0] + ".html")
        else:
            generate_pages_recursive(src, template_path, dest)
