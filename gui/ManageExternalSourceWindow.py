import tkinter as tk

from gui.InsertListData import InsertListData
from gui.attributes.InsertValueWindow import InsertValueWindow


class ManageExternalSourceWindow(tk.Toplevel):
    def __init__(self, parent, grandparent):
        super().__init__(parent)

        # variables
        self.parent = parent
        self.grandparent = grandparent
        self.links_properties = []

        # window properties
        self.window_width = 800
        self.window_height = 500
        self.padding = 10
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.title("Manage external sources window")
        center_x = int(self.screen_width / 2 - self.window_width / 2)
        center_y = int(self.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        # lists
        links_list_label = tk.Label(self, text="Links:")
        self.links_list = tk.Listbox(self, height=6, selectmode=tk.SINGLE)
        packages_list_label = tk.Label(self, text="Packages:")
        self.packages_list = tk.Listbox(self, height=6, selectmode=tk.SINGLE)

        # buttons
        button_frame_link = tk.Frame(self)
        button_frame_package = tk.Frame(self)
        button_frame = tk.Frame(self)
        add_link_button = tk.Button(button_frame_link, text="Add link", command=lambda: self.add_to_list(mode="link"))
        delete_link_button = tk.Button(button_frame_link, text="Delete link", command=lambda: self.delete_from_list(mode="link"))
        add_package_button = tk.Button(button_frame_package, text="Add package", command=lambda: self.add_to_list(mode="package"))
        delete_package_button = tk.Button(button_frame_package, text="Delete package", command=lambda: self.delete_from_list(mode="package"))
        apply_button = tk.Button(button_frame, text="Apply", command=lambda: self.apply())
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.destroy)

        # packing
        links_list_label.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.links_list.pack(side=tk.TOP, pady=self.padding, fill='both')
        packages_list_label.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.packages_list.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame.pack(side=tk.BOTTOM, fill='both')
        button_frame_package.pack(side=tk.BOTTOM, fill='both')
        button_frame_link.pack(side=tk.BOTTOM, fill='both')
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        add_link_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        delete_link_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        add_package_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        delete_package_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

        # restore
        for element in self.grandparent.coreApp.external_lists_links:
            self.links_properties.append(element)
        for element in self.links_properties:
            self.links_list.insert(tk.END, f"{element['name']} ({element['link']})")
        for element in self.grandparent.coreApp.external_lists_packages:
            self.packages_list.insert(tk.END, element)

        print(f"Links: {self.grandparent.coreApp.external_lists_links}")
        print(f"Packages: {self.grandparent.coreApp.external_lists_packages}")

    def _add_link(self, link, cert, name, pool, radiobutton_value):
        element = {"link": link, "cert": cert, "name": name, "pool": pool, "radiobutton_value": radiobutton_value}
        if_link_exists = False
        for item in self.links_properties:
            if item['link'] == link:
                if_link_exists = True
        if not if_link_exists:
            self.links_list.insert(tk.END, f"{element['name']} ({element['link']})")
            self.links_properties.append(element)
        else:
            tk.messagebox.showwarning("Warning", "Such link already added.")

    def _add_package(self, element):
        if element == "":
            tk.messagebox.showerror("Error", "Package name cannot be empty!")
        elif element in self.packages_list.get(0, tk.END):
            tk.messagebox.showwarning("Warning", "Package already added.")
        else:
            self.packages_list.insert(tk.END, element)

    def add_to_list(self, mode):
        if mode == 'link':
            entry_window = InsertListData(parent=self, title="Add link", label1="Enter link to the list: ", label2="Enter link to the certificate: ", label3="Enter list name:", label4="Enter pool: ",
                                          callback=self._add_link, width=self.parent.screen_width / 2, height=self.parent.screen_height / 2, radio_title="Do you need to add os name and pool?", radio_options=[["Yes", 1], ["No", 2]])
            entry_window.grab_set()
        if mode == 'package':
            entry_window = InsertValueWindow(parent=self, title="Add package", string="Enter package: ", callback=self._add_package,
                                             width=self.grandparent.screen_width / 2,
                                             height=self.grandparent.screen_height / 2)
            entry_window.grab_set()

    def delete_from_list(self, mode):
        if mode == 'link':
            selected = self.links_list.curselection()
            for sp in selected:
                value = self.links_list.get(sp)
                self.links_list.delete(sp)
                helper = []
                for item in self.links_properties:
                    if item['link'] != value.split(' ')[1].replace('(', '').replace(')', ''):
                        helper.append(item)
                self.links_properties = helper
        if mode == 'package':
            selected = self.packages_list.curselection()
            for sp in selected:
                self.packages_list.delete(sp)

    def apply(self):
        self.grandparent.coreApp.external_lists_links = self.links_properties
        self.grandparent.coreApp.external_lists_packages = []
        for item in self.packages_list.get(0, tk.END):
            self.grandparent.coreApp.external_lists_packages.append(item)
        self.destroy()
