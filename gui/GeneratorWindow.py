import tkinter as tk
from tkinter import ttk
from DockerfileParser import DockerfileParser
import os
import re
from createUtils.common_utils import _find_files

class GeneratorWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.window_width = 600
        self.window_height = 400
        self.padding = 5
        
        self.parser = DockerfileParser(parent.coreApp)
        
        self.title("Generate Files")
        center_x = int(parent.screen_width/2 - self.window_width / 2)
        center_y = int(parent.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        button_frame_upper = tk.Frame(self)
        search_for_dockerfile_button = tk.Button(button_frame_upper, text="Search for existing Dockerfile", command=lambda: self.search_for_dockerfile(parent))
        
        self.list_of_dockerfiles = tk.Listbox(self, height=6, selectmode=tk.SINGLE)
        label_for_list_of_dockerfiles = tk.Label(self, text="Found existing Dockerfiles: \n")
        
        button_frame_middle = tk.Frame(self)
        create_dockerfile_button = tk.Button(button_frame_middle, text="Create Dockerfile", command=lambda: self.create_dockerfile())
        create_compose_button = tk.Button(button_frame_middle, text="Create docker-compose.yml", state=tk.DISABLED, command=lambda: self.create_compose())
        
        button_frame_lower = tk.Frame(self)
        apply_button = tk.Button(button_frame_lower, text="Save", command=lambda: self.apply())
        cancel_button = tk.Button(button_frame_lower, text="Cancel", command=self.destroy)
        
        button_frame_upper.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        button_frame_middle.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        search_for_dockerfile_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        label_for_list_of_dockerfiles.pack(side=tk.TOP, fill='x')
        self.list_of_dockerfiles.pack(side=tk.LEFT, pady=self.padding, fill='both', expand=True)
        create_dockerfile_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        create_compose_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        
    def search_for_dockerfile(self, parent):
        pattern = re.compile(r".*Dockerfile.*")
        result = _find_files(path=parent.coreApp.project_root_dir, pattern=pattern)
        
    def create_dockerfile(self):
        pass
    
    def create_compose(self):
        pass
    
    def apply(self):
        pass
