import os
from PIL import Image
from rle_code_color import code_rle

# Input path of the pic
input_path = "./images/columbina.jpg"

# Load image
img = Image.open(input_path).convert("RGB")  # ✅ keep color (RGB)

# Convert to raw bytes (R, G, B per pixel)
data = img.tobytes()
width, height = img.size  # store dimensions

# Build output path
os.makedirs("./compressed", exist_ok=True)
base_name = os.path.splitext(os.path.basename(input_path))[0]
output_path = f"./compressed/{base_name}_compressed_color.rle"

# Call your RLE encoder
code_rle(data, output_path, width, height)

print(f"✅ Color compression done! File saved at: {output_path}")

# -----------------------------
# Debugging / simple tests
# -----------------------------
original_size = len(data)
compressed_size = os.path.getsize(output_path)

print("\n--- DEBUG INFO ---")
print(f"Image dimensions: {width} x {height} (total {width*height} pixels)")
print(f"Original pixel count: {len(data)//3} (RGB)")
print(f"Original size (bytes): {original_size}")
print(f"Compressed size (bytes): {compressed_size}")

if compressed_size < original_size:
    print(f"✅ Compression worked! Ratio = {compressed_size/original_size:.2f}")
else:
    print(f"⚠️ File got bigger. Ratio = {compressed_size/original_size:.2f}")

# Quick peek at data
print("\nFirst 12 bytes (4 pixels RGB):", list(data[:12]))
with open(output_path, "rb") as f:
    comp_preview = f.read(20)
print("First 20 compressed bytes:", list(comp_preview))

print("Original pixels:", width * height)
