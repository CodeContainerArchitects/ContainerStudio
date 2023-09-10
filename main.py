import subprocess
from gui import App
from CoreApp import CoreApp
from createUtils.generate_dockerfile import DockerfileGenerator

#print("Try to run Dockerfile")
# subprocess.call(["bash", "scripts/dockerfile_runner.sh"])

if __name__ == "__main__":
    coreApp = CoreApp()
    generator = DockerfileGenerator(coreApp)
    main_window = App(generator)
    main_window.mainloop()
