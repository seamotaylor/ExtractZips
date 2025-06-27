import os
import zipfile
import sys


def extract_zip_files(directory):
    """Extract all zip files in the given directory, including nested zip files."""

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.lower().endswith('.zip'):  # Case-insensitive check for .zip

            zip_path = os.path.join(directory, filename)
            extract_path = os.path.join(directory, os.path.splitext(filename)[0])

            # Create directory for extraction if it doesn't exist
            os.makedirs(extract_path, exist_ok=True)

            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            print(f"Extracted: {filename} to {extract_path}")

            # Check for nested zip files in the extracted directory
            extract_zip_files(extract_path)


if __name__ == "__main__":
    # Determine the directory containing the zip files
    if getattr(sys, 'frozen', False):  # Check if running as a bundled executable
        directory = os.path.dirname(sys.executable)
    else:
        directory = os.path.dirname(os.path.abspath(__file__))

    # Call the function to extract zip files
    extract_zip_files(directory)

#executable generator
#pyinstaller --onefile --noconsole --name=Extract_All_Zips main.py

