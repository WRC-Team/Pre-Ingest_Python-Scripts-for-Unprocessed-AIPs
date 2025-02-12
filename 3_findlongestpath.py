import os
import sys

def find_longest_path(directory):
    longest_path = ""
    max_length = 0

    if sys.platform == "win32":
        directory = "\\\\?\\" + os.path.abspath(directory)  # Enable long path support on Windows

    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            if sys.platform == "win32":
                full_path = "\\\\?\\" + os.path.abspath(full_path)  # Ensure long path support
            
            # Store the original path for display, stripping "\\?\" prefix if present
            if sys.platform == "win32" and full_path.startswith("\\\\?\\"):
                display_path = full_path[8:]  # Remove the \\?\ prefix
            else:
                display_path = full_path
            
            if len(display_path) > max_length:
                max_length = len(display_path)
                longest_path = display_path
    
    return os.path.normpath(longest_path), max_length  # Normalize for clean output

if __name__ == "__main__":
    directory = os.getcwd()
    path, length = find_longest_path(directory)
    print(f"Longest file path: {path}\nLength: {length} characters")
