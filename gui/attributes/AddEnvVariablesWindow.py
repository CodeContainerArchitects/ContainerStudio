import tkinter as tk
from tkinter import ttk
from gui.attributes.InsertValueWindow import InsertValueWindow

class AddEnvVariablesWindow(tk.Toplevel):
    def __init__(self, parent, grandparent):
        super().__init__(parent)
        self.window_width = 600
        self.window_height = 400
        self.padding = 5
        
        self.title("Add Environment Variables")
        center_x = int(grandparent.screen_width/2 - self.window_width / 2)
        center_y = int(grandparent.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        self.env_var_list = tk.Listbox(self, height=6, selectmode=tk.SINGLE)
        label_for_env_var_list = tk.Label(self, text="Environment Variables: \n")
        button_frame_upper = tk.Frame(self)
        add_env_var_button = tk.Button(button_frame_upper, text="Add variable", command=lambda: self.add_env_var())
        delete_env_var_button = tk.Button(button_frame_upper, text="Delete variable", command=lambda: self.delete_env_var())
        button_frame_lower = tk.Frame(self)
        cancel_button = tk.Button(button_frame_lower, text="Cancel", command=self.destroy)
        apply_button = tk.Button(button_frame_lower, text="Apply", command=lambda: self.apply_env_var(grandparent))
        
        label_for_env_var_list.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.env_var_list.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        button_frame_upper.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        add_env_var_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        delete_env_var_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        
        self.env_vars = grandparent.coreApp.get_env_variables()
        for var_name, var_value in self.env_vars:
            self.env_var_list.insert(tk.END, f"{var_name}={var_value}")
            
        self.temp_var_value = ''
        self.temp_var_name = ''


    def add_env_var(self):
        self.temp_var_value = ''
        self.temp_var_name = ''
        def get_var_value(value):
            if value != '':
                self.temp_var_value = value
        def get_var_name(value):
            if value != '':
                self.temp_var_name = value
        var_value_window = InsertValueWindow(self, "Enter variable name", "Enter variable name: ", get_var_value)
        var_value_window.grab_set()
        var_name_window = InsertValueWindow(self, "Enter variable value", "Enter variable value: ", get_var_name)
        var_name_window.grab_set()
        if self.temp_var_value != '':
            if self.temp_var_name == '':
                self.temp_var_name = f"-{self.temp_var_value}"
            self.env_var_list.insert(tk.END, f"{self.temp_var_name}={self.temp_var_value}")
            self.env_vars[self.temp_var_name] = self.temp_var_value
            
    def delete_env_var(self):
        selected_env_vars = self.env_var_list.curselection()
        if selected_env_vars:
            env_var_index = selected_env_vars[0]
            if env_var_index or env_var_index == 0:
                self.env_var_list.delete(env_var_index)
                
    def apply_env_var(self, grandparent):
        grandparent.coreApp.set_env_variables(self.env_vars)
        self.destroy()
