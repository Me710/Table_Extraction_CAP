import os
from pdf2image import convert_from_path

# Path to the input PDF file
pdf_path = "LLR_CAP.pdf"

# Output folder for the PNG images
output_folder = "form"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Convert PDF to images
images = convert_from_path(pdf_path)

# Save each page as a separate PNG file
for i, image in enumerate(images, start=1):
    output_path = os.path.join(output_folder, f"{i}.png")
    image.save(output_path, "PNG")

print(f"PDF '{pdf_path}' has been split into {len(images)} PNG images in the '{output_folder}' folder.")
