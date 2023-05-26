import jinja2

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
template = environment.get_template("template-dockerfile.txt")

OS_image="ubuntu"
OS_image_version="latest"
message = "testing message 123"
content = template.render(OS_image=OS_image,
                          OS_image_version=OS_image_version,
                          Echo_message=message)

print(content)