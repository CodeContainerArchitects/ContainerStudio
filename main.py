import subprocess
from gui import App


#print("Try to run Dockerfile")
# subprocess.call(["bash", "scripts/dockerfile_runner.sh"])

if __name__ == "__main__":
    main_window = App()
    main_window.mainloop()
