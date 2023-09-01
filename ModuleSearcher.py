import os
import subprocess


class ModuleSearcher:
    def __init__(self, path_to_project):
        self.path_to_project = path_to_project
        self.name_of_result_file = "packages_found.txt"
        if not os.path.exists(os.path.join(os.getcwd(), "code_container_architect_founded_packages")):
            os.mkdir(os.path.join(os.getcwd(), "code_container_architect_founded_packages"))

    def get_modules(self):
        try:
            subprocess.run(["pipreqs", "--savepath", os.path.join("code_container_architect_founded_packages", self.name_of_result_file), f"{self.path_to_project}"])
        except FileNotFoundError:
            print("There is no such file or directory")
        except subprocess.CalledProcessError as e:
            print("Error: ", e)
        self._print_modules()

    def _print_modules(self):
        with open(os.path.join(os.getcwd(), "code_container_architect_founded_packages", self.name_of_result_file)) as f:
            for line in f:
                line = line.strip("==")
                module_name = line.split("==")[0]
                module_version = line.split("==")[1]
                print(f"{module_name}: {module_version}")


mod_finder = ModuleSearcher(path_to_project='/home/ola/Desktop/example_python_codes/example_13/cli/Project_files')
mod_finder.get_modules()
