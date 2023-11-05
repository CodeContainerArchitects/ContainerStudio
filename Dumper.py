import os


class Dumper:
    def __init__(self, coreApp):
        self.coreApp = coreApp
        self.file_name = ".dump_coreapp.txt"
        
    def export_coreapp(self, path):
        file_path = os.path.join(path, self.file_name)
        
        with open(file_path, 'w') as file:
            for var_name, var_value in vars(self.coreApp).items():
                file.write(f"{var_name}={var_value}\n")
        
        if os.name == 'nt':
            os.system(f"attrib +h {file_path}")

    def import_coreapp(self, path):
        file_path = os.path.join(path, self.file_name)
        
        with open(file_path, 'r') as file:
            for line in file:
                var_name, var_value = line.strip().split("=")
                setattr(self.coreApp, var_name, var_value)
        
        for var_name, var_value in vars(self.coreApp).items():
            print(f"{var_name}: {var_value}")