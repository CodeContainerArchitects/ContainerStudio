import tkinter as tk
from ProjectTree import ProjectTree
from gui.TreeWindow import TreeWindow
from gui.ManageRequirementsWindow import ManageRequirementsWindow
from gui.GeneratorWindow import GeneratorWindow
from gui.PackageListWindow import PackageListWindow
from gui.AddAttributesWindow import AddAttributesWindow


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
        
        mainframe = tk.Frame(self, width=self.window_width, height=self.window_height)
        buttonframe = tk.Frame(mainframe)
        
        # select folder
        select_folder_button = tk.Button(buttonframe, text="Select folder",  command=lambda: self.select_working_directory())
        
        self.folder_name = "No folder selected."
        
        self.folder_label = tk.Label(buttonframe, text=self.folder_name, justify=tk.LEFT, width=25, padx = self.padding)
        
        # opens a new window
        self.project_tree_button = tk.Button(buttonframe, text="Show project tree", state=tk.DISABLED, command=lambda: self.open_tree_window())
        # manage requirements_button
        self.manage_requirements_button = tk.Button(buttonframe, text="Manage requirements", state=tk.DISABLED, command=lambda: self.open_manage_requirements_window())
        
        self.package_list_button = tk.Button(buttonframe, text="Select apt and pip packages", state=tk.DISABLED, command=lambda: self.open_packages_list_window())
        
        self.send_button = tk.Button(buttonframe, text = "Generate", state=tk.DISABLED, command=lambda:self.open_generate())
        
        self.add_attributes_button = tk.Button(buttonframe, text = "Customize Dockerfile Attributes", state=tk.DISABLED, command=lambda:self.open_add_attributes())
        exit_button = tk.Button(buttonframe, text = "Exit", command = self.destroy)
        
        mainframe.pack(side=tk.TOP)
        buttonframe.pack(expand=True)
        mainframe.pack_propagate(0)
        
        select_folder_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        self.folder_label.pack(pady=self.padding, side=tk.TOP)
        self.project_tree_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        self.manage_requirements_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        self.package_list_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        self.add_attributes_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        self.send_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        exit_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        
    def open_tree_window(self):
        tree_window = TreeWindow(self)
        # grab_set prevents user from interacting with main window and makes the tree window receive events
        tree_window.grab_set()

    def set_chosen_requirements(self, chosen_requirements, file_names, apt_packages, requirements_pip_packages):
        self.coreApp.set_chosen_requirements(chosen_requirements)
        self.coreApp.set_requirements_files_names(file_names)
        self.coreApp.subprocess_apt_packages = apt_packages
        self.coreApp.requirements_pip_packages = requirements_pip_packages

    def open_manage_requirements_window(self):
        manage_requirements_window = ManageRequirementsWindow(self, self.set_chosen_requirements)
        manage_requirements_window.grab_set()
        
    def open_packages_list_window(self):
        packages_list_window = PackageListWindow(self)
        packages_list_window.grab_set()
        
    def select_working_directory(self):
        self.projectTree.select_working_directory()
        working_directory = self.projectTree.get_working_directory()
        self.coreApp.set_project_root_dir(working_directory)
        self.folder_label['text'] = working_directory
        
        if working_directory != '' and self.project_tree_button['state'] == tk.DISABLED and self.manage_requirements_button['state'] == tk.DISABLED and self.send_button['state'] == tk.DISABLED and self.package_list_button['state'] == tk.DISABLED:
            self.project_tree_button['state'] = tk.NORMAL
            self.manage_requirements_button['state'] = tk.NORMAL
            self.send_button['state'] = tk.NORMAL
            self.package_list_button['state'] = tk.NORMAL
            self.add_attributes_button['state'] = tk.NORMAL
            
    def open_generate(self):
        self.generate_window = GeneratorWindow(self)
        self.generate_window.grab_set()
        
    def open_add_attributes(self):
        self.add_attributes_window = AddAttributesWindow(self)
        self.add_attributes_window.grab_set()
