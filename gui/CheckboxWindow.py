import tkinter as tk


class CheckboxWindow(tk.Toplevel):
    def __init__(self, parent, title, elements, callback):
        super().__init__(parent)

        # variables
        self.parent = parent
        self.row = 1
        self.checkboxes = []
        self.callback = callback

        # window properties
        self.title(title)
        self.window_width = 600
        self.window_height = 400
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 5
        center_x = int(self.screen_width / 2 - self.window_width / 2)
        center_y = int(self.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        # list with checkboxes
        frame = tk.Frame(self)
        for key, value in elements.items():
            # check button
            checked = tk.IntVar()
            checked.set(value)
            checkbox = tk.Checkbutton(frame, variable=checked, text=key)
            checkbox.grid(row=self.row, column=1, sticky="w")

            self.row += 1
            self.checkboxes.append((key, checked))

        # buttons
        button_frame = tk.Frame(self)
        apply_button = tk.Button(button_frame, text="Apply", command=lambda: self.apply())
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.destroy)

        frame.pack()
        button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

    def apply(self):
        self.callback(self.checkboxes)
        self.destroy()
