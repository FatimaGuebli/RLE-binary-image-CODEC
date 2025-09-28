from PIL import Image

def rle_decode(encoded_data, size):
    """
    Decode RLE encoded data back into image pixels.
    encoded_data: list of blocks [("run", count, value), ("lit", [values])]
    size: (width, height)
    """
    pixels = []

    for block in encoded_data:
        if block[0] == "run":
            count, value = block[1], block[2]
            pixels.extend([value] * count)
        elif block[0] == "lit":
            values = block[1]
            pixels.extend(values)

    img = Image.new("L", size)  # grayscale
    img.putdata(pixels)
    return img


def load_rle_file(path):
    """
    Load .rle file saved by encoder.
    Format:
      - 2 bytes: width
      - 2 bytes: height
      - then RLE blocks
        MSB=1 → run (7 bits count + 1 byte value)
        MSB=0 → literal (7 bits count + N bytes values)
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
            if header & 0x80:  # run
                value = f.read(1)[0]
                encoded_data.append(("run", count, value))
            else:  # literal
                values = list(f.read(count))
                encoded_data.append(("lit", values))

    return encoded_data, (width, height)
