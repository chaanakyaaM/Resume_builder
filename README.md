# 🚀 Resume Builder

A simple, interactive web application that generates professional resumes in DOCX format with clickable hyperlinks using static resume template.

## ✨ Features

- **Interactive Web Interface**: User-friendly Streamlit interface for easy data entry
- **Professional DOCX Output**: Generates formatted Word documents with proper styling
- **Clickable Hyperlinks**: LinkedIn and GitHub profiles rendered as blue, underlined hyperlinks
- **Real-time Preview**: Preview your resume data before downloading using HTML conversion
- **Sample Data**: Pre-filled example data to get started quickly
- **Form Validation**: Ensures all required fields are completed before generation
- **Multiple Sections**: Support for personal info, summary, education, experience, projects, and skills
- **Flexible Experience**: Optional work experience section for students and career changers
- **Local File Save**: Automatically saves resume as `generated_output.docx` in your directory

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Template Engine**: python-docx-template (docxtpl)
- **Document Processing**: python-docx, mammoth
- **Preview**: HTML conversion with custom styling
- **File Handling**: BytesIO for download functionality

## 📋 Prerequisites

- Python 3.8 or higher
- Microsoft Word (for creating/editing templates)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/resume-builder.git
   cd resume-builder
   ```

2. **Install required packages:**
   ```bash
   pip install streamlit docxtpl mammoth python-docx
   ```

3. **Create your Word template:**
   - Create a new Word document named `temp.docx`
   - Add the template variables (see Template Structure below)
   - Save in the same directory as the Python script

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 🎯 Usage

### Basic Workflow:

1. **Launch the app**: Run `streamlit run app.py`
2. **Fill in your information**:
   - Personal details (name, email, phone, LinkedIn, GitHub)
   - Professional summary
   - Education background
   - Work experience (optional)
   - Projects with tech stack
   - Technical skills
3. **Generate resume**: Click "Generate DOCX Resume"
4. **Preview and download**: Review the preview and download your resume

### Quick Start with Sample Data:

1. Click "Fill with Sample Data" button
2. Review the populated fields
3. Customize as needed
4. Generate and download

## 📁 File Structure

```
resume-builder/
│
├── main.py                 # Main Streamlit application
├── temp.docx             # Your Word template file
├── generated_output.docx # Generated resume (auto-created)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Configuration

### Template Customization:
- Edit `temp.docx` to change layout, fonts, and styling
- Maintain Jinja2 variable names for compatibility
- Use Word's formatting tools for professional appearance

> 💡 **NOTE**: For best results, open the generated DOCX file in Microsoft Word or Google Docs to fine-tune formatting before converting to PDF.

**Credits**
- Built with ❤️ by using streamlit