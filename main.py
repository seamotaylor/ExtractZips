"""
Zip File Extractor Utility

A robust command-line tool for extracting ZIP archives, including nested ZIP files.
Handles various edge cases like permission errors, corrupted files, and system compatibility.

Features:
- Recursive extraction of nested ZIP files
- Graceful error handling for permissions and corrupt files
- Detailed progress and error reporting
- Works as both a Python script and standalone executable

Usage:
    python main.py  # Extracts ZIP files in the current directory
    
For building a standalone executable:
    pyinstaller --onefile --noconsole --name=Extract_All_Zips main.py
"""

import os
import zipfile
import sys
import stat
from typing import Callable, Any, Optional

def remove_readonly(func: Callable[[str], Any], path: str, exc_info: Any) -> bool:
    """
    Remove read-only attribute from a file and retry the operation.
    
    This function is designed to be used as an error handler for shutil.rmtree()
    when dealing with read-only files on Windows.
    
    Args:
        func: The function that caused the error (e.g., os.unlink, os.rmdir)
        path: The path to the file or directory that couldn't be accessed
        exc_info: Exception information returned by sys.exc_info()
        
    Returns:
        bool: True if the operation succeeded after removing read-only attribute,
              False otherwise
    """
    # Check if the error is due to a read-only file
    if not os.access(path, os.W_OK):
        try:
            # Remove read-only attribute and try the operation again
            os.chmod(path, stat.S_IWRITE)
            func(path)
            return True
        except Exception as e:
            print(f"  Could not remove read-only attribute from {path}: {e}")
            return False
    return False

def extract_zip_files(directory: str) -> None:
    """
    Recursively extract all ZIP files in the specified directory.
    
    This function will:
    1. Scan the specified directory for ZIP files
    2. Extract each ZIP to a subdirectory with the same name
    3. Recursively process any ZIP files found in the extracted contents
    4. Handle various error conditions gracefully
    
    Args:
        directory: Path to the directory containing ZIP files to extract
    """
    
    try:
        files = os.listdir(directory)
    except PermissionError:
        print(f"  Warning: No permission to access directory: {directory}")
        return
        
    for filename in files:
        if not filename.lower().endswith('.zip'):
            continue
            
        zip_path = os.path.join(directory, filename)
        extract_path = os.path.join(directory, os.path.splitext(filename)[0])
        
        try:
            if not os.path.isfile(zip_path):
                print(f"  Skipping {filename} - not a file")
                continue
                
            print(f"Processing: {filename}")
            os.makedirs(extract_path, exist_ok=True)
            
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # Try normal extraction first
                    try:
                        zip_ref.extractall(extract_path)
                        print(f"  Successfully extracted: {filename}")
                    except PermissionError:
                        print(f"  Warning: Permission error during extraction. Trying individual files...")
                        # If that fails, try extracting files one by one
                        for member in zip_ref.infolist():
                            try:
                                zip_ref.extract(member, extract_path)
                            except PermissionError as pe:
                                member_path = os.path.join(extract_path, member.filename)
                                print(f"  Could not extract {member.filename}: {pe}")
                                continue
                                
                # Process nested zip files if any
                extract_zip_files(extract_path)
                
            except zipfile.BadZipFile:
                print(f"  Error: {filename} is not a valid zip file")
            except Exception as e:
                print(f"  Error processing {filename}: {e}")
                
        except Exception as e:
            print(f"  Error with {filename}: {e}")
            continue


def main() -> None:
    """
    Main entry point for the ZIP extraction utility.
    
    This function:
    1. Determines the working directory (either where the script is located or where the executable is run from)
    2. Initiates the ZIP extraction process
    3. Handles user interruptions and unexpected errors
    4. Provides appropriate console feedback
    
    The function is designed to work both as a script and as a frozen executable.
    """
    try:
        # Determine the directory containing the zip files
        if getattr(sys, 'frozen', False):  # Check if running as a bundled executable
            directory = os.path.dirname(sys.executable)
        else:
            directory = os.path.dirname(os.path.abspath(__file__))

        print(f"Starting extraction in: {directory}")
        print("-" * 50)
        
        # Call the function to extract zip files
        extract_zip_files(directory)
        
        print("\nExtraction completed!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    
    # Keep the window open if running as an executable with console
    if getattr(sys, 'frozen', False) and sys.stdin and sys.stdin.isatty():
        try:
            input("\nPress Enter to exit...")
        except (EOFError, RuntimeError):
            # If input is not available (non-interactive terminal), just exit
            pass

if __name__ == "__main__":
    main()

#executable generator, run in terminal
#pyinstaller --onefile --noconsole --name=Extract_All_Zips main.py

