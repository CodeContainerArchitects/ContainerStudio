import tkinter as tk
from ProjectTree import ProjectTree
from createUtils.DockerfileGenerator import DockerfileGenerator
from createUtils.package_listing import pip_packages, apt_packages
from gui.TreeWindow import TreeWindow
from gui.ManageRequirementsWindow import ManageRequirementsWindow
from gui.GeneratorWindow import GeneratorWindow

class App(tk.Tk):
    def __init__(self, coreApp):
        super().__init__()
        
        self.coreApp = coreApp
        self.projectTree = ProjectTree()

        # set properties of the window
        self.title("Code Container")
        
        self.window_width = 600
        self.window_height = 500
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 5
        
        center_x = int(self.screen_width/2 - self.window_width / 2)
        center_y = int(self.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.configure(background='#B9B4C7')
        
        self.project_files_folder = "Project_files"
        
        mainframe = tk.Frame(self, width=self.window_width, height=self.window_height)
        buttonframe = tk.Frame(mainframe)
        
        # select folder
        select_folder_button = tk.Button(buttonframe, text="Select folder",  command=lambda: self.select_working_directory())
        # opens a new window
        self.project_tree_button = tk.Button(buttonframe, text="Show project tree", state=tk.DISABLED, command=lambda: self.open_tree_window())
        # manage requirements_button
        self.manage_requirements_button = tk.Button(buttonframe, text="Manage requirements", state=tk.DISABLED, command=lambda: self.open_manage_requirements_window())
        
        pip_packages_label = tk.Label(buttonframe, text="Select pip packages")
        pip_packages_listvar = tk.StringVar(value=list(pip_packages.values()))
        self.pip_packages_listbox = tk.Listbox(buttonframe, listvariable=pip_packages_listvar, height=5, selectmode='multiple')
        
        self.pip_packages_listbox.bind('<<ListboxSelect>>', self.set_chosen_pip_packages)
        
        apt_packages_label = tk.Label(buttonframe, text="Select apt packages")
        apt_packages_listvar = tk.StringVar(value=list(apt_packages.values()))
        self.apt_packages_listbox = tk.Listbox(buttonframe, listvariable=apt_packages_listvar, height=5, selectmode='multiple')
        
        self.apt_packages_listbox.bind('<<ListboxSelect>>', self.set_chosen_apt_packages)
        
        self.send_button = tk.Button(buttonframe, text = "Generate", state=tk.DISABLED, command=lambda:self.open_generate())
        exit_button = tk.Button(buttonframe, text = "Exit", command = self.destroy)
        
        mainframe.pack(side=tk.TOP)
        buttonframe.pack(expand=True)
        mainframe.pack_propagate(0)
        
        select_folder_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        self.project_tree_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        self.manage_requirements_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        pip_packages_label.pack(pady=self.padding, side=tk.TOP, fill='x')
        self.pip_packages_listbox.pack(pady=self.padding, side=tk.TOP, fill='x')
        apt_packages_label.pack(pady=self.padding, side=tk.TOP, fill='x')
        self.apt_packages_listbox.pack(pady=self.padding, side=tk.TOP, fill='x')
        self.send_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        exit_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        
    def set_chosen_pip_packages(self, event):
        selected_pip_indices = self.pip_packages_listbox.curselection()
        chosen_pip_packages = [self.pip_packages_listbox.get(index) for index in selected_pip_indices]
        self.coreApp.set_chosen_pip_packages(chosen_pip_packages)

    def set_chosen_apt_packages(self, event):
        selected_apt_indices = self.apt_packages_listbox.curselection()
        chosen_apt_packages = [self.apt_packages_listbox.get(index) for index in selected_apt_indices]
        self.coreApp.set_chosen_apt_packages(chosen_apt_packages)
        
    def open_tree_window(self):
        tree_window = TreeWindow(self)
        # grab_set prevents user from interacting with main window and makes the tree window receive events
        tree_window.grab_set()

    def get_chosen_requirements(self, chosen_requirements, file_names):
        self.coreApp.set_chosen_requirements(chosen_requirements)
        self.coreApp.set_requirements_files_names(file_names)

    def open_manage_requirements_window(self):
        manage_requirements_window = ManageRequirementsWindow(self, self.get_chosen_requirements)
        manage_requirements_window.grab_set()
        
    def select_working_directory(self):
        self.projectTree.select_working_directory()
        working_directory = self.projectTree.get_working_directory()
        self.coreApp.set_project_root_dir(working_directory)
        
        if working_directory != '' and self.project_tree_button['state'] == tk.DISABLED and self.manage_requirements_button['state'] == tk.DISABLED and self.send_button['state'] == tk.DISABLED:
            self.project_tree_button['state'] = tk.NORMAL
            self.manage_requirements_button['state'] = tk.NORMAL
            self.send_button['state'] = tk.NORMAL
            
    def open_generate(self):
        self.generate_window = GeneratorWindow(self)
        self.generate_window.grab_set()
