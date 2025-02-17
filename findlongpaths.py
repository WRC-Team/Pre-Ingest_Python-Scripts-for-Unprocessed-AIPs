import os
import csv

def find_long_paths(directory, length_limit=256, output_file="long_paths.csv"):
    long_paths = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if len(file_path) >= length_limit:
                long_paths.append((file_path, len(file_path)))
    
    if long_paths:
        with open(output_file, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["File Path", "Length"])
            writer.writerows(long_paths)
        print(f"Found {len(long_paths)} long file paths. Saved to {output_file}.")
    else:
        print("No file paths exceed the limit.")

if __name__ == "__main__":
    current_directory = os.getcwd()
    find_long_paths(current_directory)
