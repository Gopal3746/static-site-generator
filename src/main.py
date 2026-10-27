import os
import shutil
import sys

from copystatic import copy_files_recursive
from generatepage import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Deleting files from Public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_files_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive("./content", "./template.html", dir_path_public, basepath)

if __name__ == "__main__":
    main()
