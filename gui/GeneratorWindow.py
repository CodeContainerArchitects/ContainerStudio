import tkinter as tk
from tkinter import ttk
from DockerfileParser import DockerfileParser
from createUtils.DockerfileGenerator import DockerfileGenerator
from createUtils.DockerComposeGenerator import DockerComposeGenerator
import os
import re
from createUtils.common_utils import _find_files
from tkinter import messagebox as messagebox
from tkinter.filedialog import asksaveasfile
from gui.FilesNotFoundWindow import FilesNotFoundWindow

class GeneratorWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.window_width = 600
        self.window_height = 400
        self.padding = 5
        
        self.title("Generate Files")
        center_x = int(parent.screen_width/2 - self.window_width / 2)
        center_y = int(parent.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        button_frame_upper = tk.Frame(self)
        search_for_dockerfile_button = tk.Button(button_frame_upper, text="Search for existing Dockerfile", command=lambda: self.search_for_dockerfile(parent))
        
        self.list_of_dockerfiles = tk.Listbox(self, height=6, selectmode=tk.SINGLE)
        label_for_list_of_dockerfiles = tk.Label(self, text="Found existing Dockerfiles: \n")
        
        button_frame_middle = tk.Frame(self)
        create_dockerfile_button = tk.Button(button_frame_middle, text="Create Dockerfile", command=lambda: self.create_dockerfile(parent))
        self.create_compose_button = tk.Button(button_frame_middle, text="Create docker-compose.yml", state=tk.DISABLED, command=lambda: self.create_compose(parent))
        
        button_frame_lower = tk.Frame(self)
        cancel_button = tk.Button(button_frame_lower, text="Exit", command=self.destroy)
        
        button_frame_upper.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        button_frame_middle.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        search_for_dockerfile_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        label_for_list_of_dockerfiles.pack(side=tk.TOP, fill='x')
        self.list_of_dockerfiles.pack(side=tk.LEFT, pady=self.padding, fill='both', expand=True)
        create_dockerfile_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        self.create_compose_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        
    def search_for_dockerfile(self, parent):
        pattern = re.compile(r".*Dockerfile.*")
        result = _find_files(path=parent.coreApp.project_root_dir, pattern=pattern)
        self.list_of_dockerfiles.delete(0, tk.END)
        if len(result) == 0:
            self.list_of_dockerfiles.insert(tk.END, "No Dockerfiles found")
        else:
            for file in result:
                self.list_of_dockerfiles.insert(tk.END, file)
        
    def create_dockerfile(self, parent):
        generator = DockerfileGenerator(parent.coreApp, parent.projectTree)
        dockerfile_selected = self.list_of_dockerfiles.curselection()
        if dockerfile_selected:
            dockerfile_index = dockerfile_selected[0]
            if dockerfile_index or dockerfile_index == 0:
                dockerfile_path = self.list_of_dockerfiles.get(dockerfile_index)
                generator.set_dockerfile_path(dockerfile_path)
                res=messagebox.askquestion("Copy Dockerfile", "Do you want to make a copy of selected Dockerfile?")
                if res == 'yes':
                    f = asksaveasfile(filetypes=[("All Files","*.*")], initialdir=parent.coreApp.project_root_dir, initialfile=dockerfile_path+"_copy")
                    if f is not None:
                        orig_file = open(os.path.join(parent.coreApp.project_root_dir, dockerfile_path), "r")
                        content = orig_file.read()
                        f.write(content)
                        orig_file.close()
                        f.close()
        generator.generate_dockerfile()
        if generator.files_not_found:
            filesNotFoundWindow = FilesNotFoundWindow(self, generator.files_not_found)
            filesNotFoundWindow.grab_set()
        self.create_compose_button.config(state=tk.NORMAL)
    
    def create_compose(self, parent):
        generator = DockerComposeGenerator(parent.coreApp, "test-project", parent.projectTree)
        generator.generate_compose()
