import os

from stdlib_list import stdlib_list


def search_imports(path_to_project):
    imports = []
    for root, dirs, files in os.walk(path_to_project):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), 'r') as f:
                    for l_no, line in enumerate(f):
                        if line.strip().startswith('import') or line.strip().startswith('from'):
                            print(line)
                            imports.append(line)
    return imports


def extract_modules(input_array):
    mods = [element.split(" ")[1].replace("\n", "") for element in input_array]
    mods = list(set(mods))
    return mods


def remove_build_in_modules(python_version='3.11', input_array=None):
    if input_array is None:
        input_array = []
    libraries = stdlib_list(python_version)
    mods = [mod for mod in input_array if mod not in libraries]
    return mods


import_lines = search_imports('/home/ola/Desktop/example/database_structures/project2')
print(import_lines)
print()
modules = extract_modules(input_array=import_lines)
print(modules)
print()
print(remove_build_in_modules(input_array=modules))

