import os
import re
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def markdown_to_docx(md_path, docx_path):
    doc = Document()
    
    # Base style configurations
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)
    
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    in_table = False
    table_headers = []
    table_rows = []
    
    for line in lines:
        stripped = line.strip()
        
        # Table parsing
        if stripped.startswith('|'):
            # Check if this is a separator line (e.g. |---|---|)
            if re.match(r'^\|[\s:-|]+$', stripped):
                continue
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if not in_table:
                in_table = True
                table_headers = cells
            else:
                table_rows.append(cells)
            continue
        else:
            if in_table:
                # Render table
                if table_headers:
                    cols = len(table_headers)
                    table = doc.add_table(rows=1, cols=cols)
                    table.style = 'Light Shading Accent 1'
                    hdr_cells = table.rows[0].cells
                    for i, header in enumerate(table_headers):
                        hdr_cells[i].text = header
                    
                    for row_data in table_rows:
                        row_cells = table.add_row().cells
                        for i, cell_value in enumerate(row_data):
                            if i < len(row_cells):
                                row_cells[i].text = cell_value
                in_table = False
                table_headers = []
                table_rows = []
        
        if not stripped:
            continue
            
        # Headings
        if stripped.startswith('# '):
            h = doc.add_heading(stripped[2:], level=1)
            h.paragraph_format.space_before = Pt(12)
            h.paragraph_format.space_after = Pt(6)
        elif stripped.startswith('## '):
            h = doc.add_heading(stripped[3:], level=2)
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(4)
        elif stripped.startswith('### '):
            h = doc.add_heading(stripped[4:], level=3)
            h.paragraph_format.space_before = Pt(8)
            h.paragraph_format.space_after = Pt(2)
            
        # Lists
        elif stripped.startswith('- ') or stripped.startswith('* '):
            # Strip markdown bold inside lists
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', stripped[2:])
            doc.add_paragraph(text, style='List Bullet')
        elif re.match(r'^\d+\.\s', stripped):
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', re.sub(r'^\d+\.\s', '', stripped))
            doc.add_paragraph(text, style='List Number')
            
        # Regular Paragraph
        else:
            # Handle Bold formatting in text
            text = stripped
            # Basic markdown bold formatting
            p = doc.add_paragraph()
            # Simple bold parser
            parts = re.split(r'(\*\*.*?\*\*)', text)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    run.bold = True
                else:
                    p.add_run(part)
            p.paragraph_format.space_after = Pt(6)
            
    # Save the document
    doc.save(docx_path)
    print(f"Converted {md_path} to {docx_path}")

# Run converter for all docs
docs_dir = "/Users/macbook-projavlon/Desktop/Jdu/docs"
files = [
    ("1_企画書.md", "1_企画書.docx"),
    ("2_設計書.md", "2_設計書.docx"),
    ("3_作業スケジュール.md", "3_作業スケジュール.docx"),
    ("4_テスト仕様書及び結果報告書.md", "4_テスト仕様書及び結果報告書.docx"),
    ("5_作業報告書及び成果報告書.md", "5_作業報告書及び成果報告書.docx"),
    ("6_日本就業素養_自己PRと自己紹介.md", "6_日本就業素養_自己PRと自己紹介.docx")
]

for md, docx in files:
    md_fullpath = os.path.join(docs_dir, md)
    docx_fullpath = os.path.join(docs_dir, docx)
    if os.path.exists(md_fullpath):
        markdown_to_docx(md_fullpath, docx_fullpath)
