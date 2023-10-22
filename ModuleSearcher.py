import os
import string
import subprocess

from createUtils.common_utils import _add_line_to_file
from createUtils.package_listing import apt_packages, build_in_packages


class ModuleSearcher:
    def __init__(self, path_to_project, requirements_file_name):
        self.path_to_project = path_to_project
        self.requirements_file_name = requirements_file_name
        self.path_to_requirements_file = os.path.join(self.path_to_project, self.requirements_file_name)
        self.apt_modules = []
        self.apt_pip_modules = []
        self.not_known_modules = []

    def get_modules(self):
        try:
            subprocess.run(["pipreqs", "--savepath", self.path_to_requirements_file, f"{self.path_to_project}", "--mode", "no-pin"])
            self._find_subprocess()
            self._find_os()
            return [os.path.relpath(self.path_to_requirements_file, start=self.path_to_project)], [self.requirements_file_name], self.apt_modules, self.not_known_modules, self.apt_pip_modules
        except FileNotFoundError:
            print("There is no such file or directory")
        except subprocess.CalledProcessError as e:
            print("Error: ", e)

    @staticmethod
    def _find_alias_and_functions(name, file_content):
        alias = ''
        functions = []
        for line in file_content:
            if not line.startswith('#') and line.startswith(f'import {name} as'):
                alias = line.split('as')[1].strip(string.whitespace)
            if line.startswith(f'from {name} import'):
                functions = [item.strip() for item in line.split('import')[1].replace('\n', '').split(',')]
        alias = name if alias == '' else alias
        return alias, functions

    def _analyze_command(self, command):
        if command != '' and command not in build_in_packages:
            subprocess_result = 1
            try:
                subprocess_result = subprocess.run(['pip', 'install', command, '--dry-run'])
            except subprocess.CalledProcessError as e:
                print("something went wrong")
            if subprocess_result.returncode == 0 and command in apt_packages.values():
                self.apt_pip_modules.append(command)
            elif subprocess_result.returncode == 0:
                _add_line_to_file(line=command, path_to_file=self.path_to_requirements_file)
            else:
                # check if apt-module
                if command in apt_packages.keys():
                    self.apt_modules[command] = "no version: "
                else:
                    self.not_known_modules.append(command)

    def _find_os(self):
        for root, dirs, files in os.walk(self.path_to_project):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file)) as f:
                        file_content = f.readlines()

                    os_alias, os_functions = self._find_alias_and_functions(name='os', file_content=file_content)

                    for line in file_content:
                        if not line.startswith("#"):
                            command = ''
                            if f'{os_alias}.system("' in line or f'{os_alias}.popen("' in line:
                                command = line.split('"')[1].replace('\n', '').split(' ')[0]
                            elif f"{os_alias}.system('" in line or f"{os_alias}.popen('" in line:
                                command = line.split("'")[1].replace('\n', '').split(' ')[0]
                            else:
                                for func in os_functions:
                                    if f'{func}("' in line:
                                        command = line.split('"')[1].replace('\n', '').split(" ")[0]
                                    elif f"{func}('" in line:
                                        command = line.split("'")[1].replace('\n', '').split(" ")[0]
                            self._analyze_command(command)

    def _find_subprocess(self):
        for root, dirs, files in os.walk(self.path_to_project):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file)) as f:
                        file_content = f.readlines()

                    # detect subprocess alias
                    subprocess_alias, subprocess_functions = self._find_alias_and_functions(name='subprocess', file_content=file_content)

                    # find subprocess
                    for line in file_content:
                        if not line.startswith("#"):
                            command = ''
                            # subprocess or subprocess alias
                            if (f'{subprocess_alias}.run(["' in line
                                    or f'{subprocess_alias}.run("' in line
                                    or f'{subprocess_alias}.call(["' in line
                                    or f'{subprocess_alias}.call("' in line
                                    or f'{subprocess_alias}.check_call(["' in line
                                    or f'{subprocess_alias}.check_call("' in line
                                    or f'{subprocess_alias}.check_output(["' in line
                                    or f'{subprocess_alias}.check_output("' in line
                                    or f'{subprocess_alias}.Popen(["' in line
                                    or f'{subprocess_alias}.Popen("' in line
                                    or f'{subprocess_alias}.getstatusoutput("' in line
                                    or f'{subprocess_alias}.getoutput("' in line):
                                command = line.split('"')[1].replace('\n', '').split(' ')[0]
                            elif (f"{subprocess_alias}.run(['" in line
                                  or f"{subprocess_alias}.run('" in line
                                  or f"{subprocess_alias}.call(['" in line
                                  or f"{subprocess_alias}.call('" in line
                                  or f"{subprocess_alias}.check_call(['" in line
                                  or f"{subprocess_alias}.check_call('" in line
                                  or f"{subprocess_alias}.check_output(['" in line
                                  or f"{subprocess_alias}.check_output('" in line
                                  or f"{subprocess_alias}.Popen(['" in line
                                  or f"{subprocess_alias}.Popen('" in line
                                  or f"{subprocess_alias}.getstatusoutput('" in line
                                  or f"{subprocess_alias}.getoutput('" in line):
                                command = line.split("'")[1].replace('\n', '').split(' ')[0]
                            else:
                                # subprocess function
                                for func in subprocess_functions:
                                    if f'{func}(["' in line or f'{func}("' in line:
                                        command = line.split('"')[1].replace('\n', '').split(' ')[0]
                                    elif f"{func}(['" in line or f"{func}('" in line:
                                        command = line.split("'")[1].replace('\n', '').split(' ')[0]
                            self._analyze_command(command)

    def _print_modules(self):
        with open(os.path.join(self.path_to_project, self.requirements_file_name)) as f:
            for line in f:
                line = line.strip("==")
                module_name = line.split("==")[0]
                module_version = line.split("==")[1]
                print(f"{module_name}: {module_version}")
