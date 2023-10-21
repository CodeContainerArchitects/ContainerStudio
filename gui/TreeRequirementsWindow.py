import tkinter as tk
from tkinter import ttk
import os


class TreeRequirementsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # window properties
        self.title("Add requirements")
        self.window_width = 600
        self.window_height = 400
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 5
        center_x = int(self.screen_width / 2 - self.window_width / 2)
        center_y = int(self.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        treeframe = tk.Frame(self)
        self.treeview = ttk.Treeview(treeframe, height=15, show='tree')
        scrollbar = ttk.Scrollbar(treeframe, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        self.directory = parent.directory
        self.treeview.heading('#0', text='Dir:' + self.directory, anchor='w')

        self.build_tree()

        buttonframe = tk.Frame(self)

        # uploading files
        apply_button = tk.Button(buttonframe, text="Apply", command=lambda: self.apply(parent))
        cancel_button = tk.Button(buttonframe, text="Cancel", command=self.destroy)

        scrollbar.pack(side="right", fill="y")
        self.treeview.pack(fill='both')
        treeframe.pack(side=tk.TOP, fill='both')
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        buttonframe.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def build_tree(self):
        path = os.path.abspath(self.directory)
        node = self.treeview.insert('', 'end', text=path, open=True)
        self.traverse_dir(node, path)

    def traverse_dir(self, parent, path):
        for dir in os.listdir(path):
            full_path = os.path.join(path, dir)
            isdir = os.path.isdir(full_path)
            id = self.treeview.insert(parent, 'end', text=dir, open=False)
            if isdir:
                self.traverse_dir(id, full_path)

    def apply(self, parent):
        selected_items = []
        for item in self.treeview.selection():
            parent_iid = self.treeview.parent(item)
            node = []
            while parent_iid != '':
                node.insert(0, self.treeview.item(parent_iid)["text"])
                parent_iid = self.treeview.parent(parent_iid)
            i = self.treeview.item(item, "text")
            path = os.path.join(*node, i)
            selected_items.append(path)

        for item in selected_items:
            parent.add_to_list_requirements(item)
        self.destroy()
