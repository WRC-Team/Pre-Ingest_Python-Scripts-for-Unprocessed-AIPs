import os
import pandas as pd
from datetime import datetime

def analyze_droid_csv(csv_file):
    """
    Function to analyze a DROID CSV file and generate a report of unique identifiers, their corresponding format names (if available), and whether they are good or bad PRONOM IDs.
    """
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Replace empty values in PUID and FORMAT_NAME columns with appropriate placeholders
    df['PUID'].fillna("(none)", inplace=True)
    df['FORMAT_NAME'].fillna("(none given)", inplace=True)

    # Group by PUID and FORMAT_NAME columns and count occurrences
    grouped = df.groupby(['PUID', 'FORMAT_NAME']).size().reset_index(name='count')

    # Load good PRONOM IDs from file
    normal_formats = set()
    with open("normal_formats.txt", "r") as f:
        for line in f:
            normal_formats.add(line.strip())

    # Create a timestamp for the report file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = f"report_{timestamp}.txt"

    # Write report to the report file
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("Report:\n")
        f.write("{:<20} {:<40} {:<10} {:<10}\n".format("PUID", "FORMAT_NAME", "COUNT", "WILL AM NORMALIZE?"))
        f.write("-" * 70 + "\n")
        for index, row in grouped.iterrows():
            format_status = "Yes" if row['FORMAT_NAME'] in normal_formats else "No"
            f.write("{:<20} {:<40} {:<10} {:<10}\n".format(row['PUID'], row['FORMAT_NAME'], row['count'], format_status))

        # Add a section for "Other Formats"
        f.write("\nOther Formats:\n")
        f.write("{:<40} {:<10}\n".format("FORMAT_NAME", "COUNT"))
        f.write("-" * 50 + "\n")
        
        # Count items where PUID and FORMAT_NAME are empty, but EXT is not
        other_formats = df[(df['PUID'] == "(none)") & (df['FORMAT_NAME'] == "(none given)") & (df['EXT'].notnull())]
        other_formats_grouped = other_formats.groupby('EXT').size().reset_index(name='count')
        for index, row in other_formats_grouped.iterrows():
            f.write("{:<40} {:<10}\n".format(row['EXT'], row['count']))

    print(f"Report generated: {report_file}")

if __name__ == "__main__":
    # Set the working directory to the directory containing the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Specify the path to the DROID CSV file
    csv_file = "droid.csv"

    # Check if the file exists
    if os.path.exists(csv_file):
        # Analyze the DROID CSV file
        analyze_droid_csv(csv_file)
    else:
        print(f"File '{csv_file}' not found.")
