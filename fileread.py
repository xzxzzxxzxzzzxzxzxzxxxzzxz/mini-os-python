import os

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P"]:
        if abs(num) < 1024.0:
            return f"{num:.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Y{suffix}"

def list_files(path="."):
    files = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            files.append((filename, sizeof_fmt(size)))
    return files

def file_selector():
    files = list_files(".")
    if not files:
        print("No files found.")
        return
    
    # Display numbered file list
    print("\nFiles in current directory:\n")
    for i, (filename, size) in enumerate(files, start=1):
        print(f"{i}. {filename} ({size})")
    
    # User picks a file
    choice = input("\nSelect a file number: ")
    if not choice.isdigit() or not (1 <= int(choice) <= len(files)):
        print("Invalid choice.")
        return
    
    selected_file = files[int(choice) - 1][0]
    print(f"\nYou selected: {selected_file}")
    
    with open(selected_file, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            print(f"{i:03}. {line.rstrip()}")

if __name__ == "__main__":
    file_selector()