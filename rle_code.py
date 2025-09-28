def code_rle(data: bytes, output_path: str, width: int, height: int) -> None:
    """
    Compress a sequence of bytes (0 or 255) using RLE
    and write the result to output_path.

    File format:
      - 2 bytes: width (big endian)
      - 2 bytes: height (big endian)
      - then RLE data blocks:
          * 1 byte: flag+count
              - MSB=1 → repeat run
              - MSB=0 → literal run
          * For repeat run: [count | 0x80][pixel_value]
          * For literal run: [count][raw bytes...]
    """

    compressed_data = bytearray()

    # --- Store dimensions first ---
    compressed_data += width.to_bytes(2, "big")
    compressed_data += height.to_bytes(2, "big")

    # --- Actual RLE encoding ---
    i = 0
    n = len(data)

    while i < n:
        current_pixel = data[i]
        count = 1

        # Count how many times this pixel repeats consecutively
        while (i + count < n) and (data[i + count] == current_pixel):
            count += 1

        if count >= 3:  # good candidate for a run
            run_count = min(count, 127)  # fits in 7 bits
            compressed_data.append(run_count | 0x80)  # MSB=1 → repeat run
            compressed_data.append(current_pixel)
            i += run_count
        else:
            # Collect literals until a run or max length
            literal_start = i
            literal_count = 1  # include current pixel
            i += 1

            while i < n:
                run_pixel = data[i]
                run_len = 1
                while (i + run_len < n) and (data[i + run_len] == run_pixel):
                    run_len += 1
                if run_len >= 3 or literal_count >= 127:
                    break
                i += 1
                literal_count += 1

            # Write literal block
            compressed_data.append(literal_count & 0x7F)  # MSB=0 → literal run
            compressed_data += data[literal_start:literal_start + literal_count]

    # Write compressed data to output file
    with open(output_path, "wb") as outfile:
        outfile.write(compressed_data)
