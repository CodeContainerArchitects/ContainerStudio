import tkinter as tk
from tkinter import ttk

class AddEnvVariablesWindow(tk.Toplevel):
    def __init__(self, parent, grandparent):
        super().__init__(parent)
        self.window_width = 600
        self.window_height = 400
        self.padding = 5
        
        self.title("Add Ports")
        center_x = int(grandparent.screen_width/2 - self.window_width / 2)
        center_y = int(grandparent.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        button_frame_upper = tk.Frame(self)
        add_env_vars_button = tk.Button(button_frame_upper, text="Add environment variables", command=lambda: self.add_env_vars(grandparent))
        
        button_frame_lower = tk.Frame(self)
        cancel_button = tk.Button(button_frame_lower, text="Return to main menu", command=self.destroy)
        
        button_frame_upper.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        add_env_vars_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
