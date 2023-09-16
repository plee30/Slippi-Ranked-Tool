def extract_mixed_width_text(byte_data, full_width_marker):
    text_parts = []
    i = 0

    while i < len(byte_data):
        # Check if the current byte is the full-width marker
        if byte_data[i:i+2] == full_width_marker:
            # Full-width character (2 bytes)
            text_parts.append(byte_data[i:i+2].decode('shift-jis'))
            i += 2
        else:
            # Half-width character (1 byte)
            text_parts.append(byte_data[i:i+1].decode('shift-jis'))
            i += 1

    return ''.join(text_parts)

# Example usage:
byte_data = b'\x00DF\x81\x94950\x00\x00\x00TS\x81\x94571\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
full_width_marker = b'\x81\x94'  # Replace with your full-width marker

text_result = extract_mixed_width_text(byte_data, full_width_marker)
print(text_result)
