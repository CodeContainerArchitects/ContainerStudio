import tkinter as tk
from gui.attributes.InsertDoubleValueWindow import InsertDoubleValueWindow


class AddVolumesWindow(tk.Toplevel):
    def __init__(self, parent, grandparent):
        super().__init__(parent)
        self.window_width = 600
        self.window_height = 400
        self.padding = 5
        self.title("Manage volumes")
        center_x = int(grandparent.screen_width / 2 - self.window_width / 2)
        center_y = int(grandparent.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        # properties
        self.volumes_list = tk.Listbox(self, height=6, selectmode=tk.SINGLE)
        volumes_label = tk.Label(self, text="Volumes: \n")

        button_frame_upper = tk.Frame(self)
        add_volume_button = tk.Button(button_frame_upper, text="Add volume", command=lambda: self.add_volume(grandparent=grandparent))
        delete_volume_button = tk.Button(button_frame_upper, text="Delete volume", command=lambda: self.delete_volume())

        button_frame_lower = tk.Frame(self)
        cancel_button = tk.Button(button_frame_lower, text="Cancel", command=self.destroy)
        apply_button = tk.Button(button_frame_lower, text="Apply", command=lambda: self.apply(grandparent=grandparent))

        volumes_label.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.volumes_list.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        button_frame_upper.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        add_volume_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        delete_volume_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

        for host_port, container_port in grandparent.coreApp.volumes.items():
            self.volumes_list.insert(tk.END, f"{host_port}:{container_port}")

    def insert_into_list(self, container_path, host_path):
        if container_path and host_path:
            if f"{host_path}:{container_path}" not in self.volumes_list.get(0, tk.END):
                self.volumes_list.insert(tk.END, f"{host_path}:{container_path}")
            else:
                tk.messagebox.showerror("Error", "Volume already exists.")
                return
        else:
            tk.messagebox.showerror("Error", "Container path and host path have to be specified!")
            return

    def add_volume(self, grandparent):
        volume_window = InsertDoubleValueWindow(parent=self, title="Enter volume values", string1="Enter container path: ",
                                                string2="Enter host path:", callback=self.insert_into_list,
                                                width=grandparent.screen_width / 2, height=grandparent.screen_height / 2)
        volume_window.grab_set()

    def delete_volume(self):
        selected_params = self.volumes_list.curselection()
        for sp in selected_params:
            self.volumes_list.delete(sp)

    def apply(self, grandparent):
        result = self.volumes_list.get(0, tk.END)
        volumes = {}
        for r in result:
            r = r.split(":")
            volumes[r[0]] = r[1]
        print(volumes)
        grandparent.coreApp.set_volumes(volumes)
        print(grandparent.coreApp.volumes)
        self.destroy()
