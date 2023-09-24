import re
import tkinter as tk
from requirements_searching import _find_files
from ModuleSearcher import ModuleSearcher
from gui.EntryWindow import EntryWindow
import os


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
        self.directory = parent.projectTree.get_working_directory()

        self.title("Manage requirements")
        center_x = int(parent.screen_width / 2 - self.window_width / 2)
        center_y = int(parent.screen_height / 2 - self.window_height / 2)

        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        # create upper buttons
        button_frame_upper = tk.Frame(self)
        search_for_requirements_button = tk.Button(button_frame_upper, text="Search for requirements", command=lambda: self.search_for_requirements())
        create_requirements_button = tk.Button(button_frame_upper, text="Create requirements", command=lambda: self.create_requirements(parent))

        # create list of requirements
        self.list_of_requirements = tk.Listbox(self, height=6, selectmode=tk.EXTENDED)

        # create label for list of requirements
        label_for_list_of_requirements = tk.Label(self, text="Found requirements files: \n")

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
            self.list_of_requirements.insert(tk.END, "No requirements files found")
        else:
            for file in result:
                self.list_of_requirements.insert(tk.END, file)

    def create_requirements(self, parent):
        def callback_create_requirements(file_name):
            if file_name != '':
                module_searcher = ModuleSearcher(path_to_project=self.directory, file_name=file_name)
                module_searcher.get_modules()
                self.search_for_requirements()
        entry_window = EntryWindow(self, parent.projectTree.get_working_directory(), callback_create_requirements)
        entry_window.grab_set()

    def apply(self):
        self.chosen_requirements = []
        for i in self.list_of_requirements.curselection():
            self.chosen_requirements.append(self.list_of_requirements.get(i))
        self.file_names = [os.path.split(file)[-1] for file in self.chosen_requirements]
        self.callback(self.chosen_requirements, self.file_names)
        self.destroy()
