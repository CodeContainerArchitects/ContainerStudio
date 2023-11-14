import tkinter as tk


class InsertListData(tk.Toplevel):
    def __init__(self, parent, title, label1, label2, label3, label4, callback, width, height, radio_title, radio_options):
        super().__init__(parent)
        self.title(title)
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
        label1_entry = tk.Label(self, text=label1)
        self.entry1 = tk.Entry(self, textvariable=tk.StringVar())
        label2_entry = tk.Label(self, text=label2)
        self.entry2 = tk.Entry(self, textvariable=tk.StringVar())
        label3_entry = tk.Label(self, text=label3)
        self.entry3 = tk.Entry(self, textvariable=tk.StringVar())
        label4_entry = tk.Label(self, text=label4)
        self.entry4 = tk.Entry(self, textvariable=tk.StringVar())

        # buttons
        buttons_frame = tk.Frame(self)
        ok_button = tk.Button(buttons_frame, text="Ok", command=lambda: self.ok_button_clicked())
        cancel_button = tk.Button(buttons_frame, text="Cancel", command=lambda: self.destroy())

        radio_buttons_frame = tk.Frame(self)
        # label for radio buttons
        choice_label = tk.Label(radio_buttons_frame, text=radio_title, width=40, padx=self.padding)
        self.chosen_option = tk.IntVar()
        self.chosen_option.set(1)

        # packing
        label1_entry.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.entry1.pack(side=tk.TOP, pady=self.padding, fill='both')
        label2_entry.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.entry2.pack(side=tk.TOP, pady=self.padding, fill='both')
        label3_entry.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.entry3.pack(side=tk.TOP, pady=self.padding, fill='both')
        label4_entry.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.entry4.pack(side=tk.TOP, pady=self.padding, fill='both')
        buttons_frame.pack(side=tk.BOTTOM, pady=self.padding, fill=tk.BOTH)
        ok_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cancel_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        radio_buttons_frame.pack(side=tk.BOTTOM, pady=self.padding, fill=tk.BOTH)

        # radio buttons
        choice_label.pack(side=tk.LEFT, pady=self.padding)
        for choice in radio_options:
            button = tk.Radiobutton(radio_buttons_frame, text=choice[0], value=choice[1], width=10, variable=self.chosen_option)
            button.pack(side=tk.LEFT, pady=self.padding)

    def ok_button_clicked(self):
        self.callback(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.entry4.get(), self.chosen_option.get())
        self.destroy()
