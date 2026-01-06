#!/usr/bin/env python3
"""
Desktop GUI Application for CSV to PDF Time Report Generator
A modern desktop application using tkinter for converting CSV time tracking exports to professional PDF reports.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass
import csv
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


@dataclass
class TimeEntry:
    """Data class for time entry records"""
    description: str
    task: str
    project: str
    client: str
    user: str
    start: datetime
    end: datetime
    duration: timedelta
    duration_decimal: float
    billable: bool
    tags: str


class CSVToPDFConverter:
    """Core converter class for CSV to PDF transformation"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for modern professional formatting"""
        # Modern color scheme
        self.primary_color = colors.HexColor('#2C3E50')  # Dark blue-gray
        self.accent_color = colors.HexColor('#3498DB')   # Bright blue
        self.light_bg = colors.HexColor('#ECF0F1')        # Light gray
        self.alt_bg = colors.HexColor('#BDC3C7')         # Medium gray
        self.text_color = colors.HexColor('#2C3E50')      # Dark text
        
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=self.primary_color,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=15,
            spaceBefore=25,
            textColor=self.primary_color,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=self.accent_color,
            borderPadding=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomSubheading',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=self.accent_color,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            textColor=self.text_color,
            fontName='Helvetica'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomSmall',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=6,
            textColor=self.text_color,
            fontName='Helvetica'
        ))

    def parse_csv(self, csv_file_path: str) -> List[TimeEntry]:
        """Parse CSV file and return list of TimeEntry objects"""
        entries = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Parse datetime fields
                        start_time = datetime.strptime(row['Start'], '%Y-%m-%d %H:%M:%S')
                        end_time = datetime.strptime(row['End'], '%Y-%m-%d %H:%M:%S')
                        
                        # Parse duration
                        duration_parts = row['Duration'].split(':')
                        duration = timedelta(
                            hours=int(duration_parts[0]),
                            minutes=int(duration_parts[1]),
                            seconds=int(duration_parts[2]) if len(duration_parts) > 2 else 0
                        )
                        
                        # Parse billable status
                        billable = row['Billable'].lower() in ['yes', 'true', '1']
                        
                        entry = TimeEntry(
                            description=row['Description'] or '',
                            task=row['Task'] or '',
                            project=row['Project'] or '',
                            client=row['Client'] or '',
                            user=row['User'] or '',
                            start=start_time,
                            end=end_time,
                            duration=duration,
                            duration_decimal=float(row['Duration (decimal)']),
                            billable=billable,
                            tags=row['Tags'] or ''
                        )
                        
                        entries.append(entry)
                        
                    except (ValueError, KeyError) as e:
                        print(f"Warning: Skipping row {row_num} due to error: {e}")
                        continue
                        
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {e}")
            
        return entries

    def _create_summary_table(self, entries: List[TimeEntry]) -> Table:
        """Create modern summary statistics table"""
        total_hours = sum(entry.duration_decimal for entry in entries)
        billable_hours = sum(entry.duration_decimal for entry in entries if entry.billable)
        non_billable_hours = total_hours - billable_hours
        
        # Group by client
        client_hours = {}
        for entry in entries:
            client = entry.client or 'Unassigned'
            if client not in client_hours:
                client_hours[client] = 0
            client_hours[client] += entry.duration_decimal
        
        # Create summary data
        summary_data = [
            ['Metric', 'Hours'],
            ['Total Hours', f"{total_hours:.2f}"],
            ['Billable Hours', f"{billable_hours:.2f}"],
            ['Non-Billable Hours', f"{non_billable_hours:.2f}"],
            ['', ''],
            ['Breakdown by Client:', ''],
        ]
        
        for client, hours in sorted(client_hours.items()):
            summary_data.append([client, f"{hours:.2f}"])
        
        summary_table = Table(summary_data, colWidths=[3*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
            ('BACKGROUND', (0, 1), (-1, -1), self.light_bg),
            ('GRID', (0, 0), (-1, -1), 1, self.primary_color),
            ('LINEBELOW', (0, 0), (-1, 0), 2, self.accent_color),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        # Style the client breakdown section header
        client_breakdown_row = 5  # Row index of 'Breakdown by Client:'
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, client_breakdown_row), (-1, client_breakdown_row), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, client_breakdown_row), (-1, client_breakdown_row), self.accent_color),
            ('BACKGROUND', (0, client_breakdown_row), (-1, client_breakdown_row), self.light_bg),
        ]))
        
        return summary_table

    def _create_entries_table(self, entries: List[TimeEntry]) -> Table:
        """Create modern detailed time entries table with proper text wrapping"""
        # Sort entries by start date (most recent first)
        sorted_entries = sorted(entries, key=lambda x: x.start, reverse=True)
        
        # Table headers (removed 'Billable' column)
        headers = [
            'Date', 'Client', 'Project', 'Description', 
            'Start', 'End', 'Duration'
        ]
        
        # Build table data with proper text handling
        table_data = [headers]
        
        for entry in sorted_entries:
            # Smart text truncation to prevent overflow
            description = entry.description
            max_length = 45  # Reduced from 60 for better fitting
            if len(description) > max_length:
                # Find a good breaking point near the max length
                break_point = max_length
                for i in range(max_length - 5, max_length + 1):
                    if i < len(description) and description[i] in [' ', '-', ',']:
                        break_point = i + 1
                        break
                description = description[:break_point] + '...'
            
            row = [
                entry.start.strftime('%Y-%m-%d'),
                entry.client or 'N/A',
                entry.project or 'N/A',
                description,
                entry.start.strftime('%H:%M'),
                entry.end.strftime('%H:%M'),
                f"{entry.duration_decimal:.2f}h"
            ]
            table_data.append(row)
        
        # Optimized column widths to prevent overflow
        # Give more space to Description, less to others
        table = Table(table_data, 
                     colWidths=[0.8*inch, 1.1*inch, 1.3*inch, 2.8*inch, 0.6*inch, 0.6*inch, 0.8*inch],
                     repeatRows=1)  # Repeat header on new pages
        
        # Modern table styling with better text handling
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),  # Slightly smaller header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('LINEBELOW', (0, 0), (-1, 0), 2, self.accent_color),
            
            # Data row styling
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),  # Smaller font for better fitting
            ('BACKGROUND', (0, 1), (-1, -1), self.light_bg),
            ('GRID', (0, 0), (-1, -1), 1, self.primary_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center align vertically
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            
            # Ensure text doesn't overflow
            ('WORDWRAP', (3, 1), (3, -1), 'CJK'),  # Word wrap for description column
            ('MAXWIDTH', (3, 1), (3, -1), 2.8*inch),  # Max width for description
        ]))
        
        # Add alternating row colors for better readability
        for i in range(1, len(table_data)):
            if i % 2 == 0:
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8F9FA'))
                ]))
        
        return table

    def generate_pdf(self, entries: List[TimeEntry], output_path: str, title: str = "Time Report"):
        """Generate modern PDF report from time entries"""
        if not entries:
            raise ValueError("No time entries to generate report")
        
        # Create PDF document with modern margins
        doc = SimpleDocTemplate(
            output_path, 
            pagesize=A4,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=1*inch
        )
        story = []
        
        # Add a subtle header line
        story.append(Spacer(1, 30))
        
        # Title with modern styling
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 25))
        
        # Summary section with modern heading
        story.append(Paragraph("Summary", self.styles['CustomHeading']))
        story.append(self._create_summary_table(entries))
        story.append(Spacer(1, 35))
        
        # Detailed entries section
        story.append(Paragraph("Detailed Time Entries", self.styles['CustomHeading']))
        story.append(self._create_entries_table(entries))
        
        # Build PDF
        doc.build(story)
        
        print(f"Modern PDF report generated successfully: {output_path}")


class DesktopApp:
    """Main desktop application GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("CSV to PDF Time Report Generator")
        self.root.geometry("650x600")
        self.root.configure(bg='#f0f0f0')
        
        # Modern color scheme
        self.primary_color = '#2C3E50'
        self.accent_color = '#3498DB'
        self.success_color = '#27AE60'
        self.error_color = '#E74C3C'
        
        # Initialize converter
        self.converter = CSVToPDFConverter()
        
        # Variables
        self.csv_file_path = None
        self.pdf_file_path = None
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="CSV to PDF Time Report Generator",
            font=('Helvetica', 20, 'bold'),
            fg=self.primary_color,
            bg='#f0f0f0'
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky=tk.W)
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Transform your time tracking CSV exports into professional PDF reports",
            font=('Helvetica', 11),
            fg='#666666',
            bg='#f0f0f0'
        )
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 30), sticky=tk.W)
        
        # File Selection Section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="15")
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(1, weight=1)
        
        # CSV File Selection
        tk.Label(file_frame, text="CSV File:", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.csv_path_var = tk.StringVar()
        csv_entry = ttk.Entry(file_frame, textvariable=self.csv_path_var, state='readonly')
        csv_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        browse_csv_btn = ttk.Button(
            file_frame, 
            text="Browse CSV File",
            command=self.browse_csv_file
        )
        browse_csv_btn.grid(row=1, column=2, padx=(10, 0), sticky=tk.E)
        
        # Output File Selection
        tk.Label(file_frame, text="Output PDF:", font=('Helvetica', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.pdf_path_var = tk.StringVar()
        pdf_entry = ttk.Entry(file_frame, textvariable=self.pdf_path_var, state='readonly')
        pdf_entry.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        browse_pdf_btn = ttk.Button(
            file_frame,
            text="Choose Output Location",
            command=self.browse_output_location
        )
        browse_pdf_btn.grid(row=3, column=2, padx=(10, 0), sticky=tk.E)
        
        # Status Section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="15")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_text = tk.Text(
            status_frame,
            height=8,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#ffffff',
            fg='#333333'
        )
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for status text
        status_scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        status_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        
        self.convert_btn = ttk.Button(
            button_frame,
            text="Convert to PDF",
            command=self.convert_to_pdf,
            style='Accent.TButton'
        )
        self.convert_btn.grid(row=0, column=0, padx=(0, 10))
        
        clear_btn = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_form
        )
        clear_btn.grid(row=0, column=1, padx=(0, 10))
        
        exit_btn = ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit
        )
        exit_btn.grid(row=0, column=2)
        
        # Configure button styles
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'))
        
        # Initial status message
        self.update_status("Welcome to CSV to PDF Time Report Generator!\n\nPlease select a CSV file to begin.", "info")
        
    def browse_csv_file(self):
        """Open file dialog to select CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            self.csv_file_path = file_path
            self.csv_path_var.set(file_path)
            self.update_status(f"CSV file selected: {os.path.basename(file_path)}", "success")
            
            # Auto-generate PDF path if not already set
            if not self.pdf_file_path:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                pdf_path = os.path.join(os.path.dirname(file_path), f"{base_name}_report.pdf")
                self.pdf_file_path = pdf_path
                self.pdf_path_var.set(pdf_path)
    
    def browse_output_location(self):
        """Open file dialog to select output PDF location"""
        if self.csv_file_path:
            default_name = f"{os.path.splitext(os.path.basename(self.csv_file_path))[0]}_report.pdf"
        else:
            default_name = "time_report.pdf"
            
        file_path = filedialog.asksaveasfilename(
            title="Save PDF Report",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=default_name
        )
        
        if file_path:
            self.pdf_file_path = file_path
            self.pdf_path_var.set(file_path)
            self.update_status(f"Output location set: {os.path.basename(file_path)}", "success")
    
    def update_status(self, message, message_type="info"):
        """Update status text with color coding"""
        self.status_text.delete(1.0, tk.END)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        
        self.status_text.insert(tk.END, full_message)
        
        # Color coding (simplified for tkinter)
        if message_type == "error":
            self.status_text.tag_add("error", "1.0", "1.end")
            self.status_text.tag_config("error", foreground=self.error_color)
        elif message_type == "success":
            self.status_text.tag_add("success", "1.0", "1.end")
            self.status_text.tag_config("success", foreground=self.success_color)
        
        self.status_text.see(tk.END)
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_var.set(value)
        self.root.update_idletasks()
    
    def convert_to_pdf(self):
        """Convert CSV to PDF in a separate thread"""
        if not self.csv_file_path:
            messagebox.showerror("Error", "Please select a CSV file first.")
            return
        
        if not self.pdf_file_path:
            messagebox.showerror("Error", "Please select an output location for the PDF.")
            return
        
        # Disable convert button during processing
        self.convert_btn.configure(state='disabled')
        self.update_progress(0)
        self.update_status("Starting conversion process...", "info")
        
        # Start conversion in separate thread
        thread = threading.Thread(target=self._convert_worker)
        thread.daemon = True
        thread.start()
    
    def _convert_worker(self):
        """Worker thread for CSV to PDF conversion"""
        try:
            # Step 1: Parse CSV
            self.root.after(0, lambda: self.update_status("Parsing CSV file...", "info"))
            self.root.after(0, lambda: self.update_progress(20))
            
            entries = self.converter.parse_csv(self.csv_file_path)
            
            if not entries:
                self.root.after(0, lambda: self.update_status("No valid time entries found in CSV file.", "error"))
                self.root.after(0, lambda: self.convert_btn.configure(state='normal'))
                return
            
            self.root.after(0, lambda: self.update_status(f"Found {len(entries)} time entries", "success"))
            
            # Step 2: Generate PDF
            self.root.after(0, lambda: self.update_status("Generating PDF report...", "info"))
            self.root.after(0, lambda: self.update_progress(60))
            
            self.converter.generate_pdf(entries, self.pdf_file_path)
            
            # Step 3: Complete
            self.root.after(0, lambda: self.update_progress(100))
            self.root.after(0, lambda: self.update_status(f"PDF report generated successfully!\nSaved to: {self.pdf_file_path}", "success"))
            
            # Ask if user wants to open the PDF
            self.root.after(0, lambda: self._ask_open_pdf())
            
        except Exception as e:
            error_msg = f"Error during conversion: {str(e)}"
            self.root.after(0, lambda: self.update_status(error_msg, "error"))
        
        finally:
            # Re-enable convert button
            self.root.after(0, lambda: self.convert_btn.configure(state='normal'))
    
    def _ask_open_pdf(self):
        """Ask user if they want to open the generated PDF"""
        result = messagebox.askyesno(
            "Conversion Complete",
            "PDF report generated successfully!\n\nWould you like to open the PDF file?"
        )
        
        if result:
            try:
                os.startfile(self.pdf_file_path)
            except:
                messagebox.showinfo("Info", "Could not open the PDF file automatically. Please open it manually.")
    
    def clear_form(self):
        """Clear all form fields"""
        self.csv_file_path = None
        self.pdf_file_path = None
        self.csv_path_var.set("")
        self.pdf_path_var.set("")
        self.progress_var.set(0)
        self.status_text.delete(1.0, tk.END)
        self.update_status("Form cleared. Ready for new conversion.", "info")


def main():
    """Main function to run the desktop application"""
    root = tk.Tk()
    app = DesktopApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
