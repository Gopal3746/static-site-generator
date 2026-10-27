import os
import shutil

from block_markdown import markdown_to_html_node, extract_title

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    os.makedirs(dest_dir_path, exist_ok=True)
    files = os.listdir(dir_path_content)
    for file in files:
        src = os.path.join(dir_path_content, file)
        dest = os.path.join(dest_dir_path, file)
        if os.path.isfile(src):
            if not src.endswith(".md"):
                continue
            dest = os.path.splitext(dest)[0] + ".html"
            print(f"Generating page from {src} to {dest} using {template_path}")
            with open(src, "r") as f:
                markdown = f.read()
            with open(template_path, "r") as f:
                template = f.read()
            html_string = markdown_to_html_node(markdown).to_html()
            title = extract_title(markdown)
            page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(page)
        else:
            generate_pages_recursive(src, template_path, dest)
