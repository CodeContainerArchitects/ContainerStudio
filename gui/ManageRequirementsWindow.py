import re
import tkinter as tk
from ModuleSearcher import ModuleSearcher
from createUtils.common_utils import _find_files
from gui.EntryWindow import EntryWindow
from gui.PipAptPackageWindow import PipAptPackageWindow
from gui.TreeRequirementsWindow import TreeRequirementsWindow
from pip_requirements_parser import RequirementsFile
import os
from gui.UnknownPackagesFoundWindow import UnknownPackagesFoundWindow


class ManageRequirementsWindow(tk.Toplevel):
    def __init__(self, parent, set_chosen_requirements):
        super().__init__(parent)

        # variables
        self.file_names = None
        self.apt_packages = []
        self.apt_pip_packages = []
        self.chosen_requirements = []
        self.callback = set_chosen_requirements

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
        self.search_for_requirements_button = tk.Button(button_frame_upper, text="Search for requirements", command=lambda: self.search_for_requirements())
        create_requirements_button = tk.Button(button_frame_upper, text="Create requirements", command=lambda: self.create_requirements(parent))
        add_requirements_manual_button = tk.Button(button_frame_upper, text="Add requirements", command=lambda: self.add_requirements_manual())

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
        self.search_for_requirements_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        create_requirements_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        add_requirements_manual_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

        label_for_list_of_requirements.pack(side=tk.TOP, fill='x')
        self.list_of_requirements.pack(side=tk.LEFT, pady=self.padding, fill='both', expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

    def search_for_requirements(self):
        result = _find_files(path=self.directory, pattern=re.compile(r".*requirements.*"))

        # delete comment if it exists
        self.delete_no_files_found_comment()

        if len(result) == 0 and self.list_of_requirements.size() == 0:
            self.list_of_requirements.insert(tk.END, "No requirements files found")
        else:
            for file in result:
                if file not in self.list_of_requirements.get(0, tk.END):
                    self.list_of_requirements.insert(tk.END, file)

    def add_to_list_requirements(self, value):
        self.delete_no_files_found_comment()
        if os.path.relpath(value, start=self.directory) not in self.list_of_requirements.get(0, tk.END):
            value = os.path.relpath(value, start=self.directory)
            self.list_of_requirements.insert(tk.END, value)

    def delete_no_files_found_comment(self):
        if self.list_of_requirements.size() > 0:
            if "No requirements files found" in self.list_of_requirements.get(0):
                self.list_of_requirements.delete(0, tk.END)

    def add_requirements_manual(self):
        TreeRequirementsWindow(parent=self)

    def create_requirements(self, parent):
        def callback_create_requirements(file_name):
            if file_name != '':
                module_searcher = ModuleSearcher(path_to_project=self.directory, requirements_file_name=file_name)
                _, _, self.apt_packages, self.not_known_packages, self.apt_pip_packages = module_searcher.get_modules()

                self.delete_no_files_found_comment()
                self.list_of_requirements.insert(tk.END, file_name)
                if len(self.apt_pip_packages) != 0:
                    PipAptPackageWindow(parent=self, path=os.path.join(self.directory, file_name))
                if len(self.not_known_packages) != 0:
                    UnknownPackagesFoundWindow(parent=self, unknown_packages=self.not_known_packages)
        entry_window = EntryWindow(self, parent.projectTree.get_working_directory(), callback_create_requirements)
        entry_window.grab_set()

    def apply(self):
        self.chosen_requirements = []
        requirements_pip_packages = []
        for i in self.list_of_requirements.curselection():
            self.chosen_requirements.append(self.list_of_requirements.get(i))
        self.file_names = [os.path.split(file)[-1] for file in self.chosen_requirements]

        # remove duplicates
        self.apt_packages = list(set(self.apt_packages))

        # parse choosen requirements
        for r in self.chosen_requirements:
            rf = RequirementsFile.from_file(os.path.join(self.directory, r))
            for req in rf.requirements:
                d = req.to_dict()
                requirements_pip_packages.append(d["name"])
        print(requirements_pip_packages)

        # give requirements_pip_packages to the main list
        self.callback(self.chosen_requirements, self.file_names, self.apt_packages, requirements_pip_packages)
        self.destroy()
