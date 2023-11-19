import jinja2
import os
from DockerfileParser import DockerfileParser
import config as cfg


class DockerfileGenerator:
    def __init__(self, coreApp, projectTree):
        self.coreApp = coreApp
        self.projectTree = projectTree
        self.environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(cfg.path_to_project, "templates")), trim_blocks=True, lstrip_blocks=True)
        
        if self.coreApp.get_template_version() == 1:
            self.template = self.environment.get_template("template-dockerfile-copy.txt")
        elif self.coreApp. get_template_version() == 2:
            self.template = self.environment.get_template("template-dockerfile-apt.txt")

        self.files_not_found = []
        self.dockerfile_path = ""
        self.dockerfile_files = []
        
    def set_dockerfile_path(self, path):
        self.dockerfile_path = path

    def generate_dockerfile(self):
        #copy_folder_to_dockerfile = self.projectTree.copy_dir_to_container()
        self.projectTree.use_dockerignore()
        external_lists_added = False
        external_packages_added = False
        if self.coreApp.external_lists_links is not None:
            external_lists_added = True
        if self.coreApp.external_lists_packages is not None:
            external_packages_added = True
        
        
        res_apt_packages = self.coreApp.chosen_apt_packages | self.coreApp.subprocess_apt_packages
        content = self.template.render(OS_image=self.coreApp.OS_data["OS_image"],
                                       OS_image_version=self.coreApp.OS_data["OS_image_version"],
                                       python_version=self.coreApp.python_version,
                                       update_pip=self.coreApp.resources_and_access_management["Pip update"],
                                       packages_to_install=self.coreApp.chosen_pip_packages,
                                       apt_get_packages=res_apt_packages,
                                       use_requirements=self.coreApp.chosen_requirements,
                                       file_names=self.coreApp.requirements_files_names,
                                       ranges=len(self.coreApp.chosen_requirements),
                                       env_variables=self.coreApp.env_variables,
                                       ports=self.coreApp.expose_ports,
                                       all_commands=self.coreApp.all_commands,
                                       entry_point=self.coreApp.entry_point,
                                       commands_before_files=self.coreApp.commands_before_files,
                                       commands_after_files=self.coreApp.commands_after_files,
                                       volumes=self.coreApp.volumes,
                                       external_lists_added=external_lists_added,
                                       external_lists=self.coreApp.external_lists_links,
                                       external_packages_added=external_packages_added,
                                       external_packages=self.coreApp.external_lists_packages)

        filename = "Dockerfile"
        with open(os.path.join(self.coreApp.get_project_root_dir(), filename), "w") as file:
            file.write(content)

        print(content)
