import os
import re

from ContainerStudio.searching_imports import ModuleSearcher


def _find_files(path, pattern):
    matching_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if pattern.match(file):
                relative_path = os.path.relpath(os.path.join(root, file), start=path)
                matching_files.append(relative_path)
    return matching_files


def _get_file_names(files):
    file_names = [os.path.split(file)[-1] for file in files]
    return file_names


def use_requirements(path):
    pattern = re.compile(r".*requirements.*")
    result = _find_files(path=path, pattern=pattern)
    chosen_requirements = []
    file_names = []
    if result:
        file_names = _get_file_names(result)
        print(f"Found requirements.txt at:")
        for i in range(0, len(result)):
            print(f'{i}. {result[i]}')
        print('Choose appropriate requirements file. To quit press x.\n')
        while True:
            index = input()
            if index == 'x':
                break
            chosen_requirements.append(result[int(index)])
    else:
        print("File requirements.txt not found in the specified directory")
        user_choice = input("Do you want to search for imports your project files (y/n)?\n")
        if user_choice == "y":
            user_path_to_folder = input("Please enter the path to your project folder: \n")
            ModuleSearcher(path_to_project=user_path_to_folder).get_modules()
    return chosen_requirements, file_names
