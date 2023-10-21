import tkinter as tk
from tkinter import ttk

class InsertDoubleValueWindow(tk.Toplevel):
    def __init__(self, parent, title, string1, string2, callback, width, height):
        super().__init__(parent)
        self.title(title)
        self.string1 = string1
        self.string2 = string2
        self.callback = callback
        
        self.window_width = 600
        self.window_height = 400
        self.screen_width = width
        self.screen_height = height
        self.padding = 3
        
        center_x = int(self.screen_width - self.window_width / 2)
        center_y = int(self.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        Label1 = tk.Label(self, text=self.string1)
        self.Entry1 = tk.Entry(self, textvariable=tk.StringVar())
        
        Label2 = tk.Label(self, text=self.string2)
        self.Entry2 = tk.Entry(self, textvariable=tk.StringVar())
        
        buttons_frame = tk.Frame(self)
        ok_button = tk.Button(buttons_frame, text="Ok", command=lambda: self.ok_button_clicked())
        cancel_button = tk.Button(buttons_frame, text="Cancel", command=lambda: self.cancel_button_clicked())
        Label1.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.Entry1.pack(side=tk.TOP, pady=self.padding, fill='both')
        
        Label2.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.Entry2.pack(side=tk.TOP, pady=self.padding, fill='both')
        
        buttons_frame.pack(side=tk.BOTTOM, pady=self.padding, fill=tk.BOTH)
        ok_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cancel_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def get_value(self):
        return self.Entry1.get(), self.Entry2.get()

    def ok_button_clicked(self):
        host_port, container_port = self.get_value()
        self.callback(host_port, container_port)
        self.destroy()

    def cancel_button_clicked(self):
        self.destroy()
