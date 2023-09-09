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
            file_name = result[int(index)]
            return file_name
        else:
            return None
    else:
        print("Dockerfile not found in the specified directory.")
        return None
    
def parse_dockerfile(dockerfile_path, apt_packages, pip_packages, run_commands,
                     env_variables, os_docker, expose_ports, users, arguments,
                     entrypoint_commands, cmd_commands, shell_commands,
                     maintainers, volumes, labels, stop_signals, healthchecks,
                     images, files, all_commands, files_root_dir, files_not_found) :
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
            #print(whole_command)
            if 'ONBUILD' not in command:
                if 'FROM' in command:
                    if os_selected:
                        image = command[command.index('FROM')+1:command.index('FROM')+2]
                        if ':' in image[0]:
                            parts = image[0].split(':')
                            os_docker["OS_image"] = parts[0]
                            os_docker["OS_image_version"] = parts[1]
                        else:
                            os_docker["OS_image"] = image[0]
                            os_docker["OS_image_version"] = 'latest'
                        os_selected = True
                    else:
                        all_commands.append(whole_command)
                        images.append(whole_command)
                if 'MAINTAINER' in command:
                    all_commands.append(whole_command)
                    maintainers.append(whole_command)
                if 'VOLUME' in command:
                    all_commands.append(whole_command)
                    volumes.append(whole_command)
                if 'LABEL' in command:
                    all_commands.append(whole_command)
                    labels.append(whole_command)
                if 'EXPOSE' in command:
                    expose_ports.append(whole_command)
                    all_commands.append(whole_command)
                if 'USER' in command:
                    users.append(whole_command)
                    all_commands.append(whole_command)
                if 'WORKDIR' in command:
                    all_commands.append(whole_command)
                if 'ARG' in command:
                    arguments.append(whole_command)
                    all_commands.append(whole_command)
                if 'ENTRYPOINT' in command:
                    entrypoint_commands.append(whole_command)
                    all_commands.append(whole_command)
                if 'CMD' in command:
                    cmd_commands.append(whole_command)
                    all_commands.append(whole_command)
                if 'STOPSIGNAL' in command:
                    all_commands.append(whole_command)
                    stop_signals.append(whole_command)
                if 'HEALTHCHECK' in command:
                    all_commands.append(whole_command)
                    healthchecks.append(whole_command)
                if 'SHELL' in command:
                    shell_commands.append(whole_command)
                    all_commands.append(whole_command)
                if 'RUN' in command:                     
                    if 'apt' in command or 'apt-get' in command:
                        if 'install' in command:
                            apt_packages, rest_of_command = add_apt_packages(command, apt_packages)
                            if rest_of_command:
                                run_commands.append(" ".join(rest_of_command))
                                all_commands.append(" ".join(rest_of_command))
                    elif 'pip' in command:
                        if 'install' in command:
                            pip_packages, rest_of_command = add_pip_packages(command, pip_packages)
                            if rest_of_command:
                                run_commands.append(" ".join(rest_of_command))
                                all_commands.append(" ".join(rest_of_command))
                    else:
                        run_commands.append(whole_command)
                        all_commands.append(whole_command)
                if 'ENV' in command:
                    env_variables.append(whole_command)
                    all_commands.append(whole_command)
                if 'COPY' in command:
                    files.append(whole_command)
                    all_commands.append(whole_command)
                    file_names = command[command.index('COPY')+1:]
                    file_names.remove(file_names[-1])
                    for file_name in file_names:
                        if file_name[0] != '-' and (file_name[0] != '.' or len(file_name) > 1 ):
                            file_found = False                       
                            for root, dirs, files in os.walk(files_root_dir):
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
                    all_commands.append(whole_command)
                    file_names = command[command.index('ADD')+1:]
                    file_names.remove(file_names[-1])
                    for file_name in file_names:
                        if file_name[0] != '-' and (file_name[0] != '.' or len(file_name) > 1 ):
                            file_found = False                       
                            for root, dirs, files in os.walk(files_root_dir):
                                if file_name in files:
                                    file_found = True
                                    break
                            if not file_found:
                                files_not_found.append(file_name)
                

    return apt_packages, pip_packages, run_commands, env_variables, os, expose_ports, users, arguments, entrypoint_commands, cmd_commands, shell_commands
    
def add_apt_packages(command, apt_packages):
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
        if package not in apt_packages:
            apt_packages.append(package)
            
    last_index = command.index(packages[-1])
    rest_of_command = command[:first_index-1] + command[last_index+1:]
    
    if len(rest_of_command) == 1:
        rest_of_command = None
            
    return apt_packages, rest_of_command

def add_pip_packages(command, pip_packages):
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
        if package not in pip_packages:
            pip_packages.append(package)
            
    last_index = command.index(packages[-1])
    rest_of_command = command[:first_index-1] + command[last_index+1:]
    
    if len(rest_of_command) == 1:
        rest_of_command = None
    
    return pip_packages, rest_of_command