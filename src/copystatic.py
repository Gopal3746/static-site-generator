import shutil
import os

def copy_files_recursive(path_to_source: str, path_to_destination: str):
    if not os.path.exists(path_to_destination):
        os.mkdir(path_to_destination)
    entries = os.listdir(path_to_source)
    for filename in entries:
        if filename == ".DS_Store":
            continue
        path_to_entry = os.path.join(path_to_source, filename)
        path_to_public = os.path.join(path_to_destination, filename)
        if os.path.isfile(path_to_entry):
            print(f"Copying file {path_to_entry} to {path_to_public}")
            shutil.copy(path_to_entry, path_to_public)
        else:
            copy_files_recursive(path_to_entry, path_to_public)
