import jinja2
import add_files
import os
from requirements_searching import use_requirements
from createUtils.package_listing import apt_packages, pip_packages
from existing_dockerfile import parse_dockerfile, get_dockerfile_path
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
        use_req, file_names = use_requirements(path=add_files.get_working_directory())
        copy_folder_to_dockerfile = add_files.copy_dir_to_container()
        
        dockerfile_path = get_dockerfile_path(path=add_files.get_working_directory())
        
        if dockerfile_path:
            dockerfile_path = os.path.join(add_files.get_working_directory(), dockerfile_path)
            parse_dockerfile(dockerfile_path=dockerfile_path,
                            apt_packages=self.coreApp.chosen_apt_packages,
                            pip_packages=self.coreApp.chosen_pip_packages,
                            run_commands=self.coreApp.run_commands,
                            env_variables=self.coreApp.env_variables,
                            os_docker=self.coreApp.OS_data,
                            expose_ports=self.coreApp.expose_ports,
                            users=self.coreApp.users,
                            arguments=self.coreApp.arguments,
                            entrypoint_commands=self.coreApp.entrypoint_commands,
                            cmd_commands=self.coreApp.cmd_commands,
                            shell_commands=self.coreApp.shell_commands,
                            maintainers=self.coreApp.maintainers,
                            volumes=self.coreApp.volumes,
                            labels=self.coreApp.labels,
                            stop_signals=self.coreApp.stop_signals,
                            healthchecks=self.coreApp.healthchecks,
                            images=self.coreApp.images,
                            files=self.dockerfile_files,
                            all_commands=self.coreApp.all_commands,
                            files_root_dir=self.coreApp.project_root_dir,
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
                                use_requirements=use_req,
                                file_names=file_names,
                                ranges=len(use_req),
                                copy_folder_to_dockerfile=copy_folder_to_dockerfile,
                                all_commands=self.coreApp.all_commands)

        filename = "Dockerfile"
        with open(os.path.join(add_files.get_working_directory(), filename), "w") as file:
            file.write(content)

        print(content)