import tkinter.filedialog as fd
import os
import shutil

parent_dir = os.getcwd()
working_directory = "Dockerfile_files"
path = os.path.join(parent_dir, working_directory)
container_directory = "/files"
files = []

# selects the directory where the files will be copied to and where the Dockerfile will be created
def select_working_directory():
    global parent_dir
    parent_dir = fd.askdirectory(mustexist=True)
    
    global path
    path = os.path.join(parent_dir, working_directory)
    if os.path.isdir(path) == False:
        os.mkdir(path)

def get_working_directory():
    return parent_dir

# opens dialog to select files to be added to Dockerfile
def select_files(root, mode):
    global files
    if mode == 'file':
        files = fd.askopenfilenames(parent=root, title='Select files to be included')
        files = root.splitlist(files)
    elif mode == 'dir':
        files = fd.askdirectory(mustexist=True)
    
    if os.path.isdir(path) == False:
        os.mkdir(path)
    
    if len(files) > 0 and mode == 'file':
        copy_files_to_directory(path=path)
    elif files and mode == 'dir':
        copy_folder_to_directory(path=path)

def copy_files_to_directory(path):
    for file in files:
        # it overrides files with the same name
        shutil.copy2(file, path)
        
def copy_folder_to_directory(path):
    new_folder = os.path.basename(os.path.normpath(files))
    new_folder = os.path.join(path,new_folder)
    shutil.copytree(files, new_folder)

def copy_folder_to_dockerfile():
    if os.path.isdir(path) == True and len(os.listdir(path)) > 0:
        return f"{working_directory} {container_directory}"
    return None