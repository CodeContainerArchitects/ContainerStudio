import tkinter as tk
from tkinter import ttk

class InsertValueWindow(tk.Toplevel):
    def __init__(self, parent, title, string, callback):
        super().__init__(parent)
        self.title(title)
        self.string = string
        self.callback = callback
        
        self.window_width = 300
        self.window_height = 200
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 3
        
        center_x = int(self.screen_width - self.window_width / 2)
        center_y = int(self.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        Label = tk.Label(self, text=self.string)
        self.Entry = tk.Entry(self, textvariable=tk.StringVar())
        
        buttons_frame = tk.Frame(self)
        ok_button = tk.Button(buttons_frame, text="Ok", command=lambda: self.ok_button_clicked())
        cancel_button = tk.Button(buttons_frame, text="Cancel", command=lambda: self.cancel_button_clicked())
        Label.pack(side=tk.LEFT, pady=self.padding, fill='both')
        self.Entry.pack(side=tk.RIGHT, pady=self.padding, fill='both')
        
        buttons_frame.pack(side=tk.BOTTOM, pady=self.padding, fill=tk.BOTH)
        ok_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cancel_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def get_value(self):
        return self.Entry.get()

    def ok_button_clicked(self):
        self.value = self.get_value()
        self.callback(self.value)
        self.destroy()

    def cancel_button_clicked(self):
        self.destroy()
