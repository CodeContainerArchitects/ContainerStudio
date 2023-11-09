import tkinter as tk


class FoundRequirementsFileWindow(tk.Toplevel):
    def __init__(self, parent, files):
        super().__init__(parent)

        # variables
        self.parent = parent

        # window properties
        self.window_width = 600
        self.window_height = 400
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 5
        center_x = int(self.screen_width / 2 - self.window_width / 2)
        center_y = int(self.screen_height / 2 - self.window_height / 2)
        self.title("Found requirements files")
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        # buttons
        # create upper buttons
        button_frame = tk.Frame(self)
        apply_button = tk.Button(button_frame, text="Apply", command=lambda: self.apply())
        cancel_button = tk.Button(button_frame, text="Cancel", command=lambda: self.destroy())

        # list of requirements
        list_label = tk.Label(self, text="Requirements files: \n")
        self.list_of_requirements = tk.Listbox(self, height=6, selectmode=tk.EXTENDED)
        for file in files:
            self.list_of_requirements.insert(tk.END, file)

        list_label.pack(side=tk.TOP, fill="x")
        self.list_of_requirements.pack(side=tk.TOP, fill="both", expand=True, pady=self.padding)
        button_frame.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

    def apply(self):
        for i in self.list_of_requirements.curselection():
            if self.list_of_requirements.get(i) not in self.parent.chosen_requirements.get(0, tk.END):
                self.parent.chosen_requirements.insert(tk.END, self.list_of_requirements.get(i))
            else:
                tk.messagebox.showinfo("Info", "Such file already exists in main list")
        self.destroy()
