from PIL import Image, ImageOps

def resize_webp_image(input_path, output_path, size=(300, 450), output_format="JPEG"):
    """
    Resizes a WebP image to 300x450 pixels while maintaining aspect ratio.
    Converts it to a different format (JPEG by default).
    """
    img = Image.open(input_path)

    # Preserve aspect ratio and fit within the target size
    img.thumbnail(size, Image.LANCZOS)

    # Create a new white background image
    new_img = Image.new("RGB", size, "white")

    # Calculate position to center the resized image
    x_offset = (size[0] - img.size[0]) // 2
    y_offset = (size[1] - img.size[1]) // 2

    # Paste the resized image onto the white background
    new_img.paste(img, (x_offset, y_offset))

    # Convert and save in the specified format
    new_img.save(output_path, format=output_format)
    print(f"Resized image saved as {output_path} in {output_format} format.")

# Example Usage
resize_webp_image("background.webp", "output.jpg")  # Convert WebP to JPEG (or change to PNG)
