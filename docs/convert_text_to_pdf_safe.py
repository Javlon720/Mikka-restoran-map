import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import pypdf

def text_to_pdf_safe(text_path, pdf_path):
    width, height = 1240, 1754
    margin = 80
    line_spacing = 18
    
    with open(text_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    font_paths = [
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/AquaKana.ttc",
        "/Library/Fonts/Arial Unicode.ttf"
    ]
    
    font_path = None
    for p in font_paths:
        if os.path.exists(p):
            font_path = p
            break
            
    if not font_path:
        font = ImageFont.load_default()
        print("Warning: Using default font.")
    else:
        font = ImageFont.truetype(font_path, 28)
        bold_font = ImageFont.truetype(font_path, 34)
        title_font = ImageFont.truetype(font_path, 40)
        
    png_paths = []
    page_num = 1
    
    # Initialize first page
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    y = margin
    
    for line in lines:
        stripped = line.rstrip()
        current_font = font
        
        if stripped.startswith('# '):
            current_font = title_font
            text_to_draw = stripped[2:]
            y += 20
        elif stripped.startswith('## '):
            current_font = bold_font
            text_to_draw = stripped[3:]
            y += 15
        elif stripped.startswith('★') or stripped.startswith('**'):
            current_font = bold_font
            text_to_draw = stripped.replace('**', '')
        else:
            current_font = font
            text_to_draw = stripped
            
        # Text wrap logic
        words = []
        current_line = ""
        for char in text_to_draw:
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=current_font)
            line_width = bbox[2] - bbox[0]
            if line_width > (width - 2 * margin):
                words.append(current_line)
                current_line = char
            else:
                current_line = test_line
        words.append(current_line)
        
        for wl in words:
            if y + 40 > (height - margin):
                # Save page as PNG
                png_path = f"/tmp/page_{page_num}.png"
                img.save(png_path, "PNG")
                png_paths.append(png_path)
                page_num += 1
                
                # New Page
                img = Image.new('RGB', (width, height), 'white')
                draw = ImageDraw.Draw(img)
                y = margin
                
            draw.text((margin, y), wl, font=current_font, fill='black')
            bbox = draw.textbbox((0, 0), wl, font=current_font)
            text_height = bbox[3] - bbox[1] if (bbox[3] - bbox[1]) > 0 else 30
            y += text_height + line_spacing
            
        if stripped.startswith('---'):
            y += 25
            
    # Save final page
    png_path = f"/tmp/page_{page_num}.png"
    img.save(png_path, "PNG")
    png_paths.append(png_path)
    
    # Convert PNGs to PDFs using macOS sips tool
    pdf_pages = []
    for png_p in png_paths:
        pdf_p = png_p.replace(".png", ".pdf")
        # Run sips tool (built-in macOS command)
        subprocess.run(["sips", "-s", "format", "pdf", png_p, "--out", pdf_p], stdout=subprocess.DEVNULL)
        pdf_pages.append(pdf_p)
        
    # Merge PDFs using pypdf
    merger = pypdf.PdfWriter()
    for pdf_p in pdf_pages:
        merger.append(pdf_p)
        
    merger.write(pdf_path)
    merger.close()
    
    # Cleanup temp files
    for png_p, pdf_p in zip(png_paths, pdf_pages):
        try:
            os.remove(png_p)
            os.remove(pdf_p)
        except:
            pass
            
    print(f"Successfully generated clean visual PDF at {pdf_path}")

if __name__ == "__main__":
    search_dir = "/Users/macbook-projavlon/Desktop/JDU_bitiruv/employability"
    md_files = [os.path.join(search_dir, f) for f in os.listdir(search_dir) if "自己紹介" in f and "ひらがな" in f and f.endswith(".md")]
    
    if not md_files:
        print("Hiragana MD script file not found!")
    else:
        text_path = md_files[0]
        pdf_path = text_path.replace(".md", ".pdf")
        text_to_pdf_safe(text_path, pdf_path)
