import tkinter as tk
from tkinter import ttk
from add_files import select_files, select_working_directory, get_working_directory, delete_files_from_directory
from createUtils.generate_dockerfile import DockerfileGenerator
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
        self.directory = get_working_directory()
        self.treeview.heading('#0', text='Dir:' + self.directory, anchor='w')
        
        self.build_tree()
        
        buttonframe = tk.Frame(self)
        
        # uploading files
        choose_file_button = tk.Button(buttonframe, text = "Choose file", command = lambda:self.add_files(parent,mode='file'))
        choose_folder_button = tk.Button(buttonframe, text = "Choose folder", command = lambda:self.add_files(parent, mode='dir'))
        delete_items_button = tk.Button(buttonframe, text = "Delete selected items", command = lambda:self.delete_selected_items())
        exit_button = tk.Button(buttonframe, text = "Exit", command = self.destroy)
        
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
        node=self.treeview.insert('', 'end', text=path, open=True)
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
        
    def delete_selected_items(self):
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
            
        #print(selected_items)
        
        delete_files_from_directory(selected_items)
        
        self.update_tree()
    
    def add_files(self, root, mode):
        select_files(root, mode)
        self.update_tree()


class App(tk.Tk):
    def __init__(self, dockerfile_generator):
        super().__init__()
        
        self.dockerfile_generator = dockerfile_generator
        
        # set properties of the window
        self.title("Code Container")
        
        self.window_width = 600
        self.window_height = 400
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.padding = 5
        
        center_x = int(self.screen_width/2 - self.window_width / 2)
        center_y = int(self.screen_height/2 - self.window_height / 2)
        
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        self.project_files_folder = "Project_files"
        
        mainframe = tk.Frame(self, width=self.window_width, height=self.window_height, background="#B9B4C7")
        buttonframe = tk.Frame(mainframe, background="#B9B4C7")
        
        #select folder 
        select_folder_button = tk.Button(buttonframe, text = "Select folder",  command = lambda:self.select_working_directory())
        
        #opens a new window 
        self.project_tree_button = tk.Button(buttonframe, text = "Show project tree", state=tk.DISABLED, command = lambda:self.open_tree_window())
        
        send_button = tk.Button(buttonframe, text = "Generate Dockerfile", command=lambda:self.dockerfile_generator.generate_dockerfile())
        exit_button = tk.Button(buttonframe, text = "Exit", command = self.destroy)
        
        mainframe.pack(side=tk.TOP)
        buttonframe.pack(expand=True)
        mainframe.pack_propagate(0)
        
        select_folder_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        self.project_tree_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        send_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        exit_button.pack(pady=self.padding, side=tk.TOP, fill='x')
        
    def open_tree_window(self):
        tree_window = TreeWindow(self)
        #grab_set prevents user from interacting with main window and makes the tree window receive events
        tree_window.grab_set()
        
    def select_working_directory(self):
        select_working_directory()
        working_directory = get_working_directory()
        
        if working_directory != '' and self.project_tree_button['state'] == tk.DISABLED:
            self.project_tree_button['state'] = tk.NORMAL