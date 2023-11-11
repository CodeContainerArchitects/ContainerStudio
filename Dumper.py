import os
import json

class Dumper:
    def __init__(self, coreApp, file_name):
        self.coreApp = coreApp
        self.file_name = file_name
        
    def export_coreapp(self, path):
        file_path = os.path.join(path, self.file_name)
        
        data = {}
        
        for var_name, var_value in vars(self.coreApp).items():
            if isinstance(var_value, dict):
                var_value = {k: str(v) if isinstance(v, int) else v for k, v in var_value.items()}
            data[var_name] = var_value
            #file.write(f"{var_name}={var_value}\n")
        
        with open(file_path, 'w') as file:
            json.dump(data, file)
        
        if os.name == 'nt':
            os.system(f"attrib +h {file_path}")

    def import_coreapp(self, path):
        file_path = os.path.join(path, self.file_name)
        
        with open(file_path, 'r') as file:
            print("importing")
            data = json.load(file)
            for var_name, var_value in data.items():
                if isinstance(var_value, dict):
                    if var_name != "apt_packages" and var_name != "pip_packages":
                        var_value = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in var_value.items()}
                setattr(self.coreApp, var_name, var_value)
                
        for var_name, var_value in vars(self.coreApp).items():
            print(f"{var_name}={var_value}")