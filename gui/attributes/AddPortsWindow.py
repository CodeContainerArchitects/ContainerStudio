import tkinter as tk
from tkinter import ttk
from gui.attributes.InsertValueWindow import InsertValueWindow

class AddPortsWindow(tk.Toplevel):
    def __init__(self, parent, grandparent):
        super().__init__(parent)
        self.window_width = 600
        self.window_height = 400
        self.padding = 5
        
        self.title("Manage ports")
        center_x = int(grandparent.screen_width/2 - self.window_width / 2)
        center_y = int(grandparent.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        self.ports_list = tk.Listbox(self, height=6, selectmode=tk.SINGLE)
        label_for_ports_list = tk.Label(self, text="Ports: \n")
        button_frame_upper = tk.Frame(self)
        add_ports_button = tk.Button(button_frame_upper, text="Add port", command=lambda: self.add_ports())
        delete_ports_button = tk.Button(button_frame_upper, text="Delete port", command=lambda: self.delete_ports())
        button_frame_lower = tk.Frame(self)
        cancel_button = tk.Button(button_frame_lower, text="Cancel", command=self.destroy)
        apply_button = tk.Button(button_frame_lower, text="Apply", command=lambda: self.apply_ports(grandparent))
        
        label_for_ports_list.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.ports_list.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        button_frame_upper.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        add_ports_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        delete_ports_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        
        self.ports = grandparent.coreApp.get_expose_ports()
        for host_port, container_port in self.ports:
            self.ports_list.insert(tk.END, f"{host_port}={container_port}")
            
        self.temp_container_port = ''
        self.temp_host_port = ''
        
    def add_ports(self):
        self.temp_container_port = ''
        self.temp_host_port = ''
        def get_container_port(value):
            if value != '':
                self.temp_container_port = value
        def get_host_port(value):
            if value != '':
                self.temp_host_port = value
        container_port_window = InsertValueWindow(self, "Enter container port", "Enter container port: ", get_container_port)
        container_port_window.grab_set()
        host_port_window = InsertValueWindow(self, "Enter host port", "Enter host port: ", get_host_port)
        host_port_window.grab_set()
        if self.temp_container_port != '':
            if self.temp_host_port == '':
                self.temp_host_port = f"-{self.temp_container_port}"
            self.env_variables_list.insert(tk.END, f"{self.temp_host_port}={self.temp_container_port}")
            self.ports[self.temp_host_port] = self.temp_container_port
            
    def delete_ports(self):
        selected_ports = self.ports_list.curselection()
        if selected_ports:
            port_index = selected_ports[0]
            if port_index or port_index == 0:
                self.ports_list.delete(port_index)
                
    def apply_ports(self, grandparent):
        grandparent.coreApp.set_expose_ports(self.ports)
        self.destroy()
