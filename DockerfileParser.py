import os
import re
import shutil
from createUtils.common_utils import _find_files

class DockerfileParser:
    def __init__(self, coreApp):
        self.coreApp = coreApp
        
    def parse_dockerfile(self, dockerfile_path, files, files_not_found) :
        with open(dockerfile_path, 'r') as file:
            content = file.readlines()
        icontent = iter(content)    
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
                        pass
                    if 'MAINTAINER' in command:
                        pass
                    if 'VOLUME' in command:
                        pass
                    if 'LABEL' in command:
                        pass
                    if 'EXPOSE' in command:
                        container_port = whole_command.split()[1]
                        host_port = f"-{container_port}"
                        self.coreApp.expose_ports[host_port] = container_port
                    if 'USER' in command:
                        pass
                    if 'WORKDIR' in command:
                        pass
                    if 'ARG' in command:
                        pass
                    if 'ENTRYPOINT' in command:
                        self.coreApp.entry_point = whole_command.replace("ENTRYPOINT ", "")
                    if 'CMD' in command:
                        pass
                    if 'STOPSIGNAL' in command:
                        pass
                    if 'HEALTHCHECK' in command:
                        pass
                    if 'SHELL' in command:
                        pass
                    if 'RUN' in command:                     
                        if 'apt' in command or 'apt-get' in command:
                            if 'install' in command:
                                self.coreApp.chosen_apt_packages = self.add_apt_packages(command, self.coreApp.chosen_apt_packages)
                        elif 'pip' in command:
                            if 'install' in command:
                                self.coreApp.chosen_pip_packages = self.add_pip_packages(command, self.coreApp.chosen_pip_packages)
                        else:
                            pass
                    if 'ENV' in command:
                        if '=' in whole_command:
                            key = whole_command.split()[1].split('=')[0]
                            value = whole_command.split()[1].split('=')[1]
                            self.coreApp.env_variables[key] = value
                        else:
                            key = whole_command.split()[1]
                            value = whole_command.split()[2]
                            self.coreApp.env_variables[key] = value
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
                
        return apt_packages

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
                pip_packages[package] = "package from requirements"
                
        return pip_packages
