import os
import subprocess

from createUtils.common_utils import _add_line_to_file
from createUtils.package_listing import apt_packages


class ModuleSearcher:
    def __init__(self, path_to_project, requirements_file_name):
        self.path_to_project = path_to_project
        self.requirements_file_name = requirements_file_name
        self.path_to_requirements_file = os.path.join(self.path_to_project, self.requirements_file_name)
        self.apt_modules = []
        self.not_known_modules = []

    def get_modules(self):
        try:
            subprocess.run(["pipreqs", "--savepath", self.path_to_requirements_file, f"{self.path_to_project}"])
            self._find_subprocess()
            return [os.path.relpath(self.path_to_requirements_file, start=self.path_to_project)], [self.requirements_file_name], self.apt_modules, self.not_known_modules
        except FileNotFoundError:
            print("There is no such file or directory")
        except subprocess.CalledProcessError as e:
            print("Error: ", e)

    def _find_subprocess(self):
        for root, dirs, files in os.walk(self.path_to_project):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file)) as f:
                        file_content = f.readlines()
                    # search for aliases to subprocess
                    subprocess_alias = ''
                    for line in file_content:
                        if not line.startswith('#') and line.startswith('import subprocess as'):
                            subprocess_alias = line.split('as')[1].replace('\n', '')
                    for line in file_content:
                        if not line.startswith("#"):
                            command = ''
                            if subprocess_alias == '':
                                if 'subprocess.run(["' in line:
                                    command = line.split('"')[1].replace('\n', '')
                                elif "subprocess.run(['" in line:
                                    command = line.split("'")[1].replace('\n', '')
                            else:
                                if f'{subprocess_alias}.run(["' in line:
                                    command = line.split('"')[1].replace('\n', '')
                                elif f"{subprocess_alias}.run(['" in line:
                                    command = line.split("'")[1].replace('\n', '')
                            print(command)
                            if command != '':
                                subprocess_result = 1
                                try:
                                    subprocess_result = subprocess.run(['pip', 'install', command, '--dry-run'])
                                except subprocess.CalledProcessError as e:
                                    print("something went wrong")
                                if subprocess_result.returncode == 0:
                                    _add_line_to_file(line=command, path_to_file=self.path_to_requirements_file)
                                else:
                                    # check if apt-module
                                    if command in apt_packages:
                                        self.apt_modules.append(command)
                                    else:
                                        self.not_known_modules.append(command)

    def _print_modules(self):
        with open(os.path.join(self.path_to_project, self.requirements_file_name)) as f:
            for line in f:
                line = line.strip("==")
                module_name = line.split("==")[0]
                module_version = line.split("==")[1]
                print(f"{module_name}: {module_version}")
