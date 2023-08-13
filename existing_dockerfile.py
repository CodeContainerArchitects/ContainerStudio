import os
import re


def _find_dockerfile(path):
    for root, dirs, files in os.walk(path):
        if 'Dockerfile' in files:
            return os.path.join(root, 'Dockerfile')
    return None


def get_dockerfile_path(path):
    result = _find_dockerfile(path=path)
    if result:
        print(f"Found Dockerfile at: {result}")
        user_choice = input('Do you want to use found Dockerfile as a base? y/n \n')
        if user_choice == 'y' or user_choice == 'yes':
            return result
        else:
            return None
    else:
        return None
    
def parse_dockerfile(dockerfile_path, apt_packages, pip_packages):
    with open(dockerfile_path, 'r') as file:
        content = file.readlines()
    icontent = iter(content)
    for line in icontent:
        if 'RUN' in line:
            command = line.split()
            while command[-1] == "\\":
                next_line = next(icontent).split()
                for word in next_line:
                    command.append(word)
            while "\\" in command:
                command.remove("\\")
            #print(command)                      
            if 'apt' in command or 'apt-get' in command:
                if 'install' in command:
                    apt_packages = add_apt_packages(command, apt_packages)
            if 'pip' in command:
                if 'install' in command:
                    pip_packages = add_pip_packages(command, pip_packages)
            
            
            
            #print(line)
            # if 'apt' in line or 'apt-get' in line:
            #     if 'install' in line or "\\" in line:
            #         apt_packages.append(line)
            # if 'pip' in line:
            #     if 'install' in line:
            #         pip_packages.append(line)
    return apt_packages, pip_packages
    
def add_apt_packages(command, apt_packages):
    packages = command
    index = packages.index("install")
    packages = packages[index+1:]
    if "&&" in packages:
        index = packages.index("&&")
        packages = packages[:index]
    pattern = '^-+.*'
    indexes = []
    for word in packages:
        if re.match(pattern, word):
            indexes.append(packages.index(word))
    for index in reversed(indexes):
        packages.remove(packages[index])
    print(packages)
    
    for package in packages:
        if package not in apt_packages.keys():
            apt_packages[package] = package
    return apt_packages

def add_pip_packages(command, pip_packages):
    packages = command
    index = packages.index("install")
    packages = packages[index+1:]
    if "&&" in packages:
        index = packages.index("&&")
        packages = packages[:index]
    pattern = '^-+.*'
    indexes = []
    for word in packages:
        if re.match(pattern, word):
            indexes.append(packages.index(word))
    for index in reversed(indexes):
        packages.remove(packages[index])
    print(packages)
    
    if "requirements.txt" in packages:
        packages.remove("requirements.txt")
    
    for package in packages:
        if package not in pip_packages.keys():
            pip_packages[package] = package
    return pip_packages