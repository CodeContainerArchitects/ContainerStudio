import ast
import os
import subprocess
import sys

from stdlib_list import stdlib_list


class ModuleSearcher:
    def __init__(self, path_to_project, python_version='3.11'):
        self.path_to_project = path_to_project
        self.python_version = python_version
        self.modules = []
        self.directories = []
        self.pip_modules_for_user_display = []
        self.pip_modules_from_file = []
        self.pip_modules_to_file = []
        self.external_modules = []

    def get_modules(self):
        self._search_imports()
        self._extract_directories()
        self._remove_build_in_modules()
        self._remove_project_modules()
        self._extract_pip_and_external_modules()

    # look for all modules in the project
    def _search_imports(self):
        for root, dirs, files in os.walk(self.path_to_project):
            for file in files:
                if file.endswith(".py"):
                    self.directories.append(os.path.relpath(os.path.join(root, file), start=self.path_to_project))
                    with open(os.path.join(root, file), 'r') as f:
                        file_to_explore = f.read()
                    tree = ast.parse(file_to_explore)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                self.modules.append(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            self.modules.append(node.module)
        self.modules = [mod for mod in self.modules if mod is not None]
        self.modules = [mod.split(".")[0] for mod in self.modules]
        self.modules = list(set(self.modules))

    # remove build in modules e.g. numpy, os
    def _remove_build_in_modules(self):
        libraries = stdlib_list(self.python_version)
        self.modules = [mod for mod in self.modules if mod not in libraries]

    # remove project modules which comes from project files
    def _remove_project_modules(self):
        to_remove = []
        for mod in self.modules:
            for file_name in self.directories:
                if file_name == mod:
                    to_remove.append(mod)
                    break
        mod = [m for m in self.modules if m not in to_remove]
        self.modules = mod

    # get all names of files to delete that modules from self.modules
    def _extract_directories(self):
        self.directories = [directory.split("/") for directory in self.directories]
        self.directories = [item for sublist in self.directories for item in sublist]
        self.directories = list(set(self.directories))
        self.directories = [item.replace(".py", "") for item in self.directories]

    def _extract_pip_and_external_modules(self):
        self._get_pip_modules()
        for i in range(len(self.modules)):
            if self.modules[i] not in self.pip_modules_from_file:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", self.modules[i], "--dry-run"])
                    self.pip_modules_for_user_display.append(self.modules[i])
                    self.pip_modules_to_file.append(self.modules[i])
                except subprocess.CalledProcessError as e:
                    print(e)
                    self.external_modules.append(self.modules[i])
            else:
                self.pip_modules_for_user_display.append(self.modules[i])
        self._save_pip_modules()

    def _get_pip_modules(self):
        with open("pip_modules.txt", 'r') as f:
            self.pip_modules_from_file = [line.replace("\n", "") for line in f.readlines()]

    def _save_pip_modules(self):
        if len(self.pip_modules_to_file) != 0:
            with open("pip_modules.txt", 'a') as f:
                print("\n".join(self.pip_modules_to_file) + "\n")
                f.write("\n".join(self.pip_modules_to_file) + "\n")


module_searcher = ModuleSearcher(path_to_project="/home/ola/Desktop/example_python_codes/example_4/dogs_app_kivy")
module_searcher.get_modules()
print(f"ALl modules: \n {module_searcher.modules} \n")
print(f"Pip modules: \n {module_searcher.pip_modules_for_user_display} \n")
print(f"External modules: \n {module_searcher.external_modules} \n")
print(f"Pip modules to file: \n {module_searcher.pip_modules_to_file} \n")
