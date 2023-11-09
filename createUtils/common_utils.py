import os
from tkinter import END
from bs4 import BeautifulSoup
import requests


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


def map_apt_package(package, os_name):
    response = requests.get(url=f"https://command-not-found.com/{package}")
    if response.status_code == 200:
        parsed_response = BeautifulSoup(response.text)
        find_div = parsed_response.body.find('div', attrs={'data-os': os_name})
        if find_div:
            find_package = find_div.find('code').text
            return find_package.split(' ')[-1]
        else:
            print("No <code> in div")
    else:
        print("Bad response")
