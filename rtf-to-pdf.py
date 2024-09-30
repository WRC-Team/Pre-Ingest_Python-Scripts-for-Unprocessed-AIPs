import os
from datetime import datetime
from win32com import client

def is_rtf_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as f:
        # Read the first few characters to determine if it starts with RTF magic number
        magic_number = f.read(5)
        # Check if it starts with "{\rtf"
        return magic_number == "{\\rtf"

def convert_rtf_to_pdf(input_folder):
    # Create COM object for Word application
    word = client.Dispatch("Word.Application")
    
    # Disable visibility to speed up the process
    word.Visible = False

    # List to store error messages
    error_messages = []

    # Function to recursively traverse folders and convert RTF files to PDF
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
                if is_rtf_file(file_path):
                    try:
                        # Open RTF file
                        doc = word.Documents.Open(file_path)

                        # Get filename and extension separately
                        file_name, file_extension = os.path.splitext(filename)

                        # Set output filename
                        output_filename = f"{file_name}_RTF.pdf"
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
    report_file = os.path.join(input_folder, f"conversion_report_rtf_{timestamp}.txt")
    with open(report_file, "w") as f:
        if error_messages:
            f.write("\n".join(error_messages))
        else:
            f.write("No errors encountered during conversion.")

 # Specify input folder
input_folder = os.getcwd()

# Convert RTF files to PDF
convert_rtf_to_pdf(input_folder)
