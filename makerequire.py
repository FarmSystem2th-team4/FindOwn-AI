import os

def install_packages(requirements_file):
    with open(requirements_file, 'r') as file:
        packages = file.readlines()

    for package in packages:
        package = package.strip()
        try:
            print(f"Installing {package}")
            os.system(f"pip install {package}")
        except Exception as e:
            print(f"Failed to install {package}: {e}")

if __name__ == "__main__":
    install_packages("new_requirement.txt")

