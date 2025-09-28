import os
from PIL import Image
from rle_code import code_rle

# Input path of the pic
input_path = "./images/flower.png"

# Load image
img = Image.open(input_path)

# Convert to grayscale
gray = img.convert("L")

# Apply threshold to make it strictly black & white
bw = gray.point(lambda x: 255 if x > 128 else 0)

# Convert to raw bytes (0 or 255)
data = bw.tobytes()
width, height = bw.size  # store dimensions here ✅

# Build output path
os.makedirs("./compressed", exist_ok=True)
base_name = os.path.splitext(os.path.basename(input_path))[0]
output_path = f"./compressed/{base_name}_compressed.rle"

# Call your RLE encoder
code_rle(data, output_path, width, height)

print(f"✅ Compression done! File saved at: {output_path}")

# -----------------------------
# Debugging / simple tests
# -----------------------------
original_size = len(data)
compressed_size = os.path.getsize(output_path)

print("\n--- DEBUG INFO ---")
print(f"Image dimensions: {width} x {height} (total {width*height} pixels)")
print(f"Original pixel count: {len(data)}")
print(f"Original size (bytes): {original_size}")
print(f"Compressed size (bytes): {compressed_size}")

if compressed_size < original_size:
    print(f"✅ Compression worked! Ratio = {compressed_size/original_size:.2f}")
else:
    print(f"⚠️ File got bigger. Ratio = {compressed_size/original_size:.2f}")

# Quick peek at data
print("\nFirst 20 pixels:", list(data[:20]))
with open(output_path, "rb") as f:
    comp_preview = f.read(20)
print("First 20 compressed bytes:", list(comp_preview))


print("Original pixels:", width * height)
