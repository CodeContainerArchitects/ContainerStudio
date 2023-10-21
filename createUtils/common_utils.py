import os
from tkinter import END


def _find_files(path, pattern):
    matching_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if pattern.match(file):
                relative_path = os.path.relpath(os.path.join(root, file), start=path)
                matching_files.append(relative_path)
    return matching_files

def update_list(listbox, data):
        listbox.delete(0, END)
        
        for item in data:
            listbox.insert(END, item)
            
def update_list_dict(listbox, data):
        listbox.delete(0, END)
        
        for name, version in data.items():
            listbox.insert(END, f'{name} ({version})')

def _add_line_to_file(line, path_to_file):
    with open(path_to_file, "a") as f:
        f.write(line + '\n')
