import tkinter as tk
import os


class EntryWindow(tk.Toplevel):
    def __init__(self, parent, directory, callback):
        super().__init__(parent)

        # self variables
        self.file_name = ""
        self.callback = callback
        self.directory = directory

        # window properties
        self.window_width = 600
        self.window_height = 400
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 5

        center_x = int(self.screen_width / 2 - self.window_width / 2)
        center_y = int(self.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        self.title("Create requirements")

        label_for_entry = tk.Label(self, text="Enter requirements file name: ")
        self.entry = tk.Entry(self, textvariable=tk.StringVar())
        self.label_for_message = tk.Label(self, text="")
        buttons_frame = tk.Frame(self)
        ok_button = tk.Button(buttons_frame, text="Ok", command=lambda: self.ok_button_clicked())
        cancel_button = tk.Button(buttons_frame, text="Cancel", command=lambda: self.cancel_button_clicked())

        label_for_entry.pack(side=tk.TOP, pady=self.padding, fill=tk.BOTH)
        self.entry.pack(side=tk.TOP, pady=self.padding, fill=tk.BOTH)
        self.label_for_message.pack(side=tk.TOP, pady=self.padding, fill=tk.BOTH)
        buttons_frame.pack(side=tk.BOTTOM, pady=self.padding, fill=tk.BOTH)
        ok_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cancel_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def get_user_input(self):
        return self.file_name

    def destroy_object(self):
        self.destroy()

    def ok_button_clicked(self):
        if os.path.exists(os.path.join(self.directory, self.entry.get())):
            self.label_for_message.config(text="File already exists. Choose another name.", fg="red")
        else:
            self.file_name = self.entry.get()
            self.label_for_message.config(text=f"Creating {self.file_name} file...", fg="green")
            self.update_idletasks()
            self.callback(self.file_name)
            self.destroy()

    def cancel_button_clicked(self):
        self.destroy()
