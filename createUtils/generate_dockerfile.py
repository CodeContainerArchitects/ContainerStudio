import jinja2
import os
import add_files
from createUtils.package_listing import apt_packages, pip_packages
from existing_dockerfile import DockerfileParser
from CoreApp import CoreApp

class DockerfileGenerator:
    def __init__(self, coreApp):
        self.coreApp = coreApp
        self.environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
        self.template = self.environment.get_template("template-dockerfile.txt")
        self.files_not_found = []
        self.dockerfile_path = ""
        self.dockerfile_files = []

    def generate_dockerfile(self):
        copy_folder_to_dockerfile = add_files.copy_dir_to_container()
        
        self.coreApp.project_root_dir = add_files.get_working_directory()
        parser = DockerfileParser(self.coreApp)
        
        dockerfile_path = parser.get_dockerfile_path()
        
        if dockerfile_path:
            dockerfile_path = os.path.join(add_files.get_working_directory(), dockerfile_path)
            parser.parse_dockerfile(dockerfile_path=dockerfile_path,
                            files=self.dockerfile_files,
                            files_not_found=self.files_not_found)
            
            if self.files_not_found:
                print("Files not found:")
                for file in self.files_not_found:
                    print(file)
                print("Check if files are in the right directory or adjust their paths.")
                
        
        content = self.template.render(OS_image=self.coreApp.OS_data["OS_image"],
                                OS_image_version=self.coreApp.OS_data["OS_image_version"],
                                packages_to_install=self.coreApp.chosen_pip_packages,
                                apt_get_packages=self.coreApp.chosen_apt_packages,
                                use_requirements=self.coreApp.chosen_requirements,
                                file_names=self.coreApp.requirements_files_names,
                                ranges=len(self.coreApp.chosen_requirements),
                                copy_folder_to_dockerfile=copy_folder_to_dockerfile,
                                all_commands=self.coreApp.all_commands)

        filename = "Dockerfile"
        with open(os.path.join(add_files.get_working_directory(), filename), "w") as file:
            file.write(content)

        print(content)
