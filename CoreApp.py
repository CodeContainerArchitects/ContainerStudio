from createUtils.package_listing import apt_packages, pip_packages

class CoreApp:
    def __init__(self):
        self.OS_data = {
            "OS_image": "ubuntu",
            "OS_image_version": "latest"
        }
        self.run_commands = []
        self.env_variables = []
        self.expose_ports = []
        self.users = []
        self.arguments = []
        self.entrypoint_commands = []
        self.cmd_commands = []
        self.shell_commands = []
        self.maintainers = []
        self.volumes = []
        self.labels = []
        self.stop_signals = []
        self.healthchecks = []
        self.images = []
        self.all_commands = []
        self.chosen_pip_packages = [pip_packages["numpy"], pip_packages["pandas"]]
        self.chosen_apt_packages = [apt_packages["curl"], apt_packages["vim"]]
        self.project_root_dir = ""
        self.dockerfile_filename = ""