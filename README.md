# CSV to PDF Time Report Generator - Desktop Application

A modern desktop application that converts CSV time tracking exports into professionally formatted PDF reports.

## Features

- **Modern Desktop Interface**: Clean, intuitive GUI built with tkinter
- **Drag-and-Drop Support**: Easy file selection with browse dialogs
- **Real-Time Progress**: Live progress tracking and status updates
- **Professional PDF Output**: Modern styling with summary statistics and detailed entries
- **Error Handling**: Robust error handling with user-friendly messages
- **Auto-Open PDF**: Option to automatically open generated PDF files

## Requirements

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python csv_to_pdf_converter.py
```

### Using the Desktop App

1. **Select CSV File**: Click "Browse CSV File" to select your time tracking CSV
2. **Choose Output Location**: Click "Choose Output Location" to specify where to save the PDF
3. **Convert**: Click "Convert to PDF" to generate your report
4. **View Results**: The app will show progress and ask if you want to open the PDF

## CSV Format

The application expects CSV files with the following columns:
- `Description` - Task description
- `Task` - Task name (optional)
- `Project` - Project name (optional)
- `Client` - Client name
- `User` - User name
- `Start` - Start time (format: YYYY-MM-DD HH:MM:SS)
- `End` - End time (format: YYYY-MM-DD HH:MM:SS)
- `Duration` - Duration in HH:MM:SS format
- `Duration (decimal)` - Duration in decimal hours
- `Billable` - Yes/No or True/False
- `Tags` - Tags (optional)

## PDF Output Features

The generated PDF includes:
- **Modern Design**: Professional styling with custom color scheme
- **Summary Section**: Total hours, billable vs non-billable breakdown, client statistics
- **Detailed Entries Table**: All time entries sorted by date with proper text wrapping
- **No Text Overflow**: Smart truncation prevents text from spilling between columns
- **Consistent Layout**: Professional margins and spacing throughout

## Application Interface

- **File Selection Section**: Easy-to-use file browsers for input and output
- **Status Window**: Real-time updates with timestamps and color-coded messages
- **Progress Bar**: Visual feedback during conversion process
- **Action Buttons**: Convert, Clear, and Exit controls

## Error Handling

The application includes comprehensive error handling for:
- Invalid or missing CSV files
- Malformed data in CSV rows
- File permission issues
- PDF generation errors
- Missing required columns

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **Memory**: Minimum 512MB RAM
- **Storage**: 50MB for application and dependencies

## Security

- All file processing is done locally
- No data is sent to external servers
- Temporary files are cleaned up automatically
- File validation prevents malicious uploads

## License

This project is open source and available under the MIT License.
