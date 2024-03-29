import os.path

from createUtils.common_utils import delete_from_file


class CoreApp:
    def __init__(self):
        self.OS_data = {}
        self.run_commands = []
        self.env_variables = {}
        self.expose_ports = {}
        self.users = []
        self.arguments = []
        self.entrypoint_commands = []
        self.cmd_commands = []
        self.shell_commands = []
        self.maintainers = []
        self.volumes = {}
        self.labels = []
        self.stop_signals = []
        self.healthchecks = []
        self.images = []
        self.all_commands = []
        self.chosen_pip_packages = {}
        self.chosen_apt_packages = {}
        self.subprocess_apt_packages = {}
        self.requirements_pip_packages = {}
        self.project_root_dir = ""
        self.dockerfile_filename = ""
        self.chosen_requirements = []
        self.requirements_files_names = []
        self.operating_systems = ""
        self.python_version = ""
        self.template_version = None
        self.entry_point = ""
        self.commands_before_files = []
        self.commands_after_files = []
        self.container_directory = "/data/"
        self.apt_packages = {}
        self.pip_packages = {}
        self.external_lists_links = []
        self.external_lists_packages = []
        self.resources_and_access_management = {"Sharing graphics card resources": 0, "Display sharing": 0, "Sharing a sound card": 0, "Pip update": 0}

    def get_OS_data(self):
        return self.OS_data

    def set_OS_data(self, value):
        self.OS_data = value

    def get_run_commands(self):
        return self.run_commands

    def set_run_commands(self, value):
        self.run_commands = value

    def get_env_variables(self):
        return self.env_variables

    def set_env_variables(self, value):
        self.env_variables = value

    def get_expose_ports(self):
        return self.expose_ports

    def set_expose_ports(self, value):
        self.expose_ports = value

    def get_users(self):
        return self.users

    def set_users(self, value):
        self.users = value

    def get_arguments(self):
        return self.arguments

    def set_arguments(self, value):
        self.arguments = value

    def get_entrypoint_commands(self):
        return self.entrypoint_commands

    def set_entrypoint_commands(self, value):
        self.entrypoint_commands = value

    def get_cmd_commands(self):
        return self.cmd_commands

    def set_cmd_commands(self, value):
        self.cmd_commands = value

    def get_shell_commands(self):
        return self.shell_commands

    def set_shell_commands(self, value):
        self.shell_commands = value

    def get_maintainers(self):
        return self.maintainers

    def set_maintainers(self, value):
        self.maintainers = value

    def get_volumes(self):
        return self.volumes

    def set_volumes(self, value):
        self.volumes = value

    def get_labels(self):
        return self.labels

    def set_labels(self, value):
        self.labels = value

    def get_stop_signals(self):
        return self.stop_signals

    def set_stop_signals(self, value):
        self.stop_signals = value

    def get_healthchecks(self):
        return self.healthchecks

    def set_healthchecks(self, value):
        self.healthchecks = value

    def get_images(self):
        return self.images

    def set_images(self, value):
        self.images = value

    def get_all_commands(self):
        return self.all_commands

    def set_all_commands(self, value):
        self.all_commands = value

    def get_chosen_pip_packages(self):
        return self.chosen_pip_packages | self.requirements_pip_packages

    def set_chosen_pip_packages(self, value):
        self.chosen_pip_packages = value
        
    def add_chosen_pip_package(self, name, version):
        if name not in self.chosen_pip_packages.keys():
            self.chosen_pip_packages[name] = version
            
    def delete_chosen_pip_packages(self, values):
        for value in values:
            name = value.split(" ")[0]
            if name in self.chosen_pip_packages.keys():
                self.chosen_pip_packages.pop(name)
            elif name in self.requirements_pip_packages.keys():
                self.requirements_pip_packages.pop(name)

        # delete also if selected is from requirements file
        values = [val.split(" ")[0] for val in values]
        for i in range(0, len(self.chosen_requirements)):
            delete_from_file(file_path=os.path.join(self.project_root_dir, self.chosen_requirements[i]), content=values)

    def get_chosen_apt_packages(self):
        return self.chosen_apt_packages | self.subprocess_apt_packages

    def set_chosen_apt_package(self, value):
        self.chosen_apt_packages = value
        
    def add_chosen_apt_package(self, name, version):
        if name not in self.chosen_apt_packages.keys():
            self.chosen_apt_packages[name] = version
            
    def delete_chosen_apt_packages(self, values):
        for value in values:
            name = value.split(" ")[0]
            if name in self.chosen_apt_packages.keys():
                self.chosen_apt_packages.pop(name)
            elif name in self.subprocess_apt_packages.keys():
                self.subprocess_apt_packages.pop(name)

    def add_apt_package(self, value):
        self.chosen_apt_packages.extend(value)

    def get_project_root_dir(self):
        return self.project_root_dir

    def set_project_root_dir(self, value):
        self.project_root_dir = value

    def get_dockerfile_filename(self):
        return self.dockerfile_filename

    def set_dockerfile_filename(self, value):
        self.dockerfile_filename = value

    def get_chosen_requirements(self):
        return self.chosen_requirements

    def set_chosen_requirements(self, value):
        self.chosen_requirements = value

    def get_requirements_files_names(self):
        return self.requirements_files_names

    def set_requirements_files_names(self, value):
        self.requirements_files_names = value

    def get_operating_system(self):
        return self.operating_systems

    def get_python_version(self):
        return self.python_version
    
    def set_template_version(self, value):
        self.template_version = value
    
    def get_template_version(self):
        return self.template_version
