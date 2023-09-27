import os


def _find_files(path, pattern):
    matching_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if pattern.match(file):
                relative_path = os.path.relpath(os.path.join(root, file), start=path)
                matching_files.append(relative_path)
    return matching_files


def _add_line_to_file(line, path_to_file):
    with open(path_to_file, "w") as f:
        f.write(line)
