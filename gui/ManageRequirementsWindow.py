import re
import tkinter as tk
from ModuleSearcher import ModuleSearcher
from createUtils.common_utils import _find_files
from gui.EntryWindow import EntryWindow
from gui.FoundRequirementsFileWindow import FoundRequirementsFileWindow
from gui.PipAptPackageWindow import PipAptPackageWindow
from gui.TreeRequirementsWindow import TreeRequirementsWindow
from pip_requirements_parser import RequirementsFile
import os


class ManageRequirementsWindow(tk.Toplevel):
    def __init__(self, parent, set_chosen_requirements):
        super().__init__(parent)

        # variables
        self.file_names = None
        self.apt_packages = []
        self.apt_pip_packages = []
        self.chosen_requirements = []
        self.callback = set_chosen_requirements
        self.parent = parent

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
        label_for_list_of_requirements = tk.Label(self, text="Requirements files: \n")
        self.chosen_requirements = tk.Listbox(self, height=6, selectmode=tk.EXTENDED)

        # create lower buttons
        button_frame_lower = tk.Frame(self)
        delete_button = tk.Button(button_frame_lower, text="Delete", command=lambda: self.delete())
        apply_button = tk.Button(button_frame_lower, text="Apply", command=lambda: self.apply())
        cancel_button = tk.Button(button_frame_lower, text="Cancel", command=self.destroy)

        button_frame_upper.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        self.search_for_requirements_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        create_requirements_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        add_requirements_manual_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

        label_for_list_of_requirements.pack(side=tk.TOP, fill='x')
        self.chosen_requirements.pack(side=tk.LEFT, pady=self.padding, fill='both', expand=True)
        delete_button.pack(side=tk.TOP, pady=self.padding, fill='both', expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

        # take previously saved
        for element in parent.coreApp.chosen_requirements:
            self.chosen_requirements.insert(tk.END, element)

    def search_for_requirements(self):
        result = _find_files(path=self.directory, pattern=re.compile(r".*requirements.*"))
        if result:
            found_requirements_file_window = FoundRequirementsFileWindow(parent=self, files=result)
            found_requirements_file_window.grab_set()
        else:
            tk.messagebox.showinfo(title="Info", message="No requirements files found.")

    def add_to_list_requirements(self, value):
        if os.path.relpath(value, start=self.directory) not in self.chosen_requirements.get(0, tk.END):
            value = os.path.relpath(value, start=self.directory)
            self.chosen_requirements.insert(tk.END, value)
        else:
            tk.messagebox.showinfo(title="Info", message="File already is in the list.")

    def add_requirements_manual(self):
        TreeRequirementsWindow(parent=self)

    def create_requirements(self, parent):
        def callback_create_requirements(file_name):
            if file_name != '':
                module_searcher = ModuleSearcher(path_to_project=self.directory, requirements_file_name=file_name, os_name=self.parent.coreApp.OS_data["OS_image"].capitalize(), coreApp=self.parent.coreApp)
                _, _, self.apt_packages, self.not_known_packages, self.apt_pip_packages = module_searcher.get_modules()

                self.chosen_requirements.insert(tk.END, file_name)
                if len(self.apt_pip_packages) != 0:
                    PipAptPackageWindow(parent=self, path=os.path.join(self.directory, file_name), os_name=self.parent.coreApp.OS_data["OS_image"].capitalize())
                if len(self.not_known_packages) != 0:
                    self.not_known_packages = list(set(self.not_known_packages))
                    tk.messagebox.showwarning(title="Warning", message="Not known found packages during creating "
                                                                       "requirements file. Check it and add this "
                                                                       "packages if necessary. \n\n" + '\n'.join(self.not_known_packages))
        entry_window = EntryWindow(self, parent.projectTree.get_working_directory(), callback_create_requirements)
        entry_window.grab_set()

    def delete(self):
        selected = self.chosen_requirements.curselection()
        for s in selected:
            self.chosen_requirements.delete(s)

    def apply(self):
        requirements_pip_packages = {}
        requirements_files = []
        for item in self.chosen_requirements.get(0, tk.END):
            requirements_files.append(item)
        self.file_names = [os.path.split(file)[-1] for file in requirements_files]
        requirements_files_dockerfile_path = [self.parent.coreApp.container_directory + item for item in requirements_files]

        # remove duplicates
        self.apt_packages = list(set(self.apt_packages))
        apt_packages_dict = {}
        for item in self.apt_packages:
            apt_packages_dict[item] = "latest"

        # parse choosen requirements
        for r in requirements_files:
            rf = RequirementsFile.from_file(os.path.join(self.directory, r))
            for req in rf.requirements:
                d = req.to_dict()
                name = d["name"]
                requirements_pip_packages[name] = "no version"

        # give requirements_pip_packages to the main list
        self.callback(requirements_files, requirements_files_dockerfile_path, apt_packages_dict, requirements_pip_packages)
        self.destroy()
