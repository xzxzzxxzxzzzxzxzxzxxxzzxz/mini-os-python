import os

current_dir = os.getcwd()

def ls():
    for file in os.listdir(current_dir):
        print(file)

def cd(path):
    global current_dir
    try:
        os.chdir(path)
        current_dir = os.getcwd()
    except FileNotFoundError:
        print("Directory not found")