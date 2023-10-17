import tkinter as tk
from createUtils.package_listing import pip_packages, apt_packages

class PackageListWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.window_width = 800
        self.window_height = 600
        self.padding = 5
        self.title("Select apt and pip packages")
        center_x = int(parent.screen_width/2 - self.window_width / 2)
        center_y = int(parent.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        self.parent = parent
        
        pipframe = tk.Frame(self, width = self.window_width/2 - self.padding * 2)
        aptframe = tk.Frame(self, width = self.window_width/2 - self.padding * 2)
        optionsframe = tk.Frame(self, width = self.window_width - self.padding*2)
        
        pipframe.grid(row = 0, column = 0, sticky='nsew', padx=self.padding, pady=self.padding)
        aptframe.grid(row = 0, column = 1, sticky='nsew', padx=self.padding, pady=self.padding)
        optionsframe.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=self.padding, pady=self.padding)
        
        pip_packages_label = tk.Label(pipframe, text="Select pip packages")
        self.pip_entry = tk.Entry(pipframe, width=50)
        self.pip_entry.bind("<KeyRelease>", self.check_pip_list)
        
        #pip_packages_listvar = tk.StringVar(value=list(pip_packages.values()))
        self.pip_packages_listbox = tk.Listbox(pipframe, height=10, width=50, selectmode='multiple', exportselection=0)
        
        self.pip_packages_listbox.bind('<<ListboxSelect>>', self.set_chosen_pip_packages)
        self.update_list(self.pip_packages_listbox, pip_packages.values())
        
        apt_packages_label = tk.Label(aptframe, text="Select apt packages")
        
        self.apt_entry = tk.Entry(aptframe, width=50)
        self.apt_entry.bind("<KeyRelease>", self.check_apt_list)
        
        #apt_packages_listvar = tk.StringVar(value=list(apt_packages.values()))
        self.apt_packages_listbox = tk.Listbox(aptframe, height=10, width=50, selectmode='multiple', exportselection=0)
        self.apt_packages_listbox.bind('<<ListboxSelect>>', self.set_chosen_apt_packages)
        self.update_list(self.apt_packages_listbox, apt_packages.values())
        
        exit_button = tk.Button(optionsframe, text="Apply", command=self.destroy)
        
        pip_packages_label.grid(row=0, column=0, pady=self.padding)
        self.pip_entry.grid(row=1, column=0, pady=self.padding)
        #pip_packages_label.pack(pady=self.padding)
        self.pip_packages_listbox.grid(row=2, column=0, pady=self.padding)
        #self.pip_packages_listbox.pack(pady=self.padding)
        
        apt_packages_label.grid(row=0, column=0, pady=self.padding)
        self.apt_entry.grid(row=1, column=0, pady=self.padding)
        #apt_packages_label.pack(pady=self.padding)
        self.apt_packages_listbox.grid(row=2, column=0, pady=self.padding)
        #self.apt_packages_listbox.pack(pady=self.padding)
        
        exit_button.grid(row=0, column=0, pady=self.padding)
        
    def update_list(self, listbox, data):
        listbox.delete(0, tk.END)
        
        for item in data:
            listbox.insert(tk.END, item)
        
    def check_pip_list(self, event):
        entry = self.pip_entry.get()
        if entry =='':
            data = pip_packages.values()
        else:
            data = []
            
            for item in pip_packages.values():
                if entry.lower() in item.lower():
                    data.append(item)
                    
        self.update_list(self.pip_packages_listbox, data)  
        
    def check_apt_list(self, event):
        entry = self.apt_entry.get()
        if entry =='':
            data = apt_packages.values()
        else:
            data = []
            
            for item in apt_packages.values():
                if entry.lower() in item.lower():
                    data.append(item)
                    
        self.update_list(self.apt_packages_listbox, data)  
        

    def set_chosen_pip_packages(self, event):
        selected_pip_indices = self.pip_packages_listbox.curselection()
        chosen_pip_packages = [self.pip_packages_listbox.get(index) for index in selected_pip_indices]
        self.parent.coreApp.set_chosen_pip_packages(chosen_pip_packages)

    def set_chosen_apt_packages(self, event):
        selected_apt_indices = self.apt_packages_listbox.curselection()
        chosen_apt_packages = [self.apt_packages_listbox.get(index) for index in selected_apt_indices]
        self.parent.coreApp.set_chosen_apt_packages(chosen_apt_packages)
