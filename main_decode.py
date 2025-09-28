import os
from PIL import Image
from rle_decode import load_rle_file, rle_decode

# Input/output paths
input_path = "./compressed/flower_compressed.rle"
output_path = "./images/flower_restored.png"

# Load encoded data + dimensions from .rle file
encoded_data, size = load_rle_file(input_path)

# Decode back into image
decoded_img = rle_decode(encoded_data, size)

# Save result
os.makedirs(os.path.dirname(output_path), exist_ok=True)
decoded_img.save(output_path)

print(f"✅ Decoded image saved to {output_path}")

# --- DEBUG INFO ---
decoded_pixels = list(decoded_img.getdata())
compressed_size = os.path.getsize(input_path)
decompressed_size = os.path.getsize(output_path)

print("\n--- DEBUG INFO ---")
print(f"Image size (W x H): {size[0]} x {size[1]}")
print(f"Total pixel count: {len(decoded_pixels)}")
print(f"Compressed size (bytes): {compressed_size}")
print(f"Decompressed size (bytes): {decompressed_size}")
print(f"Ratio (compressed / decompressed): {compressed_size / decompressed_size:.2f}")
print(f"\nFirst 20 decoded pixels: {decoded_pixels[:20]}")


print("Decoded pixels:", len(decoded_img.getdata()))
