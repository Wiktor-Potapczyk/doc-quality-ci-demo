# Documentation Quality Checker - User Guide

## 1. Introduction
The **Doc Quality Checker** is a command-line utility designed for DevSecOps and Technical Writing teams. It automates the validation of HTML documentation files to ensure they meet Veeam's strict quality and structural standards.

## 2. Installation

1.  **Clone the Repository** (or download source files):
    ```bash
    git clone https://github.com/Wiktor-Potapczyk/doc-quality-checker.git
    cd doc-quality-checker
    ```

2.  **Install Required Libraries**:
    Run the following command in your terminal/command prompt:
    ```bash
    pip install beautifulsoup4
    ```

## 3. Prerequisites
Before running the tool, ensure your environment meets these requirements:
*   **Operating System**: Windows, macOS, or Linux.
*   **Python**: Version 3.8 or higher.
*   **Dependencies**: `beautifulsoup4` (Python library for parsing HTML).

## 4. Procedure

### Basic Usage
To check a single HTML file, run the script and provide the file path as an argument:
```bash
python doc_checker.py path/to/your/document.html
```

### Checking Multiple Files
You can check multiple files in one run. All results will be aggregated into a single report.
```bash
python doc_checker.py file1.html file2.html file3.html
```

### Running the Included Test Case
The repository comes with a "modified" copy of a real Veeam user guide that contains intentional errors for demonstration purposes. To see the tool catch errors:
```bash
python doc_checker.py test_files/modified_veeam_test.html
```

## 5. Analysis & Validation

The tool generates a file named **`report.html`** in the directory where you ran the script. Open this file in any web browser to view the results.

### Types of Issues
The tool checks for three specific categories of issues:

| Category | Severity | Description |
| :--- | :--- | :--- |
| **Structure** | **Error** | Checks if the document has exactly one `<h1>` tag and if heading levels are sequential (e.g., `<h3>` must follow `<h2>`). |
| **Placeholder** | **Error** | Detects leftover "TBD" text or template variables like `<% VERSION %>`. |
| **Post-publish** | **Error/Warn** | Verifies that the `description` meta tag is valid. |

### Status Colors
*   <span style="color:green">**Green (No issues found)**</span>: The file passed all checks.
*   <span style="color:orange">**Yellow (Warning)**</span>: Minor issues found (e.g., non-critical tagging).
*   <span style="color:red">**Red (Error)**</span>: Critical issues found. The report includes line numbers for location tracking (e.g., `[Line 45]`).

## 6. Troubleshooting

**Error: `ModuleNotFoundError: No module named 'bs4'`**
*   **Cause**: The required library is not installed.
*   **Fix**: Run `pip install beautifulsoup4`.

**Error: `File not found`**
*   **Cause**: The path provided to the script is incorrect.
*   **Fix**: Use strict absolute paths (e.g., `C:\Work\docs\file.html`) if relative paths fail.

**Report shows no output**
*   **Cause**: Browser caching or permission issues.
*   **Fix**: Refresh the browser page or check file write permissions in the directory.
