import tkinter as tk
from createUtils.common_utils import map_apt_package


class UnknownPackagesFoundWindow(tk.Toplevel):
    def __init__(self, parent, unknown_packages, os_name):
        super().__init__(parent)

        # variables
        self.parent = parent
        self.os_name = os_name

        # window properties
        self.title("Unknown packages")
        self.window_width = 600
        self.window_height = 400
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 5
        center_x = int(self.screen_width / 2 - self.window_width / 2)
        center_y = int(self.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        # window elements
        label = tk.Label(self, text="Unknown packages have been found. Please select apt packages, which you want to install \n")
        self.list_of_packages = tk.Listbox(self, height=6, selectmode=tk.EXTENDED)

        button_frame_lower = tk.Frame(self)
        apply_button = tk.Button(button_frame_lower, text="Ok", command=lambda: self.ok())
        cancel_button = tk.Button(button_frame_lower, text="Cancel", command=self.destroy)

        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        label.pack(side=tk.TOP, fill='x')
        self.list_of_packages.pack(side=tk.LEFT, pady=self.padding, fill='both', expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

        unknown_packages = list(set(unknown_packages))
        for i in range(0, len(unknown_packages)):
            self.list_of_packages.insert(tk.END, unknown_packages[i])

    def ok(self):
        chosen_packages = []
        for i in self.list_of_packages.curselection():
            apt_package = map_apt_package(package=self.list_of_packages.get(i), os_name=self.os_name)
            chosen_packages.append(apt_package)
        self.parent.apt_packages.extend(chosen_packages)
        self.destroy()
