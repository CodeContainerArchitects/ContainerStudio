import tkinter as tk
from tkinter import ttk
import os

class TreeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.window_width = 600
        self.window_height = 400
        self.padding = 5
        
        self.title("Project directory tree")
        center_x = int(parent.screen_width/2 - self.window_width / 2)
        center_y = int(parent.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        treeframe = tk.Frame(self)
        
        self.treeview = ttk.Treeview(treeframe,height=15, show='tree')
        scrollbar = ttk.Scrollbar(treeframe, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        self.directory = parent.projectTree.get_working_directory()
        self.treeview.heading('#0', text='Dir:' + self.directory, anchor='w')
        
        self.build_tree()
        
        buttonframe = tk.Frame(self)
        
        # uploading files
        choose_file_button = tk.Button(buttonframe, text="Add file", command=lambda: self.add_files(parent,mode='file'))
        choose_folder_button = tk.Button(buttonframe, text="Add folder", command=lambda: self.add_files(parent, mode='dir'))
        delete_items_button = tk.Button(buttonframe, text="Delete selected items", command=lambda: self.delete_selected_items(parent))
        exit_button = tk.Button(buttonframe, text="Exit", command=self.destroy)
        
        scrollbar.pack(side="right", fill="y")
        self.treeview.pack(fill='both')
        treeframe.pack(side=tk.TOP, fill = 'both')
        choose_file_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        choose_folder_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        delete_items_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        exit_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
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
    
    def update_tree(self):
        # clear all items in the tree
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        self.build_tree()
        
    def delete_selected_items(self, parent):
        selected_items = []
        for item in self.treeview.selection():
            parent_iid = self.treeview.parent(item)
            node = []
            while parent_iid!= '':
                node.insert(0, self.treeview.item(parent_iid)["text"])
                parent_iid = self.treeview.parent(parent_iid)
            i = self.treeview.item(item, "text")
            path = os.path.join(*node, i)
            selected_items.append(path)
            
        # print(selected_items)
        parent.projectTree.delete_files_from_directory(selected_items)
        self.update_tree()
    
    def add_files(self, parent, mode):
        parent.projectTree.select_files(parent, mode)
        self.update_tree()
        