from markdown import markdown
import os

# Define the applications
applications = [
    ("01_Altus_Group", "Resume_Altus_Group.md", "Cover_Letter_Altus_Group.md"),
    ("02_RBC_Analyst_Program", "Resume_RBC.md", "Cover_Letter_RBC.md"),
    ("03_CGI_Entry_Level_Analyst", "Resume_CGI.md", "Cover_Letter_CGI.md"),
    ("04_NS_Government_Data_Analyst", "Resume_NS_Gov.md", "Cover_Letter_NS_Gov.md"),
    ("05_TD_Bank_Data_Analyst", "Resume_TD.md", "Cover_Letter_TD.md"),
]

base_path = "C:/Users/vrajb/Documents/MAYAI-Knowledge/Career/Applications"

html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Calibri, Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #1a3c64;
            border-bottom: 2px solid #1a3c64;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #1a3c64;
            margin-top: 25px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #333;
            margin-top: 20px;
        }}
        strong {{
            color: #1a3c64;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ccc;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>"""

for folder, resume, cover in applications:
    folder_path = os.path.join(base_path, folder)
    
    # Convert Resume
    resume_path = os.path.join(folder_path, resume)
    if os.path.exists(resume_path):
        with open(resume_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html_content = markdown(md_content, extensions=['extra'])
        full_html = html_template.format(content=html_content)
        
        output_html = os.path.join(folder_path, resume.replace('.md', '.html'))
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"Created: {output_html}")
    
    # Convert Cover Letter
    cover_path = os.path.join(folder_path, cover)
    if os.path.exists(cover_path):
        with open(cover_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html_content = markdown(md_content, extensions=['extra'])
        full_html = html_template.format(content=html_content)
        
        output_html = os.path.join(folder_path, cover.replace('.md', '.html'))
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"Created: {output_html}")

print("\nAll HTML files created successfully!")
print("To convert to PDF, open HTML files in Chrome and print to PDF, or use a PDF converter.")
