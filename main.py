import os
from PIL import Image
from rle_codec import code_rle

# Input path of the pic
input_path = "./images/flower.png"

# Load image using PIL
img = Image.open(input_path)

# Convert to grayscale
gray = img.convert("L")

# Apply threshold to make it strictly black & white
bw = gray.point(lambda x: 255 if x > 128 else 0)

# Convert the raw pixel bytes (0 or 255)
data = bw.tobytes()

# Build output path
os.makedirs("./compressed", exist_ok=True)
base_name = os.path.splitext(os.path.basename(input_path))[0]
output_path = f"./compressed/{base_name}_compressed.rle"

# Call your RLE encoder
code_rle(data, output_path)

print(f"Compression done! File saved at: {output_path}")
