import os
import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime
import html # Added for escaping

def check_html_file(filepath):
    """
    Parses an HTML file and checks for:
    1. 'TBD' or '<%...%>' placeholders.
    2. Heading hierarchy (only one h1, sequential levels).
    3. Presence of 'description' and 'keywords' meta tags.
    """
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            
            # --- Check 1: Placeholders ---
            # Text node search for TBD
            text_nodes = soup.find_all(string=re.compile(r'TBD', re.IGNORECASE))
            for node in text_nodes:
                # Basic context extract
                context = node.strip()[:50]
                issues.append({
                    'type': 'Placeholder',
                    'message': f"Found 'TBD' text: \"{context}...\"",
                    'severity': 'Error'
                })
            
            # Regex for <% %> style placeholders in raw content
            # (BeautifulSoup might hide these if they look like tags, so check raw string)
            placeholders = re.findall(r'<%.*?%>', content)
            for p in placeholders:
                issues.append({
                    'type': 'Placeholder',
                    'message': f"Found placeholder pattern: {p}",
                    'severity': 'Error'
                })

            # --- Check 2: Heading Hierarchy ---
            headings = soup.find_all(re.compile(r'^h[1-6]$'))
            h1_count = 0
            last_level = 0
            
            for tag in headings:
                level = int(tag.name[1])
                text = tag.get_text(strip=True)
                
                if level == 1:
                    h1_count += 1
                
                # Check sequential order (e.g., can't jump h2 -> h4)
                if last_level > 0 and level > last_level + 1:
                    issues.append({
                        'type': 'Structure',
                        'message': f"Skipped heading level: <h{last_level}> followed by <h{level}> ('{text}')",
                        'severity': 'Warning'
                    })
                
                last_level = level

            if h1_count == 0:
                issues.append({'type': 'Structure', 'message': "Missing <h1> tag.", 'severity': 'Error'})
            elif h1_count > 1:
                issues.append({'type': 'Structure', 'message': f"Multiple <h1> tags found ({h1_count}).", 'severity': 'Error'})

            # --- Check 3: Post-publish Validation (Meta Tags) ---
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            meta_keys = soup.find('meta', attrs={'name': 'keywords'})
            
            # Verify description is present and has non-empty content
            if not meta_desc or not meta_desc.get('content') or not meta_desc.get('content').strip():
                issues.append({
                    'type': 'Post-publish Validation', 
                    'message': "Missing or empty 'description' meta tag.", 
                    'severity': 'Error'
                })

    except Exception as e:
        issues.append({'type': 'Fatal', 'message': f"Could not parse file: {str(e)}", 'severity': 'Critical'})

    return issues

def generate_report(results):
    """
    Generates an HTML report from the results dictionary.
    """
    report_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Doc Quality Report</title>
        <style>
            body {{ font-family: sans-serif; margin: 2rem; background: #f8fafc; color: #334155; }}
            h1 {{ color: #0f172a; }}
            .file-block {{ background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 2rem; }}
            .file-name {{ font-size: 1.2rem; font-weight: bold; margin-bottom: 1rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }}
            .issue {{ padding: 0.75rem; border-left: 4px solid #ccc; background: #f1f5f9; margin-bottom: 0.5rem; }}
            .issue.Error {{ border-left-color: #ef4444; background: #fee2e2; }}
            .issue.Warning {{ border-left-color: #f59e0b; background: #fef3c7; }}
            .timestamp {{ color: #64748b; font-size: 0.9rem; }}
            .no-issues {{ color: #22c55e; font-weight: bold; }}
            .summary {{ margin-bottom: 2rem; }}
        </style>
    </head>
    <body>
        <h1>Documentation Quality Report</h1>
        <div class="summary">
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    """
    
    for filepath, issues in results.items():
        report_html += f'<div class="file-block"><div class="file-name">{filepath}</div>'
        
        if not issues:
            report_html += '<div class="no-issues">✓ No issues found.</div>'
        else:
            for issue in issues:
                # Debug print
                # print(f"DEBUG: Processing issue: {issue}")
                safe_message = html.escape(str(issue["message"]))
                report_html += f'<div class="issue {issue["severity"]}"><strong>[{issue["severity"]}] {issue["type"]}:</strong> {safe_message}</div>'
        
        report_html += '</div>'

    report_html += "</body></html>"
    return report_html

def main():
    if len(sys.argv) < 2:
        print("Usage: python doc_checker.py <file1.html> <file2.html> ...")
        sys.exit(1)

    files = sys.argv[1:]
    results = {}

    print(f"Checking {len(files)} files...")
    for fpath in files:
        if os.path.exists(fpath):
            results[fpath] = check_html_file(fpath)
        else:
            print(f"File not found: {fpath}")

    report_content = generate_report(results)
    
    with open('report.html', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"Report generated: {os.path.abspath('report.html')}")

if __name__ == '__main__':
    main()
