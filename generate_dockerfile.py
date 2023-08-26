from requirements_searching import use_requirements
from add_files import copy_folder_to_dockerfile, get_working_directory
import os
import jinja2

def generate_dockerfile():
    pip_packages = {"jinja": "Jinja2",
               "mypdf2": "PyPDF2",
               "click": "click"}

    apt_get_packages = {"git": "git",
                        "ansible":"ansible",
                        "nano": "nano",
                        "vim": "vim",
                        "htop": "htop",
                        "curl": "curl",
                        "wget": "wget",
                        "python3": "python3",
                        "python3-pip": "python3-pip",
                        "apache2": "apache2",
                        "nginx": "nginx",
                        "mysql-server": "mysql-server",
                        "postgresql": "postgresql",
                        "php": "php",
                        "nodejs": "nodejs",
                        "npm": "npm",
                        "openjdk-11-jdk": "openjdk-11-jdk",
                        "gcc": "gcc",
                        "g++": "g++",
                        "make": "make",
                        "virtualbox": "virtualbox",
                        "docker": "docker",
                        "docker-compose": "docker-compose",
                        "ansible": "ansible",
                        "wireshark": "wireshark",
                        "openssh-server": "openssh-server",
                        "tmux": "tmux",
                        "screen": "screen",
                        "emacs": "emacs",
                        "gparted": "gparted",
                        "ffmpeg": "ffmpeg",
                        "vlc": "vlc",
                        "libreoffice": "libreoffice",
                        "gimp": "gimp",
                        "inkscape": "inkscape",
                        "blender": "blender",
                        "audacity": "audacity",
                        "rhythmbox": "rhythmbox",
                        "transmission": "transmission",
                        "clamav": "clamav",
                        "fail2ban": "fail2ban",
                        "ufw": "ufw",
                        "nmap": "nmap",
                        "lynx": "lynx",
                        "elinks": "elinks",
                        "irssi": "irssi",
                        "mutt": "mutt",
                        "transmission-cli": "transmission-cli",
                        "samba": "samba",
                        "nfs-common": "nfs-common",
                        "cifs-utils": "cifs-utils",
                        "sshfs": "sshfs",
                        "zip": "zip",
                        "unzip": "unzip",
                        "rar": "rar",
                        "unrar": "unrar",
                        "gnome-terminal": "gnome-terminal",
                        "xfce4-terminal": "xfce4-terminal",
                        "konsole": "konsole",
                        "terminator": "terminator",
                        "ranger": "ranger",
                        "midnight-commander": "midnight-commander",
                        "synaptic": "synaptic",
                        "filezilla": "filezilla",
                        "putty": "putty",
                        "xrdp": "xrdp",
                        "remmina": "remmina",
                        "pidgin": "pidgin",
                        "hexchat": "hexchat",
                        "teamviewer": "teamviewer",
                        "wine": "wine",
                        "clamtk": "clamtk",
                        "xclip": "xclip",
                        "meld": "meld",
                        "bleachbit": "bleachbit",
                        "gufw": "gufw",
                        "gdebi": "gdebi",
                        "keepassxc": "keepassxc",
                        "transmission-gtk": "transmission-gtk",
                        "qbittorrent": "qbittorrent",
                        "deluge": "deluge",
                        "hexedit": "hexedit",
                        "radare2": "radare2",
                        "netcat": "netcat",
                        "john": "john",
                        "hydra": "hydra",
                        "nikto": "nikto",
                        "aircrack-ng": "aircrack-ng",
                        "ettercap-graphical": "ettercap-graphical",
                        "tcpdump": "tcpdump",
                        "openssh-client": "openssh-client",
                        "rsync": "rsync",
                        "ffmpeg": "ffmpeg",
                        "audacity": "audacity",
                        "darktable": "darktable",
                        "krita": "krita",}

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
    template = environment.get_template("template-dockerfile.txt")

    OS_image="ubuntu"
    OS_image_version="latest"
    message = "testing message 123"
    path = '/home/ola/Desktop/test_files'
    use_req, file_names = use_requirements(path=path)
    copy_folder_dockerfile = copy_folder_to_dockerfile()
    content = template.render(OS_image=OS_image,
                              OS_image_version=OS_image_version,
                              packages_to_install=pip_packages.values(),
                              apt_get_packages=apt_get_packages.values(),
                              use_requirements=use_req,
                              file_names=file_names,
                              ranges=len(use_req),
                              copy_folder_dockerfile=copy_folder_dockerfile)

    filename = "Dockerfile"
    with open(os.path.join(get_working_directory(), filename), "w") as file:
        file.write(content)

    print(content)