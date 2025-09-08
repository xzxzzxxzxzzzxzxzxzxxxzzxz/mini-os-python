import os

def cd_command(path, current_dir):
    """
    Change the current directory.
    
    Args:
        path (str): Directory to change to (can be relative or absolute)
        current_dir (str): The current working directory
    
    Returns:
        str: The new current directory (or same as current_dir if invalid)
    """
    # If path is empty, go to home directory
    if not path:
        path = os.path.expanduser("~")

    # Make path absolute relative to current_dir
    new_path = os.path.abspath(os.path.join(current_dir, path))

    # Check if directory exists
    if not os.path.isdir(new_path):
        print(f"cd: no such directory: {path}")
        return current_dir

    return new_path
