import copy
import os
import numpy as np
from stdlib_list import stdlib_list


class ModuleSearcher:
    def __init__(self, path_to_project, python_version='3.11'):
        self.path_to_project = path_to_project
        self.python_version = python_version
        self.modules = []
        self.directories = []

    def get_modules(self):
        self._search_imports()
        self._extract_modules()
        self._extract_directories()
        self._remove_build_in_modules()
        self._remove_project_modules()

    def _search_imports(self):
        for root, dirs, files in os.walk(self.path_to_project):
            for file in files:
                if file.endswith(".py"):
                    self.directories.append(os.path.relpath(os.path.join(root, file), start=self.path_to_project))
                    with open(os.path.join(root, file), 'r') as f:
                        for l_no, line in enumerate(f):
                            if line.strip().startswith('import') or line.strip().startswith('from'):
                                self.modules.append(line)

    def _extract_modules(self):
        mods = [element.split(" ")[1].replace("\n", "").replace(",", "") for element in self.modules]
        mods = [element.split(".")[0] for element in mods]
        mods = list(set(mods))
        self.modules = mods

    def _remove_build_in_modules(self):
        libraries = stdlib_list(self.python_version)
        self.modules = [mod for mod in self.modules if mod not in libraries]

    def _remove_project_modules(self):
        to_remove = []
        for mod in self.modules:
            for file_name in self.directories:
                if file_name == mod:
                    to_remove.append(mod)
                    break
        mod = [m for m in self.modules if m not in to_remove]
        self.modules = mod

    def _extract_directories(self):
        self.directories = [directory.split("/") for directory in self.directories]
        self.directories = [item for sublist in self.directories for item in sublist]
        self.directories = list(set(self.directories))
        self.directories = [item.replace(".py", "") for item in self.directories]


module_searcher = ModuleSearcher(path_to_project='/home/ola/Desktop/example_2')
module_searcher.get_modules()
print(module_searcher.modules)

