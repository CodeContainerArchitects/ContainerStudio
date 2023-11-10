import subprocess
import os
import config as cfg

pip_packages = {
    'numpy': 'numpy',
    'pandas': 'pandas',
    'requests': 'requests',
    'matplotlib': 'matplotlib',
    'scipy': 'scipy',
    'scikit-learn': 'scikit-learn',
    'tensorflow': 'tensorflow',
    'torch': 'torch',
    'flask': 'flask',
    'django': 'django',
    'beautifulsoup4': 'beautifulsoup4',
    'sqlalchemy': 'sqlalchemy',
    'pyqt5': 'pyqt5',
    'pygame': 'pygame',
    'pytz': 'pytz',
    'pillow': 'pillow',
    'requests': 'requests',
    'networkx': 'networkx',
    'jinja2': 'jinja2',
    'flask-restful': 'flask-restful',
    'tornado': 'tornado',
    'openai-gpt-3': 'openai-gpt-3',
    'pymongo': 'pymongo',
    'pymysql': 'pymysql',
    'pytest': 'pytest',
    'nltk': 'nltk',
    'seaborn': 'seaborn',
    'folium': 'folium',
    'pymc3': 'pymc3',
    'flask-wtf': 'flask-wtf',
    'dash': 'dash',
    'dask': 'dask',
    'cx_oracle': 'cx_oracle',
    'bcrypt': 'bcrypt',
    'celery': 'celery',
    'pyarrow': 'pyarrow',
    'pyspark': 'pyspark',
    'plotly': 'plotly',
    'kafka-python': 'kafka-python',
    'fastapi': 'fastapi',
    'pytest-django': 'pytest-django',
    'pyodbc': 'pyodbc',
    "mypdf2": "PyPDF2",
    "click": "click"
}


apt_packages = {"git": "git",
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
    "krita": "krita",
    "sed": "sed",}

dummy_version = ['1.1.1', '1.1.2', '1.1.3', '2.0']
    
    
def get_package_versions(mode, package_name):
    if mode == "apt":
        version = ["latest"]
    else:
        output = subprocess.check_output(f"pip index versions {package_name} | tail -1 | cut -d ':' -f 2", shell=True)
        version = output.decode().strip().split(", ")
    return version


build_in_packages = [
    "chmod",
    "chown",
    "chroot",
    "cp",
    "dd",
    "df",
    "du",
    "lm",
    "ls",
    "mkdir",
    "mv",
    "rm",
    "rmdir",
    "rmdir",
    "touch",
    "basename",
    "cat",
    "comm",
    "cut",
    "dirname",
    "echo",
    "expand",
    "false",
    "fmt",
    "fold",
    "head",
    "join",
    "paste",
    "seq",
    "sleep",
    'sort',
    "split",
    "tail",
    "tee",
    "test",
    "tr",
    "true",
    "uniq",
    "wc",
    "yes",
    "date",
    "env",
    "groups",
    "hostname",
    "id",
    "nice",
    "pwd",
    "su",
    "uname",
    "who",
    "whoami"
]

python_versions = ['3.12', '3.11', '3.10', '3.9', '3.8', '3.7', '3.6', '3.5']

os_versions = ['debian:10', 'debian:11', 'debian:12','ubuntu:20.04', 'ubuntu:22.04', 'ubuntu:23.04']


def load_apt_to_dict(os_name):
    file_content = []
    parent_directory = cfg.path_to_project
    try:
        with open(f'{parent_directory}/modules_listings/apt/{os_name}.txt', 'r') as file:
            content = file.read()
            lines = content.split('\n')
            file_content = {line.strip(): line.strip() for line in lines if line.strip()}
    except FileNotFoundError:
        file_content = None

    return file_content


def load_pip_to_dict():
    file_content = []
    parent_directory = cfg.path_to_project
    try:
        with open(os.path.join(parent_directory, "modules_listings", "pip", "all_pip_packages.txt"), 'r') as file:
            content = file.read()
            lines = content.split('\n')
            file_content = {line.strip(): line.strip() for line in lines if line.strip()}
    except FileNotFoundError:
        file_content = None

    return file_content
