import os
import re

def _find_dockerfile(path):
    for root, dirs, files in os.walk(path):
        if 'Dockerfile' in files:
            return os.path.join(root, 'Dockerfile')
    return None

def _find_files(path, pattern):
    matching_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if pattern.match(file):
                relative_path = os.path.relpath(os.path.join(root, file), start=path)
                matching_files.append(relative_path)
    return matching_files

def get_dockerfile_path(path):
    pattern = re.compile(r".*Dockerfile.*")
    result = _find_files(path=path, pattern=pattern)
    if result:
        print(f"Found Dockerfiles at:")
        for i in range(0, len(result)):
            print(f'{i}. {result[i]}')
        print('Choose appropriate Dockerfile. To quit press x.\n')
        index = input()
        if index.isdigit():
            file_name = os.path.join('Project_files', result[int(index)])
            return file_name
        else:
            return None
    else:
        print("Dockerfile not found in the specified directory.")
        return None
    
def parse_dockerfile(dockerfile_path, apt_packages, pip_packages, run_commands,
                     env_variables, os, expose_ports, users, arguments,
                     entrypoint_commands, cmd_commands, shell_commands) :
    with open(dockerfile_path, 'r') as file:
        content = file.readlines()
    icontent = iter(content)    
    workdir_changed = False
    workdir_value = None
    os_selected = False
    for line in icontent:
        command = line.split()
        if command:
            if command[0] == "#":
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
            #print(whole_command)
            if 'ONBUILD' not in command and 'VOLUME' not in command:
                if 'FROM' in command and os_selected == False:
                    image = command[command.index('FROM')+1:command.index('FROM')+2]
                    if ':' in image[0]:
                        parts = image[0].split(':')
                        os["OS_image"] = parts[0]
                        os["OS_image_version"] = parts[1]
                    else:
                        os["OS_image"] = image[0]
                        os["OS_image_version"] = 'latest'
                    os_selected = True
                if 'MAINTAINER' in command:
                    continue # currently not supported
                if 'LABEL' in command:
                    continue # currently not supported
                if 'EXPOSE' in command:
                    expose_ports.append(whole_command)
                if 'USER' in command:
                    users.append(whole_command)
                if 'WORKDIR' in command:
                    workdir_changed = True
                    workdir_value = whole_command
                if 'ARG' in command:
                    arguments.append(whole_command)
                if 'ENTRYPOINT' in command:
                    entrypoint_commands.append(whole_command)
                if 'CMD' in command:
                    cmd_commands.append(whole_command)
                if 'STOPSIGNAL' in command:
                    continue # currently not supported
                if 'HEALTHCHECK' in command:
                    continue # currently not supported
                if 'SHELL' in command:
                    shell_commands.append(whole_command)
                if 'RUN' in command:                     
                    if 'apt' in command or 'apt-get' in command:
                        if 'install' in command:
                            apt_packages, rest_of_command = add_apt_packages(command, apt_packages)
                            if rest_of_command:
                                if workdir_changed:
                                    run_commands.append(workdir_value)
                                    workdir_changed = False
                                run_commands.append(" ".join(rest_of_command))
                    elif 'pip' in command:
                        if 'install' in command:
                            pip_packages, rest_of_command = add_pip_packages(command, pip_packages)
                            if rest_of_command:
                                if workdir_changed:
                                    run_commands.append(workdir_value)
                                    workdir_changed = False
                                run_commands.append(" ".join(rest_of_command))
                    else:
                        if workdir_changed:
                            run_commands.append(workdir_value)
                            workdir_changed = False
                        run_commands.append(whole_command)
                if 'ENV' in command:
                    env_variables.append(whole_command)
                if 'COPY' in command:
                    if workdir_changed:
                        workdir_changed = False
                    continue #TODO when COPY action will be implemented, this will be added in the future

    return apt_packages, pip_packages, run_commands, env_variables, os, expose_ports, users, arguments, entrypoint_commands, cmd_commands, shell_commands
    
def add_apt_packages(command, apt_packages):
    packages = command
    index = packages.index("install")
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
        
    rest_of_command = command
    if "apt" in rest_of_command:
        rest_of_command.remove("apt")
    if "apt-get" in rest_of_command: 
        rest_of_command.remove("apt-get")
    if "install" in rest_of_command:
        rest_of_command.remove("install")
        
    for word in packages:
        rest_of_command.remove(word)
        
    was_command = False
    for word in rest_of_command:
        if word == "RUN":
            continue
        if "-" in word:
            if not was_command:
                rest_of_command.remove(word)
        else:
            was_command = True
        
    if len(rest_of_command) == 1:
        rest_of_command = None
        
    pattern = '^-+.*'
    indexes = []
    for word in packages:
        if re.match(pattern, word):
            indexes.append(packages.index(word))
    for index in reversed(indexes):
        packages.remove(packages[index])
    
    for package in packages:
        if package not in apt_packages.keys():
            apt_packages[package] = package
            
    return apt_packages, rest_of_command

def add_pip_packages(command, pip_packages):
    packages = command
    index = packages.index("install")
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
        
    rest_of_command = command
    if "pip" in rest_of_command:
        rest_of_command.remove("pip")
    if "install" in rest_of_command:
        rest_of_command.remove("install")
    
    pattern = '^-+.*'
    indexes = []
    for word in packages:
        if re.match(pattern, word):
            indexes.append(packages.index(word))
    for index in reversed(indexes):
        packages.remove(packages[index])
        
    for word in packages:
        rest_of_command.remove(word)
        
    was_command = False
    for word in rest_of_command:
        if word == "RUN":
            continue
        if "-" in word:
            if not was_command:
                rest_of_command.remove(word)
        else:
            was_command = True
        
        
    if len(rest_of_command) == 1:
        rest_of_command = None
    
    pattern = re.compile(r".*requirements.*")
    for word in packages:
        if pattern.match(word):
            packages.remove(word)
    
    for package in packages:
        if package not in pip_packages.keys():
            pip_packages[package] = package
    return pip_packages, rest_of_command