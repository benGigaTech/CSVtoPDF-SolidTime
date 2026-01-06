# CSV to PDF Time Report Generator

A modern desktop application that converts CSV time tracking exports into professionally formatted PDF reports.

![Application Preview](https://img.shields.io/badge/Python-3.7%2B-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **🖥️ Modern Desktop Interface**: Clean, intuitive GUI built with tkinter
- **📁 Easy File Selection**: Browse dialogs for CSV input and PDF output
- **📊 Real-Time Progress**: Live progress tracking with detailed status updates
- **🎨 Professional PDF Output**: Modern styling with summary statistics and detailed entries
- **🛡️ Robust Error Handling**: User-friendly error messages and validation
- **🚀 Auto-Open PDF**: Option to automatically open generated PDF files
- **📱 Responsive Design**: Optimized window sizing for different screen resolutions

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/csv-to-pdf.git
   cd csv-to-pdf
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python csv_to_pdf_converter.py
   ```

### Using the Desktop App

1. **Select CSV File**: Click "Browse CSV File" to select your time tracking CSV
2. **Choose Output Location**: Click "Choose Output Location" to specify where to save the PDF
3. **Convert**: Click "Convert to PDF" to generate your report
4. **View Results**: The app will show progress and ask if you want to open the PDF

## 📋 CSV Format Requirements

The application expects CSV files with the following columns:

| Column | Required | Format | Description |
|--------|----------|--------|-------------|
| `Description` | ✅ | Text | Task description |
| `Task` | ❌ | Text | Task name (optional) |
| `Project` | ❌ | Text | Project name (optional) |
| `Client` | ✅ | Text | Client name |
| `User` | ✅ | Text | User name |
| `Start` | ✅ | YYYY-MM-DD HH:MM:SS | Start time |
| `End` | ✅ | YYYY-MM-DD HH:MM:SS | End time |
| `Duration` | ✅ | HH:MM:SS | Duration in time format |
| `Duration (decimal)` | ✅ | Decimal | Duration in decimal hours |
| `Billable` | ✅ | Yes/No or True/False | Billable status |
| `Tags` | ❌ | Text | Tags (optional) |

### Example CSV Row
```csv
Description,Task,Project,Client,User,Start,End,Duration,"Duration (decimal)",Billable,Tags
"Ticket Response",,"CRG IT Support","CRG Homes",Benjamin,"2025-12-30 15:15:00","2025-12-30 15:30:00",0:15:00,0.25,Yes,CRG
```

## 📄 PDF Output Features

The generated PDF includes:

### Summary Section
- **Total Hours**: Overall time worked
- **Billable vs Non-Billable**: Breakdown of billable hours
- **Client Statistics**: Hours breakdown by client

### Detailed Entries Table
- **Chronological Order**: Entries sorted by date (most recent first)
- **Smart Text Wrapping**: Prevents text overflow between columns
- **Professional Styling**: Modern color scheme and typography
- **Optimized Layout**: Consistent margins and spacing

### Design Features
- **Modern Color Scheme**: Professional blue-gray palette
- **Clean Typography**: Helvetica fonts with proper hierarchy
- **No Text Overflow**: Smart truncation with ellipsis
- **Consistent Formatting**: Professional appearance throughout

## 🖥️ Application Interface

### Main Components

- **File Selection Section**: 
  - CSV file browser with validation
  - Output location selector with auto-naming
  
- **Status Window**: 
  - Real-time updates with timestamps
  - Color-coded messages (success/error/info)
  - Scrollable text area
  
- **Progress Bar**: 
  - Visual feedback during conversion
  - Percentage completion indicator
  
- **Action Buttons**: 
  - Convert to PDF
  - Clear form
  - Exit application

### Window Specifications
- **Dimensions**: 650x600 pixels (optimized for desktop)
- **Resizable**: User can adjust window size
- **Centered**: Automatically centers on screen launch

## 🛠️ Technical Details

### Architecture
- **Language**: Python 3.7+
- **GUI Framework**: tkinter
- **PDF Generation**: ReportLab
- **CSV Parsing**: Python csv module
- **Threading**: Multi-threaded for responsive UI

### Dependencies
```
reportlab>=4.0.0      # PDF generation
python-dateutil>=2.8.0 # Date/time utilities
```

### File Structure
```
csv-to-pdf/
├── csv_to_pdf_converter.py  # Main desktop application
├── requirements.txt         # Python dependencies
├── README.md               # This documentation
├── .gitignore              # Git ignore patterns
└── examples/               # Sample CSV files (optional)
```

## 🔧 Error Handling

The application includes comprehensive error handling for:

### File Errors
- Invalid or missing CSV files
- File permission issues
- Corrupted file formats
- Insufficient disk space

### Data Errors
- Malformed CSV structure
- Missing required columns
- Invalid date/time formats
- Incorrect data types

### Processing Errors
- PDF generation failures
- Memory allocation issues
- Thread synchronization problems

### User Feedback
- Clear error messages with suggested solutions
- Status updates with timestamps
- Progress indicators for long operations
- Confirmation dialogs for critical actions

## 💻 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Python**: 3.7 or higher
- **Memory**: 512MB RAM
- **Storage**: 50MB free space
- **Display**: 1024x768 resolution

### Recommended Requirements
- **Operating System**: Windows 11, macOS 12+, or Ubuntu 20.04+
- **Python**: 3.9 or higher
- **Memory**: 1GB RAM
- **Storage**: 100MB free space
- **Display**: 1280x720 resolution

## 🔒 Security & Privacy

- **Local Processing**: All file processing done locally, no data sent to external servers
- **No Data Collection**: Application does not collect or transmit any user data
- **Temporary Files**: Automatic cleanup of temporary files
- **File Validation**: Prevents malicious file uploads
- **Sandboxed**: Runs in user space with limited permissions

## 🐛 Troubleshooting

### Common Issues

**Application won't start**
- Ensure Python 3.7+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check file permissions on the application directory

**CSV file not recognized**
- Verify CSV file has required columns
- Check file encoding (should be UTF-8)
- Ensure file extension is `.csv`

**PDF generation fails**
- Check available disk space
- Verify output directory permissions
- Ensure CSV data is properly formatted

**Window sizing issues**
- Restart the application
- Check display resolution settings
- Try maximizing the window

### Getting Help

1. **Check the logs**: Status window shows detailed error messages
2. **Verify CSV format**: Ensure all required columns are present
3. **Test with sample data**: Use a known-good CSV file for testing
4. **Report issues**: Include error messages and system details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a Pull Request

### Code Style
- Follow PEP 8 Python style guidelines
- Add docstrings to functions and classes
- Include type hints where appropriate
- Write clear, descriptive variable names

## 📝 Changelog

### v1.0.0 (2025-01-06)
- ✨ Initial release
- 🖥️ Desktop GUI application
- 📊 CSV to PDF conversion
- 🎨 Modern PDF styling
- 📈 Summary statistics
- 🛡️ Error handling
- 📱 Responsive interface

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ReportLab** - PDF generation library
- **tkinter** - Python GUI framework
- **Python csv module** - CSV parsing utilities

## 📞 Support

For support, please:
1. Check the troubleshooting section above
2. Search existing [Issues](https://github.com/your-username/csv-to-pdf/issues)
3. Create a new issue with detailed information
4. Include error messages and system specifications

---

**Made with ❤️ for time tracking professionals**
