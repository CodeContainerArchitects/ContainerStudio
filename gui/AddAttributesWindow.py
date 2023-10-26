import tkinter as tk

from gui.attributes.AddPortsWindow import AddPortsWindow
from gui.attributes.AddEnvVariablesWindow import AddEnvVariablesWindow
from gui.attributes.AddEntryPointWindow import AddEntryPointWindow


class AddAttributesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.window_width = 800
        self.window_height = 600
        self.padding = 5
        
        self.title("Customize Dockerfile Attributes")
        center_x = int(parent.screen_width/2 - self.window_width / 2)
        center_y = int(parent.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        button_frame_upper = tk.Frame(self)
        add_ports_button = tk.Button(button_frame_upper, text="Add ports", command=lambda: self.add_ports(parent))
        add_env_variables_button = tk.Button(button_frame_upper, text="Add environment variables", command=lambda: self.add_env_variables(parent))

        button_frame_upper_1 = tk.Frame(self)
        add_entrypoint_button = tk.Button(button_frame_upper_1, text="Add entry point", command=lambda: self.add_entry_point(parent))
        add_volumes_button = tk.Button(button_frame_upper_1, text="Add volumes", command=lambda: self.add_volumes(parent))

        button_frame_upper_2 = tk.Frame(self)
        add_run_commands_button = tk.Button(button_frame_upper_2, text="Add commands", command=lambda: self.add_commands(parent))

        button_frame_lower = tk.Frame(self)
        cancel_button = tk.Button(button_frame_lower, text="Return to main menu", command=self.destroy)
        
        button_frame_upper.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_upper_1.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_upper_2.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')

        add_ports_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        add_env_variables_button.pack(side=tk.RIGHT, pady=self.padding, fill='x', expand=True)
        add_entrypoint_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        add_volumes_button.pack(side=tk.RIGHT, pady=self.padding, fill='x', expand=True)
        add_run_commands_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        
    def add_ports(self, parent):
        add_ports_window = AddPortsWindow(self, parent)
        add_ports_window.grab_set()
        
    def add_env_variables(self, parent):
        add_env_vars_window = AddEnvVariablesWindow(self, parent)
        add_env_vars_window.grab_set()

    def add_entry_point(self, parent):
        add_entry_point_window = AddEntryPointWindow(parent=self, grandparent=parent)
        add_entry_point_window.grab_set()

    def add_volumes(self, parent):
        pass

    def add_commands(self, parent):
        pass