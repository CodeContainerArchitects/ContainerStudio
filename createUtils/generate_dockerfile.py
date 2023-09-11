import jinja2
import add_files
from createUtils.package_listing import apt_packages, pip_packages
from existing_dockerfile import *


def generate_dockerfile(chosen_requirements, file_names, chosen_pip_packages=[], chosen_apt_packages=[]):

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
    
    copy_folder_to_dockerfile = add_files.copy_dir_to_container()
    
    dockerfile_path = get_dockerfile_path(path=add_files.get_working_directory())
    
    if dockerfile_path:
        dockerfile_path = os.path.join(add_files.get_working_directory(), dockerfile_path)
        files_root_dir=add_files.get_working_directory()
        parse_dockerfile(dockerfile_path=dockerfile_path,
                        apt_packages=chosen_apt_packages,
                        pip_packages=chosen_pip_packages,
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
            
    
    content = template.render(OOS_image=OS_data["OS_image"],
                              OS_image_version=OS_data["OS_image_version"],
                              packages_to_install=chosen_pip_packages,
                              apt_get_packages=chosen_apt_packages,
                              use_requirements=chosen_requirements,
                              file_names=file_names,
                              ranges=len(chosen_requirements),
                              copy_folder_to_dockerfile=copy_folder_to_dockerfile,
                              all_commands=all_commands)

    filename = "Dockerfile"
    with open(os.path.join(add_files.get_working_directory(), filename), "w") as file:
        file.write(content)

    print(content)