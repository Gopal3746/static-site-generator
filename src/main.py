import os
import shutil

from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from generatepage import generate_page

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    print("Deleting files from Public director...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_files_recursive(dir_path_static, dir_path_public)
    generate_page("./content/index.md", "./template.html", "./public/index.html")


if __name__ == "__main__":
    main()
