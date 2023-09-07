import jinja2
import tkinter as tk
import add_files
import os
from requirements_searching import use_requirements
from createUtils.package_listing import apt_packages, pip_packages

def generate_dockerfile():
    

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
    template = environment.get_template("template-dockerfile.txt")

    OS_image="ubuntu"
    OS_image_version="latest"
    message = "testing message 123"
    use_req, file_names = use_requirements(path=os.path.join(add_files.get_working_directory(), 'Project_files'))
    copy_folder_to_dockerfile = add_files.copy_folder_to_dockerfile()
    
    chosen_pip_packages = [pip_packages["numpy"], pip_packages["pandas"]]
    chosen_apt_packages = [apt_packages["curl"], apt_packages["vim"]]
    
    content = template.render(OS_image=OS_image,
                              OS_image_version=OS_image_version,
                              packages_to_install=chosen_pip_packages,
                              apt_get_packages=chosen_apt_packages,
                              use_requirements=use_req,
                              file_names=file_names,
                              ranges=len(use_req),
                              copy_folder_to_dockerfile=copy_folder_to_dockerfile)

    filename = "Dockerfile"
    with open(os.path.join(add_files.get_working_directory()+"/outputs", filename), "w") as file:
        file.write(content)

    print(content)