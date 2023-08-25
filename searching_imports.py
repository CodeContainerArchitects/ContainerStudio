import os


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
    modules = [element.split(" ")[1].replace("\n", "") for element in input_array]
    return modules


import_lines = search_imports('/home/ola/Desktop/example/database_structures/project2')
print(import_lines)

print(extract_modules(input_array=import_lines))

