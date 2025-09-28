from PIL import Image

def rle_decode(encoded_data, size):
    """
    Decode RLE encoded color data back into image pixels.
    encoded_data: list of blocks [("run", count, (R,G,B)), ("lit", [(R,G,B), ...])]
    size: (width, height)
    """
    pixels = []

    for block in encoded_data:
        if block[0] == "run":
            count, rgb = block[1], block[2]
            pixels.extend([rgb] * count)
        elif block[0] == "lit":
            values = block[1]
            pixels.extend(values)

    # Flatten list of tuples into raw byte data
    flat_bytes = bytearray()
    for r, g, b in pixels:
        flat_bytes += bytes([r, g, b])

    img = Image.frombytes("RGB", size, bytes(flat_bytes))
    return img


def load_rle_file(path):
    """
    Load .rle file saved by encoder (color version).
    Format:
      - 2 bytes: width
      - 2 bytes: height
      - then RLE blocks:
        MSB=1 → run (7 bits count + 3 bytes RGB value)
        MSB=0 → literal (7 bits count + 3*count bytes raw RGB values)
    """
    encoded_data = []

    with open(path, "rb") as f:
        width = int.from_bytes(f.read(2), "big")
        height = int.from_bytes(f.read(2), "big")

        while True:
            header = f.read(1)
            if not header:
                break

            header = header[0]
            count = header & 0x7F

            if header & 0x80:  # run block
                rgb = tuple(f.read(3))  # (R, G, B)
                encoded_data.append(("run", count, rgb))
            else:  # literal block
                raw = f.read(count * 3)
                values = [tuple(raw[i:i+3]) for i in range(0, len(raw), 3)]
                encoded_data.append(("lit", values))

    return encoded_data, (width, height)
