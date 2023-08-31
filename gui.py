import tkinter as tk
from tkinter import ttk
from add_files import select_files, select_working_directory, get_working_directory, delete_files_from_directory, get_project_files_folder
from generate_dockerfile import generate_dockerfile
import os

class TreeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.window_width = 600
        self.window_height = 400

        
        self.title("Project directory tree")
        center_x = int(parent.screen_width/2 - self.window_width / 2)
        center_y = int(parent.screen_height/2 - self.window_height / 2)

        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        treeframe = tk.Frame(self)

        self.treeview = ttk.Treeview(treeframe, show='tree')
        scrollbar = ttk.Scrollbar(treeframe, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        self.directory = get_working_directory()
        self.treeview.heading('#0', text='Dir:' + self.directory, anchor='w')
        
        self.build_tree()
        
        # uploading files
        choose_file_button = tk.Button(self, text = "Choose file", command = lambda:self.add_files(parent,mode='file'))
        choose_folder_button = tk.Button(self, text = "Choose folder", command = lambda:self.add_files(parent, mode='dir'))
        delete_items_button = tk.Button(self, text = "Delete selected items", command = lambda:self.delete_selected_items())
        exit_button = tk.Button(self, text = "Exit", command = self.destroy)
        
        scrollbar.pack(side="right", fill="y")
        self.treeview.pack()
        treeframe.pack()
        choose_file_button.pack()
        choose_folder_button.pack()
        delete_items_button.pack()
        exit_button.pack()
        
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
            item = self.treeview.item(item)
            selected_items.append(item["text"])
        
        delete_files_from_directory(selected_items)
        
        for item in self.treeview.selection():
            self.treeview.delete(item)
            
    def add_files(self, root, mode):
        select_files(root, mode)
        self.update_tree()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # set properties of the window
        self.title("Code Container")

        self.window_width = 1080
        self.window_height = 720
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        center_x = int(self.screen_width/2 - self.window_width / 2)
        center_y = int(self.screen_height/2 - self.window_height / 2)

        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        
        self.project_files_folder = "Project_files"
        
        project_files_name_label = tk.Label(self, text = "Input the name of the project files folder:")
        self.project_files_name = tk.Text(self, width = 20, height = 1)
        #select folder 
        select_folder_button = tk.Button(self, text = "Select folder", command = lambda:self.select_working_directory())
        
        #opens a new window 
        self.project_tree_button = tk.Button(self, text = "Show project tree", state=tk.DISABLED, command = lambda:self.open_tree_window())

        send_button = tk.Button(self, text = "Generate Dockerfile", command=lambda:generate_dockerfile())
        exit_button = tk.Button(self, text = "Exit", command = self.destroy)

        project_files_name_label.pack()
        self.project_files_name.pack()
        select_folder_button.pack()
        self.project_tree_button.pack()
        send_button.pack()
        exit_button.pack()
        
        self.project_files_name.insert(tk.END, self.project_files_folder)
        
    def open_tree_window(self):
        treeWindow = TreeWindow(self)
        #grab_set prevents user from interacting with main window and makes the tree window receive events
        treeWindow.grab_set()
        
    def select_working_directory(self):
        select_working_directory(self.project_files_name.get(1.0, 'end-1c'))
        working_directory = get_working_directory()
        
        if working_directory != '' and self.project_tree_button['state'] == tk.DISABLED:
            self.project_tree_button['state'] = tk.NORMAL
