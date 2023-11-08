import subprocess
from gui.MainApp import App
from CoreApp import CoreApp
from createUtils.DockerfileGenerator import DockerfileGenerator

# print("Try to run Dockerfile")
# subprocess.call(["bash", "scripts/dockerfile_runner.sh"])

if __name__ == "__main__":
    coreApp = CoreApp()
    main_window = App(coreApp)
    main_window.protocol("WM_DELETE_WINDOW", main_window.on_closing)
    main_window.mainloop()
