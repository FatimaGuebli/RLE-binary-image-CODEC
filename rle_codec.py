def code_rle(data: bytes, output_path: str) -> None:
    """
    Compress a sequence of bytes (0 or 255) using RLE
    and write the result to output_path.
    """

    compressed_data = bytearray()
    i = 0
    n = len(data)

    while i < n:
        current_pixel = data[i]
        count = 1

        # Count how many times this pixel repeats consecutively
        while (i + count < n) and (data[i + count] == current_pixel):
            count += 1

        if count >= 3:
            # Repeated run: [1 byte count][1 byte pixel]
            # Count limited to 255 for 1 byte storage
            run_count = min(count, 255)
            compressed_data.append(run_count | 0x80)  # MSB=1 means repeat
            compressed_data.append(current_pixel)
            i += run_count

        else:
            # Literal run (non-repeating)
            literal_start = i
            literal_count = 0
            while i < n:
                run_pixel = data[i]
                run_len = 1
                while (i + run_len < n) and (data[i + run_len] == run_pixel):
                    run_len += 1
                if run_len >= 3 or literal_count >= 255:
                    break
                i += 1
                literal_count += 1

            compressed_data.append(literal_count & 0x7F)  # MSB=0 means literal
            compressed_data += data[literal_start:literal_start + literal_count]

    # Write compressed data to output file
    with open(output_path, "wb") as outfile:
        outfile.write(compressed_data)



