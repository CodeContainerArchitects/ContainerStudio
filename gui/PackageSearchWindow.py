import tkinter as tk
from createUtils.package_listing import pip_packages, apt_packages

class PackageSearchWindow(tk.Toplevel):
    def __init__(self, parent, mode, callback):
        super().__init__(parent)
        
        self.window_width = 300
        self.window_height = 370
        self.padding = 5
        self.mode = mode
        self.callback = callback
        
        if mode == 'pip':
            self.title("Select pip package")
        elif mode == 'apt':
            self.title("Select apt package")
        
        center_x = int(parent.screen_width/2 - self.window_width / 2)
        center_y = int(parent.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        
        listframe = tk.Frame(self, width = self.window_width - self.padding * 2)
        optionsframe = tk.Frame(self, width = self.window_width - self.padding*2)
        
        listframe.grid(row = 0, column = 0, sticky='nsew', padx=self.padding, pady=self.padding)
        optionsframe.grid(row=1, column=0, sticky='nsew', padx=self.padding, pady=self.padding)
        
        packages_label = tk.Label(listframe, text="Select package:")
        self.entry = tk.Entry(listframe, width=48)
        self.entry.bind("<KeyRelease>", self.check_list)
        
        self.packages_listbox = tk.Listbox(listframe, height=15, width=47, selectmode=tk.SINGLE)
        self.packages_listbox.bind('<Double-1>', self.set_chosen_package)
        self.update_list(self.packages_listbox, pip_packages.values())
        
        exit_button = tk.Button(optionsframe, text="Cancel", command=self.destroy)
        
        packages_label.grid(row=0, column=0, pady=self.padding)
        self.entry.grid(row=1, column=0, pady=self.padding)
        self.packages_listbox.grid(row=2, column=0, pady=self.padding)
        
        #optionsframe elements
        optionsframe.grid_columnconfigure(0, weight=1)
        exit_button.grid(row=0, column=0, sticky='se', pady=self.padding)

    def update_list(self, listbox, data):
        listbox.delete(0, tk.END)
        
        for item in data:
            listbox.insert(tk.END, item)
    
    def check_list(self, event):
        entry = self.entry.get()
        
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
                    
        self.update_list(self.packages_listbox, data)  

    def set_chosen_package(self, event):
        selected_index = self.packages_listbox.curselection()
        chosen_package = self.packages_listbox.get(selected_index)
        self.callback(chosen_package)
        self.destroy()
