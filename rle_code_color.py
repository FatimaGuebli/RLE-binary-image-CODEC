def code_rle(data: bytes, output_path: str, width: int, height: int) -> None:
    """
    Compress a sequence of RGB bytes using RLE and write the result.

    File format:
      - 2 bytes: width (big endian)
      - 2 bytes: height (big endian)
      - then RLE data blocks:
          * 1 byte: flag+count
              - MSB=1 → repeat run
              - MSB=0 → literal run
          * For repeat run: [count | 0x80][R][G][B]
          * For literal run: [count][(R,G,B) * count]
    """

    compressed_data = bytearray()

    # --- Store dimensions first ---
    compressed_data += width.to_bytes(2, "big")
    compressed_data += height.to_bytes(2, "big")

    # --- Work on pixels (3 bytes each) ---
    pixels = [data[i:i+3] for i in range(0, len(data), 3)]
    n = len(pixels)
    i = 0

    while i < n:
        current_pixel = pixels[i]
        count = 1

        # Count how many times this pixel repeats consecutively
        while (i + count < n) and (pixels[i + count] == current_pixel):
            count += 1

        if count >= 3:  # encode as run
            run_count = min(count, 127)  # 7 bits
            compressed_data.append(run_count | 0x80)  # MSB=1 → run
            compressed_data += current_pixel  # write R, G, B
            i += run_count
        else:
            # Collect literal pixels until run or max 127
            literal_start = i
            literal_count = 1
            i += 1

            while i < n:
                run_pixel = pixels[i]
                run_len = 1
                while (i + run_len < n) and (pixels[i + run_len] == run_pixel):
                    run_len += 1
                if run_len >= 3 or literal_count >= 127:
                    break
                i += 1
                literal_count += 1

            # Write literal block
            compressed_data.append(literal_count & 0x7F)  # MSB=0 → literal
            for px in pixels[literal_start:literal_start + literal_count]:
                compressed_data += px  # append R,G,B

    # Write compressed data to file
    with open(output_path, "wb") as outfile:
        outfile.write(compressed_data)
