import tkinter as tk
import os
from tkinter import messagebox
from tkinter.messagebox import askyesno
from ProjectTree import ProjectTree
from gui.BasicConfigurationWindow import BasicConfigurationWindow
from gui.CheckboxWindow import CheckboxWindow
from gui.TreeWindow import TreeWindow
from gui.ManageRequirementsWindow import ManageRequirementsWindow
from gui.GeneratorWindow import GeneratorWindow
from gui.PackageListWindow import PackageListWindow
from gui.AddAttributesWindow import AddAttributesWindow
from Dumper import Dumper


class App(tk.Tk):
    def __init__(self, coreApp):
        super().__init__()
        
        self.coreApp = coreApp
        self.dump_file_name = ".dump_coreapp.json"
        self.dumper = Dumper(coreApp, self.dump_file_name)
        self.projectTree = ProjectTree(parent=self, dump_file_name=self.dump_file_name)
        
        # set properties of the window
        self.title("Code Container")
        
        self.window_width = 600
        self.window_height = 550
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 15
        
        center_x = int(self.screen_width/2 - self.window_width / 2)
        center_y = int(self.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.configure(background='#B9B4C7')
        
        mainframe = tk.Frame(self, width=self.window_width/2, height=self.window_height)
        
        # select folder
        select_folder_button = tk.Button(mainframe, text="Select folder",  command=lambda: self.select_working_directory())
        
        self.folder_name = "No folder selected."
        
        self.folder_label = tk.Label(mainframe, text=self.folder_name, justify=tk.LEFT, width=25, padx = self.padding)
        
        # opens a new window
        self.project_tree_button = tk.Button(mainframe, text="Show project tree", state=tk.DISABLED, command=lambda: self.open_tree_window())

        self.basic_configuration_button = tk.Button(mainframe, text="Basic configuration", state=tk.DISABLED, command=lambda: self.open_basic_configuration_window())

        self.manage_requirements_button = tk.Button(mainframe, text="Manage requirements", state=tk.DISABLED, command=lambda: self.open_manage_requirements_window())
        
        self.package_list_button = tk.Button(mainframe, text="Select apt and pip packages", state=tk.DISABLED, command=lambda: self.open_packages_list_window())

        self.resource_and_access_button = tk.Button(mainframe, text="Resource & Access Management", state=tk.DISABLED, command=lambda: self.open_resource_and_access_window())

        self.send_button = tk.Button(mainframe, text = "Generate", state=tk.DISABLED, command=lambda:self.open_generate())
        
        self.add_attributes_button = tk.Button(mainframe, text = "Customize Attributes", state=tk.DISABLED, command=lambda:self.open_add_attributes())
        exit_button = tk.Button(mainframe, text = "Exit", command = self.on_closing)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        mainframe.grid(row=0, column=0, sticky='nsew')
        mainframe.grid_propagate(True)
        
        for idx in range(0,5):
            mainframe.columnconfigure(idx, weight=1)
        
        for idx in range(0, 9):
            mainframe.rowconfigure(idx, weight=1)
        
        select_folder_button.grid(row = 0, column=2, sticky='nsew', pady = self.padding)
        self.folder_label.grid(row = 1, column=2, sticky='nsew', pady = self.padding)
        self.project_tree_button.grid(row = 2, column=2, sticky='nsew', pady = self.padding)
        self.basic_configuration_button.grid(row = 3, column=2, sticky='nsew', pady = self.padding)
        self.manage_requirements_button.grid(row = 4, column=2, sticky='nsew', pady = self.padding)
        self.package_list_button.grid(row = 5, column=2, sticky='nsew', pady = self.padding)
        self.add_attributes_button.grid(row = 6, column=2, sticky='nsew', pady = self.padding)
        self.resource_and_access_button.grid(row = 7, column=2, sticky='nsew', pady = self.padding)
        self.send_button.grid(row = 8, column=2, sticky='nsew', pady = self.padding)
        exit_button.grid(row = 9, column=2, sticky='nsew', pady = self.padding)
        
    def open_tree_window(self):
        tree_window = TreeWindow(self)
        # grab_set prevents user from interacting with main window and makes the tree window receive events
        tree_window.grab_set()

    def open_basic_configuration_window(self):
        basic_confguration_window = BasicConfigurationWindow(self, self.set_os_and_python)
        basic_confguration_window.grab_set()
            
    def set_os_and_python(self, os_name, os_version, python_version):
        self.coreApp.OS_data["OS_image"] = os_name
        self.coreApp.OS_data["OS_image_version"] = os_version
        self.coreApp.python_version = python_version
        self.check_os_and_python()
        
    def check_os_and_python(self):
        if self.coreApp.OS_data and self.coreApp.python_version:
            self.manage_requirements_button['state'] = tk.NORMAL
            self.send_button['state'] = tk.NORMAL
            self.package_list_button['state'] = tk.NORMAL
            self.add_attributes_button['state'] = tk.NORMAL
            self.resource_and_access_button['state'] = tk.NORMAL

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
        
        if os.path.isfile(os.path.join(working_directory, self.dumper.file_name)):
            answer = askyesno(title="Found data from previous session!", message="Do you want to import settings from previous session?")
            if answer:
                self.dumper.import_coreapp(working_directory)
            else:
                self.coreApp.set_project_root_dir(working_directory)
        else:
            self.coreApp.set_project_root_dir(working_directory)
        self.folder_label['text'] = working_directory
        
        if working_directory != '' and self.project_tree_button['state'] == tk.DISABLED and self.manage_requirements_button['state'] == tk.DISABLED and self.send_button['state'] == tk.DISABLED and self.package_list_button['state'] == tk.DISABLED:
            self.project_tree_button['state'] = tk.NORMAL
            self.basic_configuration_button['state'] = tk.NORMAL
            self.check_os_and_python()

    def suggestions(self):
        tk.messagebox.showinfo(title="Suggestions", message="Suggestions")

    def open_generate(self):
        generate_window = GeneratorWindow(parent=self, suggestions_function=self.suggestions)
        generate_window.grab_set()
        
    def open_add_attributes(self):
        add_attributes_window = AddAttributesWindow(self)
        add_attributes_window.grab_set()

    def save_resource_and_access_window(self, checkboxes):
        for item, checked in checkboxes:
            print(f"{item}: {checked}")
            self.coreApp.resources_and_access_management[item] = checked.get()

    def open_resource_and_access_window(self):
        open_resource_and_access_window = CheckboxWindow(parent=self, title="Resource & Access Management", elements=self.coreApp.resources_and_access_management, callback=self.save_resource_and_access_window, callback1=self.suggestions)
        open_resource_and_access_window.grab_set()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            path = self.coreApp.get_project_root_dir()
            if path:
                self.dumper.export_coreapp(path)
            self.destroy()
