# ExtractZips

A robust utility for extracting ZIP archives, including nested ZIP files, with comprehensive error handling and progress feedback.

## Features

- 🚀 **Automatic Extraction**: Recursively extracts all ZIP files in the target directory
- 🔄 **Nested ZIP Support**: Handles archives within archives with ease
- 🛡️ **Error Resilience**: Gracefully handles permission issues and corrupted files
- 📝 **Detailed Logging**: Provides clear feedback about the extraction process
- 🖥️ **Flexible Execution**: Works as both a Python script and a standalone executable

## Installation

### Option 1: Run as Python Script
1. Ensure Python 3.6+ is installed
2. Install required dependencies (if any):
   ```bash
   pip install -r requirements.txt  # If you have a requirements file
   ```
3. Run the script:
   ```bash
   python main.py
   ```

### Option 2: Use Pre-built Executable
1. Download the latest release for your platform
2. Place the executable in your target directory
3. Run the executable

## Usage

### Basic Usage
```
Extract_All_Zips.exe
```
This will extract all ZIP files in the current directory.

### Features in Action
- Each ZIP file is extracted to its own subdirectory
- The script continues processing even if some files can't be extracted
- Detailed logs show the progress and any issues encountered

### Building from Source
To create a standalone executable:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name=Extract_All_Zips main.py
```
The executable will be created in the `dist` directory.
