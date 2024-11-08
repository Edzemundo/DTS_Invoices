# Document Scanner and Organizer

A Python-based utility for automatically scanning, renaming, and organizing document files (PDFs and images) based on their content using OCR. The system watches for new files, processes them to extract reference numbers and dates, and organizes them into appropriate folders.

## Features

- Automatic file watching and processing
- OCR-based document scanning for reference numbers and dates
- PDF and image file support
- Automatic file organization into dated folders
- PDF splitting capabilities
- Batch file processing
- File renaming utilities

## Prerequisites

Before running this project, you need to install the following dependencies:

```bash
pip install opencv-python
pip install pillow
pip install paddleocr
pip install pdf2image
pip install watchdog
pip install pypdf
```

You'll also need to install system dependencies for pdf2image:

For Ubuntu/Debian:

```bash
sudo apt-get install poppler-utils
```

For macOS:

```bash
brew install poppler
```

## Project Structure

- `file_handling.py`: Core utilities for file operations and organization
- `scan_number.py`: OCR processing and document scanning functionality
- `watch.py`: File system monitoring and automatic processing

## Usage

### Running the File Watcher

To start automatic file monitoring and processing:

```bash
python watch.py
```

This will:

1. Monitor the current directory for new files
2. Automatically process new documents
3. Organize files into dated folders

### Manual File Processing

You can also process files manually using the menu interface:

```bash
python file_handling.py
```

Menu options include:

1. Folderize - Organize files into dated folders
2. Move all PDFs in directory
3. Prepend PDFs with 'scan'
4. Split PDF into multiple PDFs

### Document Naming Convention

The system expects and processes files with the following patterns:

- Files starting with "scan" (for listing)
- Files starting with "OD" (for organization)
- Supported formats: .pdf, .jpeg, .png

### File Organization

Files are organized into folders based on their dates:

- Regular files go into MM-DD folders
- Files without reference numbers go to "Reference_not_found"
- Files without dates go to "Date_not_found"

## Functions

### File Handling (`file_handling.py`)

- `listscans()`: List all scan files in current directory
- `rename_scans()`: Rename scan files
- `folderize()`: Organize files into dated folders
- `split_pdf()`: Split PDFs into smaller files
- `move_pdfs_to_folder()`: Batch move/copy PDF files

### Document Scanning (`scan_number.py`)

- `scan_image()`: Process and extract info from images
- `scan_pdf()`: Process and extract info from PDFs
- `process()`: Image processing for better OCR results
- `ocr()`: Extract reference numbers and dates using OCR

### File Watching (`watch.py`)

- Continuous monitoring of directory for new files
- Automatic processing of new documents
- Multi-process handling of file watching and manual scanning

## Error Handling

- Files without reference numbers are moved to "Reference_not_found" directory
- Files without dates are moved to "Date_not_found" directory
- Invalid files and processing errors are logged to console

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Insert your chosen license here]
