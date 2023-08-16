import tkinter.filedialog as fd
import os
import shutil

parent_dir = ""
path = ""
working_directory = "Dockerfile_files"
container_directory = "/files"
files = []

# selects the directory where the files will be copied to and where the Dockerfile will be created
def select_working_directory():
    global parent_dir
    parent_dir = fd.askdirectory(mustexist=True)
    
    if not parent_dir:
        parent_dir = os.getcwd()
        print(parent_dir)
    
    global path
    path = os.path.join(parent_dir, working_directory)
    if os.path.isdir(path) == False:
        os.mkdir(path)

def get_working_directory():
    return parent_dir

# opens dialog to select files to be added to Dockerfile
def select_files(root):
    global files
    files = fd.askopenfilenames(parent=root, title='Select files to be included')
    files = root.splitlist(files)
    if os.path.isdir(path) == True:
        if len(files) > 0:
            copy_files_to_directory(path=path)

def copy_files_to_directory(path):
    for file in files:
        # it overrides files with the same name
        shutil.copy2(file, path)

def copy_folder_to_dockerfile():
    if os.path.isdir(path) == True and len(os.listdir(path)) > 0:
        return f"{working_directory} {container_directory}"
    return None