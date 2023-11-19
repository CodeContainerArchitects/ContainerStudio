import tkinter as tk
from tkinter import ttk
from gui.attributes.InsertDoubleValueWindow import InsertDoubleValueWindow

class AddEnvVariablesWindow(tk.Toplevel):
    def __init__(self, parent, grandparent):
        super().__init__(parent)
        self.window_width = 600
        self.window_height = 400
        self.padding = 5
        
        self.title("Manage environment variables")
        center_x = int(grandparent.screen_width/2 - self.window_width / 2)
        center_y = int(grandparent.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        self.env_vars_list = tk.Listbox(self, height=6, selectmode=tk.SINGLE)
        label_for_env_vars_list = tk.Label(self, text="Environment Variables: \n")
        button_frame_upper = tk.Frame(self)
        add_env_vars_button = tk.Button(button_frame_upper, text="Add variable", command=lambda: self.add_env_vars(grandparent))
        delete_env_vars_button = tk.Button(button_frame_upper, text="Delete variable", command=lambda: self.delete_env_vars())
        button_frame_lower = tk.Frame(self)
        cancel_button = tk.Button(button_frame_lower, text="Cancel", command=self.destroy)
        apply_button = tk.Button(button_frame_lower, text="Apply", command=lambda: self.apply_env_vars(grandparent))
        
        label_for_env_vars_list.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.env_vars_list.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        button_frame_upper.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        add_env_vars_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        delete_env_vars_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        
        self.env_variables = grandparent.coreApp.get_env_variables()
        for key, value in self.env_variables.items():
            self.env_vars_list.insert(tk.END, f"{key}={value}")
        
    def insert_into_list(self, key, value):
        if key == "":
            tk.messagebox.showerror("Error", "Variable name cannot be empty!")
            return
        if value == "":
            tk.messagebox.showerror("Error", "Variable value cannot be empty!")
            return
        if key in self.env_variables:
            tk.messagebox.showerror("Error", "This variable already exists!")
            return
        self.env_vars_list.insert(tk.END, f"{key}={value}")
        self.env_variables[key] = value
    
    def add_env_vars(self, grandparent):
        env_vars_window = InsertDoubleValueWindow(self, "Add variable", "Enter variable name: ", "Enter variable value", self.insert_into_list, grandparent.screen_width/2, grandparent.screen_height/2)
        env_vars_window.grab_set()
            
    def delete_env_vars(self):
        selected_env_vars = self.env_vars_list.curselection()
        if selected_env_vars:
            env_var_index = selected_env_vars[0]
            if env_var_index or env_var_index == 0:
                list_item = self.ports_list.get(env_var_index)
                key = list_item.split(':')[0]
                self.env_variables.pop(key)
                self.env_vars_list.delete(env_var_index)
                
    def apply_env_vars(self, grandparent):
        grandparent.coreApp.set_env_variables(self.env_variables)
        self.destroy()
