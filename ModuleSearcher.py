import os
import subprocess


class ModuleSearcher:
    def __init__(self, path_to_project, file_name):
        self.path_to_project = path_to_project
        self.file_name = file_name

    def get_modules(self):
        try:
            subprocess.run(["pipreqs", "--savepath", os.path.join(self.path_to_project, self.file_name), f"{self.path_to_project}"])
            self._print_modules()
            return [os.path.relpath(os.path.join(self.path_to_project, self.file_name), start=self.path_to_project)], [self.file_name]
        except FileNotFoundError:
            print("There is no such file or directory")
        except subprocess.CalledProcessError as e:
            print("Error: ", e)

    def _print_modules(self):
        with open(os.path.join(self.path_to_project, self.file_name)) as f:
            for line in f:
                line = line.strip("==")
                module_name = line.split("==")[0]
                module_version = line.split("==")[1]
                print(f"{module_name}: {module_version}")
