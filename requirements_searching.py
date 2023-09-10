import os
import re
from createUtils.common_utils import _find_files
from ModuleSearcher import ModuleSearcher


def _get_file_names(files):
    file_names = [os.path.split(file)[-1] for file in files]
    return file_names


def use_requirements(path):
    pattern = re.compile(r".*requirements.*")
    result = _find_files(path=path, pattern=pattern)
    chosen_requirements = []
    file_names = []
    if result:
        print(f"Found requirements.txt at:")
        for i in range(0, len(result)):
            print(f'{i}. {result[i]}')
        print('Choose appropriate requirements file. To quit press x.\n')
        while True:
            index = input()
            if index == 'x':
                break
            chosen_requirements.append(result[int(index)])
        chosen_requirements = list(set(chosen_requirements))
        file_names = _get_file_names(chosen_requirements)
    else:
        print("Requirements file not found in the project directory.")
        user_choice = input("Do you want to search for imports your project files (y/n)?\n")
        if user_choice == "y":
            while True:
                user_filename = input("Enter the name of the requirements file: \n")
                if os.path.exists(os.path.join(path, user_filename)):
                    print("File arleady exists. Choose another file name.\n")
                else:
                    break
            chosen_requirements, file_names = ModuleSearcher(path_to_project=path, file_name=user_filename).get_modules()
    return chosen_requirements, file_names
