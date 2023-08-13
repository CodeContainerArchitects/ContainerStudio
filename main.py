import jinja2
import subprocess
import tkinter as tk
from existing_dockerfile import *

pip_packages = {"jinja": "Jinja2",
               "mypdf2": "PyPDF2",
               "click": "click"}

apt_get_packages = {"git": "git",
                    "ansible":"ansible"}

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
template = environment.get_template("template-dockerfile.txt")

path="/home/weektor/test-repos/Auto-GPT"
dockerfile_path = get_dockerfile_path(path=path)
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
if dockerfile_path:
    parse_dockerfile(dockerfile_path=dockerfile_path,
                     apt_packages=apt_get_packages,
                     pip_packages=pip_packages,
                     run_commands=run_commands,
                     env_variables=env_variables,
                     os=OS_data,
                     expose_ports=expose_ports,
                     users=users,
                     arguments=arguments,
                     entrypoint_commands=entrypoint_commands,
                     cmd_commands=cmd_commands,
                     shell_commands=shell_commands)
    
# print(apt_get_packages)
# print(pip_packages)
# print(OS_data["OS_image"])
# print(OS_data["OS_image_version"])
# print(run_commands)
# print(env_variables)
# print(expose_ports)
# print(users)
# print(arguments)
# print(entrypoint_commands)
# print(cmd_commands)
# print(shell_commands)

message = "testing message 123"
content = template.render(OS_image=OS_data["OS_image"],
                          OS_image_version=OS_data["OS_image_version"],
                          packages_to_install=pip_packages.values(),
                          apt_get_packages=apt_get_packages.values(),
                          run_commands=run_commands,
                          env_variables=env_variables,
                          expose_ports=expose_ports,
                          users=users,
                          arguments=arguments,
                          entrypoint_commands=entrypoint_commands,
                          cmd_commands=cmd_commands,
                          shell_commands=shell_commands)


with open("outputs/Dockerfile", "w") as file:
    file.write(content)

#print(content)

print("Try to run Dockerfile")
#subprocess.call(["bash", "scripts/dockerfile_runner.sh"])

root = tk.Tk()

# set properties of the window
root.title("Code Container")

window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# textbox for inputting text
textbox = tk.Text(root, height=5, width=70, pady = 10)
label = tk.Label(root, text = "Type a message")

# uploading files
#upload_file_button = tk.Button(root, text = "Upload file", command = lambda:upload_file())
file_label = tk.Label(text='Choose a file')

send_button = tk.Button(root, text = "Send", )
exit_button = tk.Button(root, text = "Exit", command = root.destroy)

label.pack()
textbox.pack()
#upload_file_button.pack()
file_label.pack()
send_button.pack()
exit_button.pack()

root.mainloop()