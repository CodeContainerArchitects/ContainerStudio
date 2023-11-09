import tkinter.filedialog as fd
from tkinter import messagebox
import os
import shutil


class ProjectTree:
    def __init__(self, parent, dump_file_name):
        self.parent_dir = ""
        self.parent = parent
        self.files = []  
        self.dump_file_name = dump_file_name

    # selects the directory where the files will be copied to and where the Dockerfile will be created
    def select_working_directory(self):
        try:
            self.parent_dir = fd.askdirectory(mustexist=True, initialdir=os.path.expanduser('~'))
        except:
            messagebox.showerror("Error", "You have to select a folder to continue.")
            pass
        
        if self.parent_dir == "":
            messagebox.showerror("Error", "You have to select a folder to continue.")

    def get_working_directory(self):
        return self.parent_dir

    # opens dialog to select files to be added to Dockerfile
    def select_files(self, root, mode):
        global files
        try:
            if mode == 'file':
                files = fd.askopenfilenames(parent=root, title='Select files to be included', initialdir=os.path.expanduser('~'))
                files = root.splitlist(files)
            elif mode == 'dir':
                files = fd.askdirectory(mustexist=True, initialdir=os.path.expanduser('~'))
            
            if os.path.isdir(self.parent_dir) == False:
                os.mkdir(self.parent_dir)
        
            if len(files) > 0 and mode == 'file':
                self.copy_files_to_directory(path=self.parent_dir)
            elif files and mode == 'dir':
                # error if the folder chosen is the same as the working directory
                if files != self.parent_dir:
                    self.copy_folder_to_directory(path=self.parent_dir)
                else:
                    messagebox.showerror("Error", "You cannot add the working directory to the Dockerfile!")
        except:
            messagebox.showerror("Error", "You have to select a viable file or folder.")
            pass

    def copy_files_to_directory(self, path):
        for file in files:
            # it overrides files with the same name
            shutil.copy2(file, path)

    def copy_folder_to_directory(self, path):
        new_folder = os.path.basename(os.path.normpath(files))
        new_folder = os.path.join(path,new_folder)
        shutil.copytree(files, new_folder)
        
    def delete_files_from_directory(self, rm_files):
        for file in rm_files:
            if os.path.isfile(file) == True:
                os.remove(file)
            elif os.path.isdir(file) == True:
                shutil.rmtree(file)

    def copy_dir_to_container(self):
        files_to_container = []
        if os.path.isdir(self.parent_dir) == True and len(os.listdir(self.parent_dir)) > 0:
            for file in os.listdir(self.parent_dir):
                if file != self.dump_file_name:
                    line = file + " " + self.parent.coreApp.container_directory + file
                    files_to_container.append(line)
        return files_to_container
