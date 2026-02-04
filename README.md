# Documentation Quality Checker

A Python-based CLI tool designed to audit HTML documentation files for structural integrity, content verification, and metadata quality.

## Documentation
See [User Guide](doc_checker_user_guide.md) for detailed usage instructions.

## Features

This tool implements **3 specific quality checks** found in common technical writing standards:

1.  **HTML Structure**:
    *   Verifies that exactly one `<h1>` tag exists.
    *   Ensures heading levels are sequential (e.g., `<h2>` must follow `<h1>`, not jump to `<h4>`).
2.  **Build Leftovers**:
    *   Detects "TBD" (To Be Determined) text.
    *   Detects raw template placeholders like `<% variable %>`.
3.  **Post-publish Validation (Meta Tags)**:
    *   Verifies that the `description` meta tag is present and contains non-empty text.

## Prerequisites

- Python 3.x installed.
- **Dependencies**: Install the required library using pip:
  ```bash
  pip install beautifulsoup4
  ```

## Usage

Run the script from the command line, providing the path(s) to the HTML file(s) you want to check.

### Basic Command
```bash
python doc_checker.py "path/to/your/file.html"
```

### Checking Multiple Files
```bash
python doc_checker.py file1.html file2.html file3.html
```

## Output

The tool generates a single **HTML Report** in the current directory:
- **File**: `report.html`
- **Content**: A color-coded summary of passes (Green) and failures (Red/Yellow) for each checked file.

## Troubleshooting

- **"File not found"**: Ensure you provide the correct absolute or relative path to the HTML file.
- **"ModuleNotFoundError"**: Run `pip install beautifulsoup4`.
