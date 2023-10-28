import tkinter as tk

from gui.attributes.InsertDoubleValueWindow import InsertDoubleValueWindow
from gui.attributes.InsertValueWithRadioWIndow import InsertValueWithRadioWindow


class AddCommandsWindow(tk.Toplevel):
    def __init__(self, parent, grandparent):
        super().__init__(parent)
        self.window_width = 600
        self.window_height = 400
        self.padding = 5

        # variables
        self.before_or_after_files = "<adding dependencies and files>"
        self.switch_user_index = 0

        # window attributes
        self.title("Add commands")
        center_x = int(grandparent.screen_width / 2 - self.window_width / 2)
        center_y = int(grandparent.screen_height / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        label_for_added_commands_list = tk.Label(self, text="Commands: \n")
        self.added_commands_list = tk.Listbox(self, height=13)

        # buttons
        button_frame_upper = tk.Frame(self)
        add_command_button = tk.Button(button_frame_upper, text="Add command", command=lambda: self.add(grandparent=grandparent))
        insert_command_button = tk.Button(button_frame_upper, text="Insert command", command=lambda: self.insert(grandparent=grandparent))
        delete_command_button = tk.Button(button_frame_upper, text="Delete command", command=lambda: self.delete())
        switch_user_button = tk.Button(button_frame_upper, text="Switch user", command=lambda: self.switch_user(grandparent=grandparent))

        button_frame_lower = tk.Frame(self)
        apply_button = tk.Button(button_frame_lower, text="Apply", command=lambda: self.apply(grandparent=grandparent))
        cancel_button = tk.Button(button_frame_lower, text="Cancel", command=self.destroy)

        label_for_added_commands_list.pack(side=tk.TOP, pady=self.padding, fill='both')
        self.added_commands_list.pack(side=tk.TOP, pady=self.padding, fill='both')
        button_frame_lower.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        button_frame_upper.pack(side=tk.BOTTOM, pady=self.padding, fill='both')
        add_command_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        insert_command_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        switch_user_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        delete_command_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        apply_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)
        cancel_button.pack(side=tk.LEFT, pady=self.padding, fill='x', expand=True)

        # self.ports = grandparent.coreApp.get_expose_ports()
        # for host_port, container_port in self.ports.items():
        #     if host_port == f"-{container_port}":
        #         self.ports_list.insert(tk.END, f":{container_port}")
        #     else:
        #         self.ports_list.insert(tk.END, f"{host_port}:{container_port}")

    def _add_command(self, command, if_with_files):
        if command == "":
            tk.messagebox.showerror("Error", "Command cannot be empty!")
            return
        if len(self.added_commands_list.get(0, tk.END)) == 0:
            self.added_commands_list.insert(tk.END, self.before_or_after_files)

        # when command will use files it will be added after the before_or_after_files
        if if_with_files == 1:
            self.added_commands_list.insert(tk.END, "RUN " + command)
        elif if_with_files == 2:
            index = self._find_index_of_files()
            self.added_commands_list.insert(index, "RUN " + command)

    def _find_index_of_files(self):
        index = 0
        added_commands = self.added_commands_list.get(0, tk.END)
        for i in range(0, len(added_commands)):
            if added_commands[i] == self.before_or_after_files:
                index = i
                break
        return index

    def add(self, grandparent):
        add_command_window = InsertValueWithRadioWindow(parent=self, title="Enter command", string="Enter command: ", callback=self._add_command,
                                                        width=grandparent.screen_width / 2, height=grandparent.screen_height / 2, radio_title="Does command use files?", radio_options=[["Yes", 1], ["No", 2]])
        add_command_window.grab_set()

    def delete(self):
        selected_params = self.added_commands_list.curselection()
        for sp in selected_params:
            if self.added_commands_list.get(sp) != self.before_or_after_files:
                self.added_commands_list.delete(sp)
        if len(self.added_commands_list.get(0, tk.END)) == 1:
            self.added_commands_list.delete(0)

    def _insert_command(self, index, command):
        self.added_commands_list.insert(index, "RUN " + command)

    def insert(self, grandparent):
        if len(self.added_commands_list.get(0, tk.END)) == 0:
            self.add(grandparent=grandparent)
        else:
            insert_window = InsertDoubleValueWindow(parent=self, title="Insert command", string1="Index:", string2="Command:",
                                                    callback=self._insert_command, width=grandparent.screen_width / 2, height=grandparent.screen_height / 2)
            insert_window.grab_set()

    @staticmethod
    def _check_if_int(variable):
        try:
            return int(variable)
        except ValueError:
            return variable

    def _switch_user_command(self, user_uid, group_gid):
        user_uid = self._check_if_int(user_uid)
        group_gid = self._check_if_int(group_gid)
        if user_uid and group_gid:
            if (isinstance(user_uid, str) and isinstance(group_gid, str)) or (isinstance(user_uid, int) and isinstance(group_gid, int)):
                self.added_commands_list.insert(self.switch_user_index, "USER " + str(user_uid) + ":" + str(group_gid))
            else:
                tk.messagebox.showerror("Error", "Only combination user-group and UID-GID can be used together.")
        elif user_uid:
            self.added_commands_list.insert(self.switch_user_index, "USER " + str(user_uid))
        else:
            tk.messagebox.showerror("Error", "User(UID) cannot be empty. Only group(GID) is optional.")

    def switch_user(self, grandparent):
        self.switch_user_index = self.added_commands_list.curselection()[0]
        switch_user_window = InsertDoubleValueWindow(parent=self, title="Switch user", string1="User (or UID): ", string2="Group (or GID):",
                                                     callback=self._switch_user_command, width=grandparent.screen_width / 2, height=grandparent.screen_height / 2)
        switch_user_window.grab_set()

    def apply(self, grandparent):
        grandparent.coreApp.set_expose_ports(self.ports)
        self.destroy()
