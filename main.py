import jinja2
import subprocess

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
template = environment.get_template("template-dockerfile.txt")

OS_image="ubuntu"
OS_image_version="latest"
message = "testing message 123"
items = ["Jinja2", "PyPDF2", "click"]
content = template.render(OS_image=OS_image,
                          OS_image_version=OS_image_version,
                          packages_to_install=items)


with open("outputs/Dockerfile", "w") as file:
    file.write(content)

print(content)

print("Try to run Dockerfile")
subprocess.call(["bash", "scripts/dockerfile_runner.sh"])

