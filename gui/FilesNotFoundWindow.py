import tkinter as tk

class FilesNotFoundWindow(tk.Toplevel):
    def __init__(self, parent, files_not_found):
        super().__init__(parent)

        # self variables
        self.files_not_found = files_not_found

        # self variables
        self.window_width = 600
        self.window_height = 400
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 5

        center_x = int(self.screen_width / 2 - self.window_width / 2)
        center_y = int(self.screen_height / 2 - self.window_height / 2)
        
        self.title("Files not found")
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        label = tk.Label(self, text="Some files were not found. Check if files are in the right directory or adjust their paths: ")
        text_field = tk.Text(self, height=10, width=50)
        for file in self.files_not_found:
            text_field.insert(tk.END, file + "\n")
        text_field.config(state=tk.DISABLED)
        ok_button = tk.Button(self, text="Ok", command=self.destroy)
        
        label.pack(side=tk.TOP, pady=self.padding, fill=tk.BOTH)
        text_field.pack(side=tk.TOP, pady=self.padding, fill=tk.BOTH, expand=True)
        ok_button.pack(side=tk.BOTTOM, pady=self.padding, fill=tk.BOTH)
