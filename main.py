import jinja2
import subprocess
import tkinter as tk
import add_files
import os

def generate_dockerfile():
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
    copy_folder_to_dockerfile = add_files.copy_folder_to_dockerfile()
    content = template.render(OS_image=OS_image,
                            OS_image_version=OS_image_version,
                            packages_to_install=pip_packages.values(),
                            apt_get_packages=apt_get_packages.values(),
                            copy_folder_to_dockerfile=copy_folder_to_dockerfile)

    filename = "Dockerfile"
    with open(os.path.join(add_files.get_working_directory(), filename), "w") as file:
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

#select folder 
select_folder_button = tk.Button(root, text = "Select folder", command = lambda:add_files.select_working_directory())

# uploading files
choose_file_button = tk.Button(root, text = "Choose file", command = lambda:add_files.select_files(root,mode='file'))
choose_folder_button = tk.Button(root, text = "Choose folder", command = lambda:add_files.select_files(root, mode='dir'))


send_button = tk.Button(root, text = "Generate Dockerfile", command=lambda:generate_dockerfile())
exit_button = tk.Button(root, text = "Exit", command = root.destroy)

select_folder_button.pack()
choose_file_button.pack()
choose_folder_button.pack()
send_button.pack()
exit_button.pack()

root.mainloop()