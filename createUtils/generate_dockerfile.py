import jinja2
import tkinter as tk
import add_files
import os
from requirements_searching import use_requirements
from createUtils.package_listing import apt_packages, pip_packages
from existing_dockerfile import *

def generate_dockerfile():
    

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
    template = environment.get_template("template-dockerfile.txt")
    
    OS_data= {
        "OS_image": "ubuntu",
        "OS_image_version": "latest"
    }
    run_commands = []
    env_variables = []
    expose_ports = []
    users=[]
    arguments=[]
    entrypoint_commands = []
    cmd_commands = []
    shell_commands = []
    maintainers = []
    volumes = []
    labels = []
    stop_signals = []
    healthchecks = []
    images = []
    dockerfile_files = []
    all_commands = []
    files_not_found = []
    
    use_req, file_names = use_requirements(path=os.path.join(add_files.get_working_directory(), 'Project_files'))
    copy_folder_to_dockerfile = add_files.copy_folder_to_dockerfile()
    dockerfile_path = get_dockerfile_path(path=os.path.join(add_files.get_working_directory(), 'Project_files'))
    
    if dockerfile_path:
        dockerfile_path = os.path.join(add_files.get_working_directory(), dockerfile_path)
        files_root_dir=os.path.join(add_files.get_working_directory(), 'Project_files')
        parse_dockerfile(dockerfile_path=dockerfile_path,
                        apt_packages=apt_packages,
                        pip_packages=pip_packages,
                        run_commands=run_commands,
                        env_variables=env_variables,
                        os_docker=OS_data,
                        expose_ports=expose_ports,
                        users=users,
                        arguments=arguments,
                        entrypoint_commands=entrypoint_commands,
                        cmd_commands=cmd_commands,
                        shell_commands=shell_commands,
                        maintainers=maintainers,
                        volumes=volumes,
                        labels=labels,
                        stop_signals=stop_signals,
                        healthchecks=healthchecks,
                        images=images,
                        files=dockerfile_files,
                        all_commands=all_commands,
                        files_root_dir=files_root_dir,
                        files_not_found=files_not_found)
        
        if files_not_found:
            print("Files not found:")
            for file in files_not_found:
                print(file)
            print("Check if files are in the right directory or adjust their paths.")
            
        print("Please, choose which Dockerfile should be used:")
        print("1. Dockerfile from the project:", dockerfile_path)
        print("2. Generated Dockerfile:", os.path.join(add_files.get_working_directory(), 'Dockerfile'))
        print("3. None (exit)")
        index=0
        while index not in ['1', '2', '3']:
            index = input()
        if index == '1':
            return
        elif index == '3':
            exit()

    OS_image="ubuntu"
    OS_image_version="latest"
    message = "testing message 123"
    use_req, file_names = use_requirements(path=os.path.join(add_files.get_working_directory(), 'Project_files'))
    copy_folder_to_dockerfile = add_files.copy_dir_to_container()
    
    chosen_pip_packages = [pip_packages["numpy"], pip_packages["pandas"]]
    chosen_apt_packages = [apt_packages["curl"], apt_packages["vim"]]
    
    content = template.render(OOS_image=OS_data["OS_image"],
                              OS_image_version=OS_data["OS_image_version"],
                              packages_to_install=chosen_pip_packages,
                              apt_get_packages=chosen_apt_packages,
                              use_requirements=use_req,
                              file_names=file_names,
                              ranges=len(use_req),
                              copy_folder_to_dockerfile=copy_folder_to_dockerfile,
                              all_commands=all_commands)

    filename = "Dockerfile"
    with open(os.path.join(add_files.get_working_directory()+"/outputs", filename), "w") as file:
        file.write(content)

    print(content)