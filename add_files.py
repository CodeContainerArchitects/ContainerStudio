import tkinter.filedialog as fd
from tkinter import messagebox
import os
import shutil

parent_dir = ''
container_directory = "/data/"
files = []


# selects the directory where the files will be copied to and where the Dockerfile will be created
def select_working_directory():
    global parent_dir
    parent_dir = fd.askdirectory(mustexist=True, initialdir=os.path.expanduser('~'))
    if parent_dir != '':
        if os.path.isdir(parent_dir) == False:
            os.mkdir(parent_dir)


def get_working_directory():
    return parent_dir


# opens dialog to select files to be added to Dockerfile
def select_files(root, mode):
    global files
    if mode == 'file':
        files = fd.askopenfilenames(parent=root, title='Select files to be included', initialdir=os.path.expanduser('~'))
        files = root.splitlist(files)
    elif mode == 'dir':
        files = fd.askdirectory(mustexist=True, initialdir=os.path.expanduser('~'))
    
    if os.path.isdir(parent_dir) == False:
        os.mkdir(parent_dir)
    
    if len(files) > 0 and mode == 'file':
        copy_files_to_directory(path=parent_dir)
    elif files and mode == 'dir':
        # error if the folder chosen is the same as the working directory
        if files != parent_dir:
            copy_folder_to_directory(path=parent_dir)
        else:
            messagebox.showerror("Error", "You cannot add the working directory to the Dockerfile!")


def copy_files_to_directory(path):
    for file in files:
        # it overrides files with the same name
        shutil.copy2(file, path)


def copy_folder_to_directory(path):
    new_folder = os.path.basename(os.path.normpath(files))
    new_folder = os.path.join(path,new_folder)
    shutil.copytree(files, new_folder)
    
def delete_files_from_directory(rm_files):
    for file in rm_files:
        if os.path.isfile(file) == True:
            os.remove(file)
        elif os.path.isdir(file) == True:
            shutil.rmtree(file)

def copy_dir_to_container():
    files_to_container = []
    if os.path.isdir(parent_dir) == True and len(os.listdir(parent_dir)) > 0:
        for file in os.listdir(parent_dir):
            line = file + " " + container_directory + file
            files_to_container.append(line)
    return files_to_container