import jinja2
import os
from CoreApp import CoreApp

class DockerComposeGenerator:
    def __init__(self, coreApp, project_name, projectTree):
        self.coreApp = coreApp
        self.environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
        self.template = self.environment.get_template("template-docker-compose.txt")
        self.project_name = project_name
        self.dockerfile_name = "Dockerfile"
        self.compose_name = "docker-compose.yml"
        self.compose_version = "3"
        self.context = projectTree.parent_dir
        self.restart = "always"
        
    def generate_compose(self):
        content = self.template.render(project_name=self.project_name,
                                       dockerfile_name=self.dockerfile_name,
                                       compose_version=self.compose_version,
                                       context=self.context,
                                       ports=self.coreApp.expose_ports,
                                       env_variables=self.coreApp.env_variables,
                                       restart=self.restart)
        
        with open(os.path.join(self.coreApp.get_project_root_dir(), self.compose_name), "w") as file:
            file.write(content)
        
        print(content)
