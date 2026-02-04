import os
from bs4 import BeautifulSoup

source_path = r"C:\Users\48603\Desktop\prg\veeam\synonyms\workspace\Replication for VMware vSphere - Veeam Backup & Replication User Guide.html"
dest_path = r"C:\Users\48603\Desktop\prg\veeam\synonyms\doc_checker\test_files\modified_veeam_test.html"

# Read original
with open(source_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# 1. INTRODUCE META ERROR: Remove description
meta_desc = soup.find('meta', attrs={'name': 'description'})
if meta_desc:
    meta_desc.decompose()
    print("Removed meta description.")

# 2. INTRODUCE STRUCTURE ERROR: Remove H1
h1 = soup.find('h1')
if h1:
    h1.decompose()
    print(f"Removed h1: {h1.get_text()}")
else:
    # If no h1 found, create one then remove it? Or just ensure we didn't miss it.
    # The previous test passed "Structure", so there MUST be an h1.
    print("Warning: No h1 found in source?")

# 3. INTRODUCE BUILD LEFTOVERS: Add TBD and Placedholder
body = soup.find('body')
if body:
    new_p = soup.new_tag("p")
    new_p.string = "This section is TBD by the dev team."
    body.insert(0, new_p)
    print("Inserted TBD paragraph.")
    
    new_div = soup.new_tag("div")
    # new_div.string = "Old config: <% CONFIG_VAR %>" # This gets escaped!
    body.append(new_div)
    print("Inserted placeholder pattern.")

# Save modified copy
html_content = str(soup)
# Inject raw placeholder that won't be escaped
html_content = html_content.replace('</body>', '<p>Raw Template: <% CONFIG_VAR %></p>\n</body>')

with open(dest_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
    
print(f"Created {dest_path}")
