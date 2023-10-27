import tkinter as tk


class InsertValueWithRadioWindow(tk.Toplevel):
    def __init__(self, parent, title, string, callback, width, height, radio_title, radio_options):
        super().__init__(parent)
        self.title(title)
        self.string = string
        self.callback = callback

        # window properties
        self.window_width = 600
        self.window_height = 400
        self.screen_width = width
        self.screen_height = height
        self.padding = 3
        center_x = int(self.screen_width - self.window_width / 2)
        center_y = int(self.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        # entry field
        label_entry = tk.Label(self, text=self.string)
        self.entry = tk.Entry(self, textvariable=tk.StringVar())

        # buttons
        buttons_frame = tk.Frame(self)
        ok_button = tk.Button(buttons_frame, text="Ok", command=lambda: self.ok_button_clicked())
        cancel_button = tk.Button(buttons_frame, text="Cancel", command=lambda: self.destroy())

        radio_buttons_frame = tk.Frame(self)
        # label for radio buttons
        choice_label = tk.Label(radio_buttons_frame, text=radio_title, width=25, padx=self.padding)
        self.chosen_option = tk.IntVar()
        self.chosen_option.set(1)

        # packing
        label_entry.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.entry.pack(side=tk.TOP, pady=self.padding, fill='both')
        buttons_frame.pack(side=tk.BOTTOM, pady=self.padding, fill=tk.BOTH)
        ok_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cancel_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        radio_buttons_frame.pack(side=tk.BOTTOM, pady=self.padding, fill=tk.BOTH)
        # radio buttons
        choice_label.pack(side=tk.LEFT, pady=self.padding)
        for choice in radio_options:
            button = tk.Radiobutton(radio_buttons_frame, text=choice[0], value=choice[1], padx=self.padding, variable=self.chosen_option)
            button.pack(side=tk.LEFT, pady=self.padding)

    def get_entry(self):
        return self.entry.get()

    def get_choice(self):
        return self.chosen_option.get()

    def ok_button_clicked(self):
        self.callback(self.entry.get(), self.chosen_option.get())
        self.destroy()
