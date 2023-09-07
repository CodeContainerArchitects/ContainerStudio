import tkinter as tk
import add_files
from createUtils.generate_dockerfile import generate_dockerfile


root = tk.Tk()

# set properties of the window
root.title("Code Container")

window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# select folder
select_folder_button = tk.Button(root, text = "Select folder", command = lambda:add_files.select_working_directory())

# uploading files
choose_file_button = tk.Button(root, text = "Choose file", command = lambda:add_files.select_files(root,mode='file'))
choose_folder_button = tk.Button(root, text = "Choose folder", command = lambda:add_files.select_files(root, mode='dir'))


send_button = tk.Button(root, text = "Generate Dockerfile", command=lambda:generate_dockerfile())
exit_button = tk.Button(root, text = "Exit", command = root.destroy)

select_folder_button.pack()
choose_file_button.pack()
choose_folder_button.pack()
send_button.pack()
exit_button.pack()

root.mainloop()