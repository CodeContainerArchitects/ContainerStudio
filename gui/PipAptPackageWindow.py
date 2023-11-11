import tkinter as tk

from createUtils.common_utils import _add_line_to_file


class PipAptPackageWindow(tk.Toplevel):
    def __init__(self, parent, path, os_name):
        super().__init__(parent)

        # variables
        self.parent = parent
        self.os_name = os_name
        self.checkboxes = []
        self.row = 1
        self.path = path

        # window properties
        self.title("Same package for pip and ")
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
        for item in self.parent.apt_pip_packages:
            label = tk.Label(frame, text=item)
            label.grid(row=self.row, column=0, sticky="w")

            # checkbuttons
            if_pip = tk.IntVar()
            checkbox1 = tk.Checkbutton(frame, variable=if_pip, text="pip")
            checkbox1.grid(row=self.row, column=1, sticky="w")

            if_apt = tk.IntVar()
            checkbox2 = tk.Checkbutton(frame, variable=if_apt, text="apt")
            checkbox2.grid(row=self.row, column=2, sticky="w")
            self.row += 1

            self.checkboxes.append((item, if_pip, if_apt))

        # buttons
        button_frame = tk.Frame(self)
        apply_button = tk.Button(button_frame, text="Apply", command=lambda: self.apply())
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.destroy)

        frame.pack()
        button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

    def apply(self):
        for item, if_pip, if_apt in self.checkboxes:
            print(f"{item}: pip is {'checked' if if_pip.get() else 'unchecked'}, apt is {'checked' if if_apt.get() else 'unchecked'}")
            if if_pip.get():
                _add_line_to_file(line=item.split(' ')[0], path_to_file=self.path)
            if if_apt.get():
                self.parent.apt_packages[item.split(' ')[1].replace('(', '').replace(')', '')] = "latest"
        self.destroy()
