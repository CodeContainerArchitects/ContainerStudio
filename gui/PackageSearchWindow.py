import tkinter as tk
from createUtils.package_listing import pip_packages, apt_packages
from createUtils.common_utils import update_list
from createUtils.package_listing import get_package_versions

class PackageSearchWindow(tk.Toplevel):
    def __init__(self, parent, mode, callback):
        super().__init__(parent)
        
        self.window_width = 800
        self.window_height = 500
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 5
        self.mode = mode
        self.callback = callback
        
        self.chosen_package = ''
        self.chosen_version = ''
        
        if mode == 'pip':
            self.title("Select pip package")
        elif mode == 'apt':
            self.title("Select apt package")
        
        center_x = int(self.screen_width/2 - self.window_width / 2)
        center_y = int(self.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        
        listframe = tk.Frame(self, width = self.window_width/2 - self.padding * 2)
        versionframe = tk.Frame(self, width = self.window_width/2 - self.padding * 2)
        optionsframe = tk.Frame(self, width = self.window_width - self.padding*2)
        
        listframe.grid(row = 0, column = 0, sticky='nsew', padx=self.padding, pady=self.padding)
        versionframe.grid(row = 0, column = 1, sticky='nsew', padx=self.padding, pady=self.padding)
        optionsframe.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=self.padding, pady=self.padding)
        
        packages_label = tk.Label(listframe, text="Select package:")
        self.entry_package = tk.Entry(listframe, width=47)
        self.entry_package.bind("<KeyRelease>", self.check_list_package)
        
        self.packages_listbox = tk.Listbox(listframe, height=15, width=47, selectmode=tk.SINGLE, exportselection=0)
        self.packages_listbox.bind('<<ListboxSelect>>', self.set_chosen_package)
        
        if self.mode == 'pip':
                list = pip_packages.keys()
        elif self.mode == 'apt':
                list = apt_packages.keys()
        update_list(self.packages_listbox, list)
        
        version_label = tk.Label(versionframe, text="Select package version:")
        self.entry_version = tk.Entry(versionframe, width=47)
        self.entry_version.bind("<KeyRelease>", self.check_list_version)
        
        self.version_listbox = tk.Listbox(versionframe, height=15, width=47, selectmode=tk.SINGLE, exportselection=0)
        self.version_listbox.bind('<<ListboxSelect>>', self.set_chosen_package_version)
        
        self.apply_button = tk.Button(optionsframe, text="Apply", state=tk.DISABLED, command=lambda:self.send_package())
        exit_button = tk.Button(optionsframe, text="Cancel", command=self.destroy)
        
        packages_label.grid(row=0, column=0, pady=self.padding)
        self.entry_package.grid(row=1, column=0, pady=self.padding)
        self.packages_listbox.grid(row=2, column=0, pady=self.padding)
        
        #versionframe elements 
        version_label.grid(row=0, column=0, pady=self.padding)
        self.entry_version.grid(row=1, column=0, pady=self.padding)
        self.version_listbox.grid(row=2, column=0, pady=self.padding)
        
        #optionsframe elements
        self.apply_button.grid(row=0, column=0, pady=self.padding)
        optionsframe.grid_columnconfigure(1, weight=1)
        exit_button.grid(row=0, column=1, sticky='se', pady=self.padding)
    
    def check_list_package(self, event):
        entry = self.entry_package.get()
        
        if self.mode == 'pip':
                list = pip_packages.values()
        elif self.mode == 'apt':
                list = apt_packages.values()
                
        if entry =='':
            data = list
        else:
            data = []
            
            for item in list:
                if entry.lower() in item.lower():
                    data.append(item)
                    
        update_list(self.packages_listbox, data)  
        
    def check_list_version(self, event):
        entry = self.entry_version.get()
        
        if self.chosen_package != '':
            list = get_package_versions(self.mode, self.chosen_package)
                    
            if entry =='':
                data = list
            else:
                data = []
                
                for item in list:
                    if entry.lower() in item.lower():
                        data.append(item)
                        
            update_list(self.packages_listbox, data)  

    def set_chosen_package(self, event):
        selected_index = self.packages_listbox.curselection()
        self.chosen_package = self.packages_listbox.get(selected_index)
        
        if self.chosen_package == '':
            if self.apply_button['state'] == tk.NORMAL:
                self.apply_button['state'] = tk.DISABLED
        else:
            list = get_package_versions(self.mode, self.chosen_package)
            update_list(self.version_listbox, list)

    def set_chosen_package_version(self, event):
        selected_index = self.version_listbox.curselection()
        self.chosen_package_version = self.version_listbox.get(selected_index)
        
        if self.chosen_package != '' and self.chosen_package_version != '':
            if self.apply_button['state'] == tk.DISABLED:
                self.apply_button['state'] = tk.NORMAL
        else:
            if self.apply_button['state'] == tk.NORMAL:
                self.apply_button['state'] = tk.DISABLED

    def send_package(self):
        self.callback(self.chosen_package, self.chosen_package_version)
        self.destroy()
