import os
import subprocess


class ModuleSearcher:
    def __init__(self, path_to_project):
        self.path_to_project = path_to_project

    def get_modules(self):
        try:
            subprocess.run(["pipreqs", f"{self.path_to_project}", "--savepath", f"{os.path.join(os.getcwd(), 'chosen_project_requirements', 'requirements.txt')}"])
        except FileNotFoundError:
            print("There is no such file or directory")
        except subprocess.CalledProcessError as e:
            print("Error: ", e)
        self._print_modules()

    @staticmethod
    def _print_modules():
        with open(os.path.join(os.getcwd(), 'chosen_project_requirements', 'requirements.txt')) as f:
            for line in f:
                line = line.strip("==")
                module_name = line.split("==")[0]
                module_version = line.split("==")[1]
                print(f"{module_name}: {module_version}")
