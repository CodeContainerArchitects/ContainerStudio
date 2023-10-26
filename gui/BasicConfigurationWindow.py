import tkinter as tk
from createUtils.package_listing import pip_packages, apt_packages, python_versions, os_versions
from createUtils.common_utils import update_list
from createUtils.package_listing import get_package_versions


class BasicConfigurationWindow(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)

        # variables
        self.chosen_os = ''
        self.chosen_python = ''
        self.parent = parent
        self.callback = callback

        # appearance
        self.window_width = 800
        self.window_height = 500
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 5
        center_x = int(self.screen_width / 2 - self.window_width / 2)
        center_y = int(self.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.title("Basic Configuration")

        python_frame = tk.Frame(self, width=self.window_width / 2 - self.padding * 2)
        os_frame = tk.Frame(self, width=self.window_width / 2 - self.padding * 2)
        button_frame = tk.Frame(self, width=self.window_width - self.padding * 2)

        python_frame.grid(row=0, column=0, sticky='nsew', padx=self.padding, pady=self.padding)
        os_frame.grid(row=0, column=1, sticky='nsew', padx=self.padding, pady=self.padding)
        button_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=self.padding, pady=self.padding)

        # python version
        version_label = tk.Label(python_frame, text="Select Python version:")
        self.entry_version = tk.Entry(python_frame, width=47)
        self.entry_version.bind("<KeyRelease>", self.check_python_versions)
        self.version_listbox = tk.Listbox(python_frame, height=15, width=47, selectmode=tk.SINGLE, exportselection=0)
        self.version_listbox.bind('<<ListboxSelect>>', self.set_python_version)
        # os
        os_label = tk.Label(os_frame, text="Select Operating System:")
        self.entry_os = tk.Entry(os_frame, width=47)
        self.entry_os.bind("<KeyRelease>", self.check_operating_systems)
        self.os_listbox = tk.Listbox(os_frame, height=15, width=47, selectmode=tk.SINGLE, exportselection=0)
        self.os_listbox.bind('<<ListboxSelect>>', self.set_operating_system)

        update_list(self.version_listbox, python_versions)
        update_list(self.os_listbox, os_versions)
        
        if parent.coreApp.python_version:
            index_python = self.version_listbox.get(0, tk.END).index(parent.coreApp.python_version)
            self.version_listbox.select_set(index_python)
            self.chosen_python = self.version_listbox.get(index_python)
        
        if parent.coreApp.OS_data:
            index_os = self.os_listbox.get(0, tk.END).index(f"{parent.coreApp.OS_data['OS_image']}:{parent.coreApp.OS_data['OS_image_version']}")
            self.os_listbox.select_set(index_os)
            self.chosen_os = self.os_listbox.get(index_os)
            
        self.apply_button = tk.Button(button_frame, text="Apply", command=lambda: self.apply())
        exit_button = tk.Button(button_frame, text="Cancel", command=self.destroy)

        # python frame
        version_label.grid(row=0, column=0, pady=self.padding)
        self.entry_version.grid(row=1, column=0, pady=self.padding)
        self.version_listbox.grid(row=2, column=0, pady=self.padding)

        # os_frame elements
        os_label.grid(row=0, column=0, pady=self.padding)
        self.entry_os.grid(row=1, column=0, pady=self.padding)
        self.os_listbox.grid(row=2, column=0, pady=self.padding)

        # button_frame elements
        self.apply_button.grid(row=0, column=0, pady=self.padding)
        button_frame.grid_columnconfigure(1, weight=1)
        exit_button.grid(row=0, column=1, sticky='se', pady=self.padding)

    def check_operating_systems(self, event):
        entry = self.entry_os.get()
        if entry == '':
            data = list
        else:
            data = []
            for item in os_versions:
                if entry.lower() in item.lower():
                    data.append(item)
        update_list(self.os_listbox, data)

    def check_python_versions(self, event):
        entry = self.entry_version.get()
        if entry == '':
            data = list
        else:
            data = []
            for item in python_versions:
                if entry.lower() in item.lower():
                    data.append(item)
        update_list(self.version_listbox, data)

    def set_python_version(self, event):
        selected_index = self.version_listbox.curselection()
        self.chosen_python = self.version_listbox.get(selected_index)

    def set_operating_system(self, event):
        selected_index = self.os_listbox.curselection()
        self.chosen_os = self.os_listbox.get(selected_index)

    def apply(self):
        selected_index_os = self.os_listbox.curselection()
        selected_index_python = self.version_listbox.curselection()
        if selected_index_os:
            if selected_index_python:
                chosen_system_split = self.chosen_os.split(":")
                self.callback(chosen_system_split[0], chosen_system_split[1], self.chosen_python)
                self.destroy()
            else:
                tk.messagebox.showerror("Error", "Python version must be selected!")
        else:
            tk.messagebox.showerror("Error", "Operating system must be selected!")
