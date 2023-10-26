import tkinter as tk
from gui.attributes.InsertValueWindow import InsertValueWindow


class AddEntryPointWindow(tk.Toplevel):
    def __init__(self, parent, grandparent):
        super().__init__(parent)
        self.window_width = 600
        self.window_height = 400
        self.padding = 5

        self.title("Add ENTRYPOINT")
        center_x = int(grandparent.screen_width / 2 - self.window_width / 2)
        center_y = int(grandparent.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        result_entry_point_label = tk.Label(self, text='Result')
        self.result_entry_point = tk.Label(self, text='ENTRYPOINT ')
        parameters_list_label = tk.Label(self, text='Added parameters')
        self.parameters_list = tk.Listbox(self, height=6)

        # buttons
        button_frame_upper = tk.Frame(self)
        add_parameter_button = tk.Button(button_frame_upper, text="Add parameter", command=lambda: self.add_parameter(grandparent=grandparent))
        delete_parameter_button = tk.Button(button_frame_upper, text="Delete parameters", command=lambda: self.delete_parameters())
        button_frame_lower = tk.Frame(self)
        cancel_button = tk.Button(button_frame_lower, text="Cancel", command=self.destroy)
        apply_button = tk.Button(button_frame_lower, text="Apply", command=lambda: self.apply(grandparent))

        # packing elements
        result_entry_point_label.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.result_entry_point.pack(side=tk.TOP, pady=self.padding, fill='both')
        parameters_list_label.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.parameters_list.pack(side=tk.TOP, pady=self.padding, fill='both')

        button_frame_upper.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        add_parameter_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        delete_parameter_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

        # self.ports = grandparent.coreApp.get_expose_ports()
        # for host_port, container_port in self.ports.items():
        #     if host_port == f"-{container_port}":
        #         self.ports_list.insert(tk.END, f":{container_port}")
        #     else:
        #         self.ports_list.insert(tk.END, f"{host_port}:{container_port}")

    def _insert_into_list(self, param):
        if param == "":
            tk.messagebox.showerror("Error", "Parameter cannot be empty!")
        else:
            self.parameters_list.insert(tk.END, f"{param}")
            self._update_entry_point_layout()

    def _update_entry_point_layout(self):
        self.result_entry_point.config(text=f"ENTRYPOINT [{self._calculate_entry_point_string()}]")

    def _calculate_entry_point_string(self):
        entry_point_params = ''
        list_of_added_params = self.parameters_list.get(0, tk.END)
        for i in range(0, len(list_of_added_params)):
            if i < len(self.parameters_list.get(0, tk.END)) - 1:
                entry_point_params = entry_point_params + '"' + self.parameters_list.get(0, tk.END)[i] + '", '
            else:
                entry_point_params = entry_point_params + '"' + self.parameters_list.get(0, tk.END)[i] + '"'
        return entry_point_params

    def add_parameter(self, grandparent):
        add_parameter_window = InsertValueWindow(parent=self, title="Add parameter", string="Enter parameter: ",
                                                 callback=self._insert_into_list, width=grandparent.screen_width / 2,
                                                 height=grandparent.screen_height / 2)
        add_parameter_window.grab_set()

    def delete_parameters(self):
        selected_params = self.parameters_list.curselection()
        for sp in selected_params:
            self.parameters_list.delete(sp)
        self._update_entry_point_layout()

    def apply(self, grandparent):
        grandparent.coreApp.entry_point = f"[{self._calculate_entry_point_string()}]"
        self.destroy()
