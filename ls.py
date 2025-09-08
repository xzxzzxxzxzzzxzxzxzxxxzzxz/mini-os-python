import os
import time
from pathlib import Path

def sizeof_fmt(num, suffix="B"):
    """Convert file size to human-readable format"""
    for unit in ["", "K", "M", "G", "T", "P"]:
        if abs(num) < 1024.0:
            return f"{num:.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Y{suffix}"

def get_file_color(is_dir, is_executable):
    """Return color based on file type"""
    if is_dir:
        return "\033[94m"  # Blue for directories
    elif is_executable:
        return "\033[92m"  # Green for executables
    else:
        return "\033[0m"   # Default color for regular files

def format_time(timestamp):
    """Format timestamp to readable date"""
    return time.strftime('%b %d %H:%M', time.localtime(timestamp))

def list_directory(path=".", show_hidden=False, long_format=False):
    """List directory contents with optional formatting
    
    Args:
        path (str): Directory path to list (default: current directory)
        show_hidden (bool): Whether to show hidden files (default: False)
        long_format (bool): Whether to use long listing format (default: False)
    
    Returns:
        list: List of file/directory information dictionaries
    """
    items = []
    
    # Get all items in directory
    try:
        for item in os.listdir(path):
            # Skip hidden files if not requested
            if not show_hidden and item.startswith('.'):
                continue
                
            item_path = os.path.join(path, item)
            is_dir = os.path.isdir(item_path)
            size = 0
            mod_time = 0
            
            # Get file size and modification time for long format
            if long_format:
                try:
                    if not is_dir:
                        size = os.path.getsize(item_path)
                    mod_time = os.path.getmtime(item_path)
                except OSError:
                    pass
                    
            # Check if file is executable (Unix-like systems)
            is_executable = os.access(item_path, os.X_OK) and not is_dir
            
            items.append({
                'name': item,
                'is_dir': is_dir,
                'size': size,
                'mod_time': mod_time,
                'is_executable': is_executable,
                'full_path': item_path
            })
        
        # Sort directories first, then alphabetically
        items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        
    except PermissionError:
        print(f"ls: cannot open directory '{path}': Permission denied")
        return []
    except FileNotFoundError:
        print(f"ls: cannot access '{path}': No such file or directory")
        return []
    
    return items

def print_directory_listing(items, long_format=False, path="."):
    """Print directory listing with optional long format
    
    Args:
        items (list): List of file/directory information dictionaries
        long_format (bool): Whether to use long listing format
        path (str): Path being listed (for display purposes)
    """
    if not items:
        print(f"Directory '{path}' is empty.")
        return
    
    if long_format:
        # Print in long format with details
        total_blocks = sum(os.stat(item['full_path']).st_blocks for item in items) // 2  # Approximate block count
        print(f"total {total_blocks}")
        
        for item in items:
            color_code = get_file_color(item['is_dir'], item['is_executable'])
            size = sizeof_fmt(item['size']) if not item['is_dir'] else ""
            mod_time = format_time(item['mod_time'])
            
            # Display directory with trailing slash
            name = item['name'] + "/" if item['is_dir'] else item['name']
            
            print(f"{color_code}{name:<30} {size:>8} {mod_time}\033[0m")
    else:
        # Print in simple multi-column format
        if items:
            max_len = max(len(item['name']) for item in items) + 2
            try:
                terminal_width = os.get_terminal_size().columns
                cols = max(1, terminal_width // max_len)
            except OSError:
                cols = 1  # Fallback if terminal size can't be determined
            
            for i, item in enumerate(items):
                color_code = get_file_color(item['is_dir'], item['is_executable'])
                name = item['name'] + "/" if item['is_dir'] else item['name']
                
                print(f"{color_code}{name:<{max_len}}\033[0m", end="")
                
                # New line at end of row
                if (i + 1) % cols == 0 or i == len(items) - 1:
                    print()

def ls(path=".", all_files=False, long_format=False, **kwargs):
    """Main ls function that can be imported and used in other code
    
    Args:
        path (str): Directory path to list (default: ".")
        all_files (bool): Show hidden files (default: False)
        long_format (bool): Use long listing format (default: False)
        **kwargs: Additional parameters (ignored for compatibility)
    
    Returns:
        list: List of file/directory information dictionaries or None if error
    """
    # Check if path exists
    if not os.path.exists(path):
        print(f"ls: cannot access '{path}': No such file or directory")
        return None
    
    # Check if it's a directory
    if not os.path.isdir(path):
        # It's a file, just show the file info
        color_code = get_file_color(False, os.access(path, os.X_OK))
        print(f"{color_code}{path}\033[0m")
        return [{
            'name': os.path.basename(path),
            'is_dir': False,
            'size': os.path.getsize(path),
            'mod_time': os.path.getmtime(path),
            'is_executable': os.access(path, os.X_OK),
            'full_path': path
        }]
    
    # List directory contents
    items = list_directory(path, all_files, long_format)
    print_directory_listing(items, long_format, path)
    return items

import shlex

def ls_command(args="", base_dir="."):
    """
    ls function for miniOS shell.
    args: string containing flags and path, e.g. "-a -l 'folder with spaces'"
    base_dir: the directory to use if no path is specified
    """
    # Default values
    path = base_dir
    all_files = False
    long_format = False

    # Use shlex to handle quoted paths
    try:
        args_list = shlex.split(args)
    except ValueError as e:
        print(f"Error parsing arguments: {e}")
        return

    for arg in args_list:
        if arg.startswith('-'):
            if 'a' in arg:
                all_files = True
            if 'l' in arg:
                long_format = True
            if 'h' in arg:
                print("Usage: ls [OPTION]... [FILE]...")
                print("Options:")
                print("  -a     show hidden files")
                print("  -l     long listing format")
                print("  -h     help")
                return
        else:
            # first non-flag argument is path
            path = arg

    # Call main ls function
    ls(path, all_files, long_format)


if __name__ == "__main__":
    ls_command()