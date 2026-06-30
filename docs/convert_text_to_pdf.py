import os
from PIL import Image, ImageDraw, ImageFont

def text_to_pdf(text_path, pdf_path):
    # A4 dimensions at 150 DPI
    width, height = 1240, 1754
    margin = 80
    line_spacing = 15
    
    # Read text
    with open(text_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Find a valid Japanese font on macOS
    font_paths = [
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/AquaKana.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    ]
    
    font_path = None
    for p in font_paths:
        if os.path.exists(p):
            font_path = p
            break
            
    if not font_path:
        # Fallback to default
        font = ImageFont.load_default()
        print("Warning: No Japanese font found. Using default font.")
    else:
        # Load font with reasonable sizes
        font = ImageFont.truetype(font_path, 28)
        bold_font = ImageFont.truetype(font_path, 34)
        title_font = ImageFont.truetype(font_path, 40)
        
    pages = []
    
    # Initialize first page
    img = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(img)
    y = margin
    
    for line in lines:
        stripped = line.rstrip()
        
        # Determine font and size based on markdown structure
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
            
        # Draw line by line, handle page breaks
        # Simple word wrap for long lines
        words = []
        current_line = ""
        for char in text_to_draw:
            # check width
            test_line = current_line + char
            # get width
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
                # Page break: save current, create new page
                pages.append(img)
                img = Image.new('L', (width, height), 255)
                draw = ImageDraw.Draw(img)
                y = margin
                
            draw.text((margin, y), wl, font=current_font, fill=0)
            # Get height of drawn text
            bbox = draw.textbbox((0, 0), wl, font=current_font)
            text_height = bbox[3] - bbox[1] if (bbox[3] - bbox[1]) > 0 else 30
            y += text_height + line_spacing
            
        if stripped.startswith('---'):
            y += 20 # Extra spacing for section dividers
            
    pages.append(img)
    
    # Save all images into one multi-page PDF
    if pages:
        pages[0].save(pdf_path, save_all=True, append_images=pages[1:])
        print(f"Successfully converted {text_path} to visual PDF {pdf_path}")

if __name__ == "__main__":
    import glob
    search_dir = "/Users/macbook-projavlon/Desktop/JDU_bitiruv/employability"
    # Find MD files dynamically matching the pattern to avoid encoding issues
    md_files = [os.path.join(search_dir, f) for f in os.listdir(search_dir) if "自己紹介" in f and "ひらがな" in f and f.endswith(".md")]
    
    if not md_files:
        print("Hiragana MD script file not found!")
    else:
        text_path = md_files[0]
        # Set output PDF name using the exact NFD string of the original file
        pdf_path = text_path.replace(".md", ".pdf")
        text_to_pdf(text_path, pdf_path)
