import os


def _find_requirements(path):
    for root, dirs, files in os.walk(path):
        if 'requirements.txt' in files:
            return os.path.join(root, 'requirements.txt')
    return None


def use_requirements(path):
    result = _find_requirements(path=path)
    if result:
        print(f"Found requirements.txt at: {result}")
        user_choice = input('Do you want to use found requirements.txt in a Dockerfile? y/n \n')
        if user_choice == 'y' or user_choice == 'yes':
            return result
        else:
            return None
    else:
        print("File requirements.txt not found in the specified directory.")
        return None
