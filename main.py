import jinja2
import subprocess
import tkinter as tk
from requirements_searching import use_requirements

pip_packages = {"jinja": "Jinja2",
               "mypdf2": "PyPDF2",
               "click": "click"}

apt_get_packages = {"git": "git",
                    "ansible":"ansible"}

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
template = environment.get_template("template-dockerfile.txt")

OS_image="ubuntu"
OS_image_version="latest"
message = "testing message 123"
path = '/home/ola/Desktop/test_files'
use_requirements, file_names = use_requirements(path=path)
content = template.render(OS_image=OS_image,
                          OS_image_version=OS_image_version,
                          packages_to_install=pip_packages.values(),
                          apt_get_packages=apt_get_packages.values(),
                          use_requirements=use_requirements,
                          file_names=file_names,
                          ranges=len(use_requirements))


with open("outputs/Dockerfile", "w") as file:
    file.write(content)

print(content)

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
