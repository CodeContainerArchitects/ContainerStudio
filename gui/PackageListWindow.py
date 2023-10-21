import tkinter as tk
from createUtils.common_utils import update_list
from gui.PackageSearchWindow import PackageSearchWindow

class PackageListWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.window_width = 800
        self.window_height = 500
        self.padding = 10
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.title("Selected pip and apt packages")
        center_x = int(self.screen_width/2 - self.window_width / 2)
        center_y = int(self.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        self.parent = parent
        
        pipframe = tk.Frame(self, width = self.window_width/2 - self.padding * 2)
        aptframe = tk.Frame(self, width = self.window_width/2 - self.padding * 2)
        optionsframe = tk.Frame(self, width = self.window_width - self.padding*2)
        
        pipframe.grid(row = 0, column = 0, sticky='nsew', padx=self.padding, pady=self.padding)
        aptframe.grid(row = 0, column = 1, sticky='nsew', padx=self.padding, pady=self.padding)
        optionsframe.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=self.padding, pady=self.padding)
        
        pip_packages_label = tk.Label(pipframe, text="Selected pip packages")
        self.pip_packages_listbox = tk.Listbox(pipframe, height=10, width=45, selectmode='multiple')
        update_list(self.pip_packages_listbox, self.parent.coreApp.get_chosen_pip_packages())
        
        apt_packages_label = tk.Label(aptframe, text="Selected apt packages")
        self.apt_packages_listbox = tk.Listbox(aptframe, height=10, width=45, selectmode='multiple')
        update_list(self.apt_packages_listbox, self.parent.coreApp.get_chosen_apt_packages())
        
        add_pip_button = tk.Button(pipframe, text="Add pip package", command=lambda: self.add_package('pip'))
        add_apt_button = tk.Button(aptframe, text="Add apt package", command=lambda: self.add_package('apt'))
        delete_pip_button = tk.Button(pipframe, text="Delete pip package", command=lambda: self.delete_package('pip'))
        delete_apt_button = tk.Button(aptframe, text="Delete apt package", command=lambda: self.delete_package('apt'))
        
        
        exit_button = tk.Button(optionsframe, text="Exit", command=self.destroy)
        
        pip_packages_label.grid(row=0, column=0, pady=self.padding)
        self.pip_packages_listbox.grid(row=1, column=0, pady=self.padding)
        add_pip_button.grid(row=2, column=0, pady=self.padding)
        delete_pip_button.grid(row=3, column=0, pady=self.padding)
        
        apt_packages_label.grid(row=0, column=0, pady=self.padding)
        self.apt_packages_listbox.grid(row=1, column=0, pady=self.padding)
        add_apt_button.grid(row=2, column=0, pady=self.padding)
        delete_apt_button.grid(row=3, column=0, pady=self.padding)
        
        optionsframe.grid_columnconfigure(0, weight=1)
        exit_button.grid(row=0, column=0, sticky='e', pady=self.padding)

    def add_package(self, mode):
        def callback_add_package(chosen_package, chosen_package_version):
            if mode == 'pip':
                self.parent.coreApp.add_chosen_pip_package(chosen_package)
                update_list(self.pip_packages_listbox, self.parent.coreApp.get_chosen_pip_packages())
            elif mode == 'apt':
                self.parent.coreApp.add_chosen_apt_package(chosen_package)
                update_list(self.apt_packages_listbox, self.parent.coreApp.get_chosen_apt_packages())

        package_search_window = PackageSearchWindow(self, mode, callback_add_package)
        package_search_window.grab_set()
        
    
    def delete_package(self, mode):
        
        if mode == 'pip':
            chosen_packages_indices = self.pip_packages_listbox.curselection()
            chosen_packages = [self.pip_packages_listbox.get(index) for index in chosen_packages_indices]
            if chosen_packages:
                self.parent.coreApp.delete_chosen_pip_packages(chosen_packages)
                update_list(self.pip_packages_listbox, self.parent.coreApp.get_chosen_pip_packages())
        elif mode == 'apt':
            chosen_packages_indices = self.apt_packages_listbox.curselection()
            chosen_packages = [self.apt_packages_listbox.get(index) for index in chosen_packages_indices]
            if chosen_packages:
                self.parent.coreApp.delete_chosen_apt_packages(chosen_packages)
                update_list(self.apt_packages_listbox, self.parent.coreApp.get_chosen_apt_packages())
