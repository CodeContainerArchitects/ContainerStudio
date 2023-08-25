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


print(search_imports('/home/ola/Desktop/example/database_structures/project2'))
