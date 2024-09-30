from win32com import client
import os
from datetime import datetime
import time

def is_word_file(file_path):
    # Get the file extension
    file_extension = os.path.splitext(file_path)[1].lower()

    # Check if the file has a .doc or .docx extension
    if file_extension in ['.doc', '.docx'] or file_extension == '':
        with open(file_path, 'rb') as f:
            # Read the first few bytes to determine the file type
            magic_number = f.read(4)
            # Check if it matches the magic numbers for DOC or DOCX
            if file_extension == '.doc' or file_extension == '':
                if magic_number == b'\xD0\xCF\x11\xE0':  # Check for DOC magic number
                    return True
            if file_extension == '.docx' or file_extension == '':
                if magic_number == b'PK\x03\x04':  # Check for DOCX magic number
                    return True

    return False  # If the file is not a recognized Word file

def open_file_with_timeout(word, file_path, timeout=10):
    start_time = time.time()
    document = None
    
    while True:
        try:
            document = word.Documents.Open(file_path)
            break  # Exit loop if document is successfully opened
        except Exception as e:
            print(f"Error opening {file_path}: {e}")
            return None
        
        # Check if we have exceeded the timeout
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            print(f"Skipping likely false flag ({file_path}) due to long opening time.")
            return None

        # Give a small delay before retrying
        time.sleep(1)

    return document

def convert_word_to_pdf(input_folder):
    # Create COM object for Word application
    word = client.Dispatch("Word.Application")
    
    # Disable visibility to speed up the process
    word.Visible = False

    # List to store error messages
    error_messages = []

    # Function to recursively traverse folders and convert Word files to PDF
    def convert_files(folder):
        for filename in os.listdir(folder):
            if filename.startswith('.') or filename.lower() == 'thumbs.db':
                continue  # Skip hidden files and Thumbs.db
            file_path = os.path.join(folder, filename)
            
            if os.path.isdir(file_path):
                # If it's a directory, recursively call the function
                convert_files(file_path)
            elif os.path.isfile(file_path):
                # Check if it's a regular file
                if is_word_file(file_path):
                    # Check if the output file already exists
                    file_name, _ = os.path.splitext(filename)
                    output_filename = f"{file_name}_Word.pdf"
                    output_path = os.path.join(folder, output_filename)
                    
                    if os.path.exists(output_path):
                        print(f"Skipping {output_filename} (already exists).")
                        continue

                    try:
                        # Attempt to open the file with a timeout
                        doc = open_file_with_timeout(word, file_path)
                        if doc is None:
                            continue

                        # Set output filename
                        output_path = os.path.join(folder, output_filename)

                        # Save as PDF
                        doc.SaveAs2(output_path, FileFormat=17)  # 17 is for PDF format
                        
                        # Print a message when a file is converted
                        print(f"Converted {filename} to PDF.")

                        # Close the document
                        doc.Close()
                    except Exception as e:
                        # Store error message in the list
                        error_messages.append(f"Error converting {filename}: {e}")
                        continue

    # Start converting files from the input folder
    convert_files(input_folder)

    # Quit Word application
    word.Quit()

    # Write error messages to a timestamped text file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = os.path.join(input_folder, f"conversion_report_{timestamp}.txt")
    with open(report_file, "w") as f:
        if error_messages:
            f.write("\n".join(error_messages))
        else:
            f.write("No errors encountered during conversion.")

# Specify input folder
input_folder = os.getcwd()

# Convert Word files to PDF
convert_word_to_pdf(input_folder)
