import os
import re
import shutil
from createUtils.common_utils import _find_files

class DockerfileParser:
    def __init__(self, coreApp):
        self.coreApp = coreApp


    def get_dockerfile_path(self):
        pattern = re.compile(r".*Dockerfile.*")
        result = _find_files(path=self.coreApp.project_root_dir, pattern=pattern)
        if result:
            print(f"Found Dockerfiles at:")
            for i in range(0, len(result)):
                print(f'{i}. {result[i]}')
            print('Choose appropriate Dockerfile, which will be used as a base. To quit press x.\n')
            index = input()
            if index.isdigit():
                file_name = result[int(index)]
                print("Do you want to copy selected Dockerfile (y/n)?")
                option = input()
                if option == 'y':
                    print("Enter the name of the copy of selected Dockerfile: ")
                    copy_file_name = input()
                    while os.path.exists(os.path.join(self.coreApp.project_root_dir, copy_file_name)):
                        print("File arleady exists. Choose another file name.\n")
                        copy_file_name = input()
                    shutil.copyfile(os.path.join(self.coreApp.project_root_dir, file_name), os.path.join(self.coreApp.project_root_dir, copy_file_name))
                return file_name
            else:
                return None
        else:
            print("Dockerfile not found in the specified directory.")
            return None
        
    def parse_dockerfile(self, dockerfile_path, files, files_not_found) :
        with open(dockerfile_path, 'r') as file:
            content = file.readlines()
        icontent = iter(content)    
        os_selected = False
        for line in icontent:
            command = line.split()
            if command:
                while command[0] == "#":
                    command = next(icontent).split()
                if "#" in command:
                    index = command.index("#")
                    command = command[:index]
                while command[-1] == "\\":
                    next_line = next(icontent).split()
                    while next_line[0] == "#":
                        next_line = next(icontent).split()
                    if "#" in next_line:
                        index = next_line.index("#")
                        next_line = next_line[:index]
                    for word in next_line:
                        command.append(word)
                while "\\" in command:
                    command.remove("\\")
                whole_command = " ".join(command)
                if 'ONBUILD' not in command:
                    if 'FROM' in command:
                        if os_selected:
                            image = command[command.index('FROM')+1:command.index('FROM')+2]
                            if ':' in image[0]:
                                parts = image[0].split(':')
                                self.coreApp.os_docker["OS_image"] = parts[0]
                                self.coreApp.os_docker["OS_image_version"] = parts[1]
                            else:
                                self.coreApp.os_docker["OS_image"] = image[0]
                                self.coreApp.os_docker["OS_image_version"] = 'latest'
                            os_selected = True
                        else:
                            self.coreApp.all_commands.append(whole_command)
                            self.coreApp.images.append(whole_command)
                    if 'MAINTAINER' in command:
                        self.coreApp.all_commands.append(whole_command)
                        self.coreApp.maintainers.append(whole_command)
                    if 'VOLUME' in command:
                        self.coreApp.all_commands.append(whole_command)
                        self.coreApp.volumes.append(whole_command)
                    if 'LABEL' in command:
                        self.coreApp.all_commands.append(whole_command)
                        self.coreApp.labels.append(whole_command)
                    if 'EXPOSE' in command:
                        container_port = whole_command.split()[1]
                        host_port = f"-{container_port}"
                        self.coreApp.expose_ports[host_port] = container_port
                        self.coreApp.all_commands.append(whole_command)
                    if 'USER' in command:
                        self.coreApp.users.append(whole_command)
                        self.coreApp.all_commands.append(whole_command)
                    if 'WORKDIR' in command:
                        self.coreApp.all_commands.append(whole_command)
                    if 'ARG' in command:
                        self.coreApp.arguments.append(whole_command)
                        self.coreApp.all_commands.append(whole_command)
                    if 'ENTRYPOINT' in command:
                        self.coreApp.entrypoint_commands.append(whole_command)
                        self.coreApp.all_commands.append(whole_command)
                    if 'CMD' in command:
                        self.coreApp.cmd_commands.append(whole_command)
                        self.coreApp.all_commands.append(whole_command)
                    if 'STOPSIGNAL' in command:
                        self.coreApp.ll_commands.append(whole_command)
                        self.coreApp.stop_signals.append(whole_command)
                    if 'HEALTHCHECK' in command:
                        self.coreApp.all_commands.append(whole_command)
                        self.coreApp.healthchecks.append(whole_command)
                    if 'SHELL' in command:
                        self.coreApp.shell_commands.append(whole_command)
                        self.coreApp.all_commands.append(whole_command)
                    if 'RUN' in command:                     
                        if 'apt' in command or 'apt-get' in command:
                            if 'install' in command:
                                self.coreApp.chosen_apt_packages, rest_of_command = self.add_apt_packages(command, self.coreApp.chosen_apt_packages)
                                if rest_of_command:
                                    self.coreApp.run_commands.append(" ".join(rest_of_command))
                                    self.coreApp.all_commands.append(" ".join(rest_of_command))
                        elif 'pip' in command:
                            if 'install' in command:
                                self.coreApp.chosen_pip_packages, rest_of_command = self.add_pip_packages(command, self.coreApp.chosen_pip_packages)
                                if rest_of_command:
                                    self.coreApp.run_commands.append(" ".join(rest_of_command))
                                    self.coreApp.all_commands.append(" ".join(rest_of_command))
                        else:
                            self.coreApp.run_commands.append(whole_command)
                            self.coreApp.all_commands.append(whole_command)
                    if 'ENV' in command:
                        key = whole_command.split()[1].split('=')[0]
                        value = whole_command.split()[1].split('=')[1]
                        self.coreApp.env_variables[key] = value
                        self.coreApp.all_commands.append(whole_command)
                    if 'COPY' in command:
                        files.append(whole_command)
                        self.coreApp.all_commands.append(whole_command)
                        file_names = command[command.index('COPY')+1:]
                        file_names.remove(file_names[-1])
                        for file_name in file_names:
                            if file_name[0] != '-' and (file_name[0] != '.' or len(file_name) > 1 ):
                                file_found = False                       
                                for root, dirs, files in os.walk(self.coreApp.project_root_dir):
                                    if file_name in files:
                                        file_found = True
                                        break
                                    if file_name in dirs:
                                        file_found = True
                                        break
                                if not file_found:
                                    files_not_found.append(file_name)
                    if 'ADD' in command:
                        files.append(whole_command)
                        self.coreApp.all_commands.append(whole_command)
                        file_names = command[command.index('ADD')+1:]
                        file_names.remove(file_names[-1])
                        for file_name in file_names:
                            if file_name[0] != '-' and (file_name[0] != '.' or len(file_name) > 1 ):
                                file_found = False                       
                                for root, dirs, files in os.walk(self.coreApp.project_root_dir):
                                    if file_name in files:
                                        file_found = True
                                        break
                                if not file_found:
                                    files_not_found.append(file_name)
                    
        
    def add_apt_packages(self, command, apt_packages):
        packages = command
        index = packages.index("install")
        first_index = index
        packages = packages[index+1:]
        if "&&" in packages:
            index = packages.index("&&")
            packages = packages[:index]
        if "||" in packages:
            index = packages.index("||")
            packages = packages[:index]
        if ";" in packages:
            index = packages.index(";")
            packages = packages[:index]
        if ">" in packages:
            index = packages.index(">")
            packages = packages[:index]
        if "<" in packages:
            index = packages.index("<")
            packages = packages[:index]
        if ">>" in packages:
            index = packages.index(">>")
            packages = packages[:index]
        if "<<" in packages:
            index = packages.index("<<")
            packages = packages[:index]
        if "|" in packages:
            index = packages.index("|")
            packages = packages[:index]
        if "&" in packages:
            index = packages.index("&")
            packages = packages[:index]
        if "!" in packages:
            index = packages.index("!")
            packages = packages[:index]
            
        pattern = '^-+.*'
        indexes = []
        for word in packages:
            if re.match(pattern, word):
                indexes.append(packages.index(word))
        for index in reversed(indexes):
            packages.remove(packages[index])
        
        for package in packages:
            if package not in apt_packages.keys():
                apt_packages[package] = "latest"
                
        if packages:
            last_index = command.index(packages[-1])
            rest_of_command = command[:first_index-1] + command[last_index+1:]
        
        if len(rest_of_command) == 1:
            rest_of_command = None
                
        return apt_packages, rest_of_command

    def add_pip_packages(self, command, pip_packages):
        packages = command
        index = packages.index("install")
        first_index = index
        packages = packages[index+1:]
        if "&&" in packages:
            index = packages.index("&&")
            packages = packages[:index]
        if "||" in packages:
            index = packages.index("||")
            packages = packages[:index]
        if ";" in packages:
            index = packages.index(";")
            packages = packages[:index]
        if ">" in packages:
            index = packages.index(">")
            packages = packages[:index]
        if "<" in packages:
            index = packages.index("<")
            packages = packages[:index]
        if ">>" in packages:
            index = packages.index(">>")
            packages = packages[:index]
        if "<<" in packages:
            index = packages.index("<<")
            packages = packages[:index]
        if "|" in packages:
            index = packages.index("|")
            packages = packages[:index]
        if "&" in packages:
            index = packages.index("&")
            packages = packages[:index]
        if "!" in packages:
            index = packages.index("!")
            packages = packages[:index]
        
        pattern = '^-+.*'
        indexes = []
        for word in packages:
            if re.match(pattern, word):
                indexes.append(packages.index(word))
        for index in reversed(indexes):
            packages.remove(packages[index])
            
        pattern = re.compile(r".*requirements.*")
        for word in packages:
            if pattern.match(word):
                packages.remove(word)
        
        for package in packages:
            if package not in pip_packages.keys():
                pip_packages[package] = "latest"
                
        if packages:
            last_index = command.index(packages[-1])
            rest_of_command = command[:first_index-1] + command[last_index+1:]
        else:
            rest_of_command = command
        
        if len(rest_of_command) == 1:
            rest_of_command = None
        
        return pip_packages, rest_of_command
