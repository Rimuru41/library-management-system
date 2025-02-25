from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename
from flask import current_app
import textwrap


def allowed_file(filename):
    # Use the allowed extensions from the app config.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def resize_image(image_path, max_size=(600, 500)):
    """Resizes the image while maintaining aspect ratio."""
    with Image.open(image_path) as img:
        img.thumbnail(max_size) 
        img.save(image_path)  
        print(f"Image resized to {img.size}")



def create_default_cover(book_name, file_path):
    width, height = 300, 450
    padding = 20  # Space from edges

    # Create a blank image with a gradient background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Gradient effect
    for i in range(height):
        color = (200 - i // 5, 200 - i // 5, 200 - i // 5)  # Light to dark gray gradient
        draw.line([(0, i), (width, i)], fill=color)

    try:
        font = ImageFont.truetype("arial.ttf", 35)
    except IOError:
        font = ImageFont.load_default()

    # Wrap text to fit within the cover width
    max_width = width - (2 * padding)
    wrapped_text = textwrap.fill(book_name, width=15)  

    # Reduce font size if text is too long
    while True:
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if text_width <= max_width and text_height <= (height / 3):  
            break  

        # Reduce font size
        font_size = font.size - 2
        if font_size < 15:  
            break
        font = ImageFont.truetype("Baskerville.ttf", font_size) if font.size > 15 else ImageFont.load_default()

    # Center the text
    text_x = (width - text_width) / 2
    text_y = (height / 3) - (text_height / 2)

    # Text shadow
    draw.multiline_text((text_x + 2, text_y + 2), wrapped_text, font=font, fill="gray", align="center")

    # Main text
    draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill="black", align="center")

    # Add a simple border
    border_width = 5
    draw.rectangle([(border_width, border_width), (width - border_width, height - border_width)], outline="black", width=border_width)

    # Save the cover
    img.save(file_path)
    print(f"Generated cover at {file_path}")


def generate_filename_with_isbn(filename, isbn):
    """Generate a unique filename by appending ISBN to the original filename."""
    secure_name = secure_filename(filename)  
    name, ext = secure_name.rsplit('.', 1)  
    return f"{name}_{isbn}.{ext}"  

