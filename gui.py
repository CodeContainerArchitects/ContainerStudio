import re
import tkinter as tk
from tkinter import ttk
from add_files import select_files, select_working_directory, get_working_directory, delete_files_from_directory
from createUtils.generate_dockerfile import DockerfileGenerator
from requirements_searching import _find_files
from ModuleSearcher import ModuleSearcher
from createUtils.package_listing import pip_packages, apt_packages
from CoreApp import CoreApp
import os


class EntryWindow(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)

        # self variables
        self.file_name = ""
        self.callback = callback
        self.directory = get_working_directory()

        # window properties
        self.window_width = 600
        self.window_height = 400
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 5

        center_x = int(self.screen_width / 2 - self.window_width / 2)
        center_y = int(self.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        self.title("Entry requirements file name")

        label_for_entry = tk.Label(self, text="Enter requirements file name: ")
        self.entry = tk.Entry(self, textvariable=tk.StringVar())
        self.label_for_message = tk.Label(self, text="")
        buttons_frame = tk.Frame(self)
        ok_button = tk.Button(buttons_frame, text="Ok", command=lambda: self.ok_button_clicked())
        cancel_button = tk.Button(buttons_frame, text="Cancel", command=lambda: self.cancel_button_clicked())

        label_for_entry.pack(side=tk.TOP, pady=self.padding, fill=tk.BOTH)
        self.entry.pack(side=tk.TOP, pady=self.padding, fill=tk.BOTH)
        self.label_for_message.pack(side=tk.TOP, pady=self.padding, fill=tk.BOTH)
        buttons_frame.pack(side=tk.BOTTOM, pady=self.padding, fill=tk.BOTH)
        ok_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cancel_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def get_user_input(self):
        return self.file_name

    def destroy_object(self):
        self.destroy()

    def ok_button_clicked(self):
        if os.path.exists(os.path.join(self.directory, self.entry.get())):
            self.label_for_message.config(text="File already exists. Choose another name.", fg="red")
        else:
            self.label_for_message.config(text=f"Creating {self.file_name} file...", fg="green")
            self.update_idletasks()
            self.file_name = self.entry.get()
            self.callback(self.file_name)
            self.destroy()

    def cancel_button_clicked(self):
        self.destroy()


class ManageRequirementsWindow(tk.Toplevel):
    def __init__(self, parent, get_chosen_requirements):
        super().__init__(parent)

        # variables
        self.file_names = None
        self.chosen_requirements = None
        self.callback = get_chosen_requirements

        # window properties
        self.window_width = 600
        self.window_height = 400
        self.padding = 5
        self.directory = get_working_directory()

        self.title("Manage requirements")
        center_x = int(parent.screen_width / 2 - self.window_width / 2)
        center_y = int(parent.screen_height / 2 - self.window_height / 2)

        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        # create upper buttons
        button_frame_upper = tk.Frame(self)
        search_for_requirements_button = tk.Button(button_frame_upper, text="Search for requirements", command=lambda: self.search_for_requirements())
        create_requirements_button = tk.Button(button_frame_upper, text="Create requirements", command=lambda: self.create_requirements())

        # create list of requirements
        self.list_of_requirements = tk.Listbox(self, height=6, selectmode=tk.EXTENDED)

        # create label for list of requirements
        label_for_list_of_requirements = tk.Label(self, text="Founded requirements files: \n")

        # create lower buttons
        button_frame_lower = tk.Frame(self)
        apply_button = tk.Button(button_frame_lower, text="Apply", command=lambda: self.apply())
        cancel_button = tk.Button(button_frame_lower, text="Cancel", command=self.destroy)

        button_frame_upper.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        search_for_requirements_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        create_requirements_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        label_for_list_of_requirements.pack(side=tk.TOP, fill='x')
        self.list_of_requirements.pack(side=tk.LEFT, pady=self.padding, fill='both', expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

    def search_for_requirements(self):
        result = _find_files(path=self.directory, pattern=re.compile(r".*requirements.*"))
        self.list_of_requirements.delete(0, tk.END)
        if len(result) == 0:
            self.list_of_requirements.insert(tk.END, "No requirements files founded")
        else:
            for file in result:
                self.list_of_requirements.insert(tk.END, file)

    def create_requirements(self):
        def callback_create_requirements(file_name):
            if file_name != '':
                module_searcher = ModuleSearcher(path_to_project=self.directory, file_name=file_name)
                module_searcher.get_modules()
                self.search_for_requirements()
        entry_window = EntryWindow(self, callback_create_requirements)
        entry_window.grab_set()

    def apply(self):
        self.chosen_requirements = []
        for i in self.list_of_requirements.curselection():
            self.chosen_requirements.append(self.list_of_requirements.get(i))
        self.file_names = [os.path.split(file)[-1] for file in self.chosen_requirements]
        self.callback(self.chosen_requirements, self.file_names)
        self.destroy()


class TreeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.window_width = 600
        self.window_height = 400
        self.padding = 5
        
        self.title("Project directory tree")
        center_x = int(parent.screen_width/2 - self.window_width / 2)
        center_y = int(parent.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        treeframe = tk.Frame(self)
        
        self.treeview = ttk.Treeview(treeframe,height=15, show='tree')
        scrollbar = ttk.Scrollbar(treeframe, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        self.directory = get_working_directory()
        self.treeview.heading('#0', text='Dir:' + self.directory, anchor='w')
        
        self.build_tree()
        
        buttonframe = tk.Frame(self)
        
        # uploading files
        choose_file_button = tk.Button(buttonframe, text="Choose file", command=lambda: self.add_files(parent,mode='file'))
        choose_folder_button = tk.Button(buttonframe, text="Choose folder", command=lambda: self.add_files(parent, mode='dir'))
        delete_items_button = tk.Button(buttonframe, text="Delete selected items", command=lambda: self.delete_selected_items())
        exit_button = tk.Button(buttonframe, text="Exit", command=self.destroy)
        
        scrollbar.pack(side="right", fill="y")
        self.treeview.pack(fill='both')
        treeframe.pack(side=tk.TOP, fill = 'both')
        choose_file_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        choose_folder_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        delete_items_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        exit_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        buttonframe.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
    def build_tree(self):
        path = os.path.abspath(self.directory)
        node = self.treeview.insert('', 'end', text=path, open=True)
        self.traverse_dir(node, path)
    
    def traverse_dir(self, parent, path):
        for dir in os.listdir(path):
            full_path = os.path.join(path, dir)
            isdir = os.path.isdir(full_path)
            id = self.treeview.insert(parent, 'end', text=dir, open=False)
            if isdir:
                self.traverse_dir(id, full_path)
    
    def update_tree(self):
        # clear all items in the tree
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        self.build_tree()
        
    def delete_selected_items(self):
        selected_items = []
        for item in self.treeview.selection():
            parent_iid = self.treeview.parent(item)
            node = []
            while parent_iid!= '':
                node.insert(0, self.treeview.item(parent_iid)["text"])
                parent_iid = self.treeview.parent(parent_iid)
            i = self.treeview.item(item, "text")
            path = os.path.join(*node, i)
            selected_items.append(path)
            
        # print(selected_items)
        delete_files_from_directory(selected_items)
        self.update_tree()
    
    def add_files(self, root, mode):
        select_files(root, mode)
        self.update_tree()


class App(tk.Tk):
    def __init__(self, coreApp):
        super().__init__()
        
        self.coreApp = coreApp
        self.dockerfile_generator = DockerfileGenerator(coreApp)

        # variables
        #self.chosen_requirements = []
        #self.file_names = []
        #self.chosen_pip_packages = []
        #self.chosen_apt_packages = []
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
        
        self.send_button = tk.Button(buttonframe, text = "Generate Dockerfile", state=tk.DISABLED, command=lambda:self.dockerfile_generator.generate_dockerfile())
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
        select_working_directory()
        working_directory = get_working_directory()
        
        if working_directory != '' and self.project_tree_button['state'] == tk.DISABLED and self.manage_requirements_button['state'] == tk.DISABLED and self.send_button['state'] == tk.DISABLED:
            self.project_tree_button['state'] = tk.NORMAL
            self.manage_requirements_button['state'] = tk.NORMAL
            self.send_button['state'] = tk.NORMAL
