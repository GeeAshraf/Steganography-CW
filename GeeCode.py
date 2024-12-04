def text_to_bin(text):
    return ''.join(format(ord(char), '08b') for char in text)
 
def bin_to_text(binary):
    return ''.join(chr(int(binary[i:8+i], 2)) for i in range(0, len(binary), 8))
 
def add_text(image_path, output_path, message):
    binary_msg = text_to_bin(message) + '11111111111110'  # Add delimiter
    with open(image_path, 'rb') as file:
        image_data = bytearray(file.read())
        index = 0
        for i in range(len(image_data)):
            if index < len(binary_msg):
                image_data[i] = (image_data[i] & 0xFE) | int(binary_msg[index])
                index += 1
            else:
                break
        with open(output_path, 'wb') as file:
            file.write(image_data)
 
def extract_text(image_path):
    with open(image_path, 'rb') as file:
        binary_topic = file.read()
    binary = ''
    for byte in binary_topic:
        digit = bin(byte)[-1]
        binary += digit
        if '11111111111110' in binary:
            break
    if '11111111111110' not in binary:
        raise ValueError("Delimiter not found in the image.")
    binary = binary[:binary.index('11111111111110')]
    if len(binary) % 8 != 0:
        raise ValueError("Error: Length of binary string is not divisible by 8.")
    return bin_to_text(binary)
 
def test_image_function(input_image, output_image):
    with open(input_image, 'rb') as file:
        image_data = bytearray(file.read())
    for i in range(10):
        image_data[i] = (image_data[i] + 1) % 256
    with open(output_image, 'wb') as file:
        file.write(image_data)
    print(f"Test image written to {output_image}")
 
if __name__ == '__main__':
    input_image = 'nature.bmp'
    output_image = 'outputgann.bmp'
    test_image = 'test_output.bmp'
 
    print("Testing the image writing...")
    test_image_function(input_image, test_image)
 
    message = "Meet me at our spot!"
    print(f"Embed message: {message}")
    add_text(input_image, output_image, message)
    print(f"Message is embedded in {output_image}")
 
    print("Extracting hidden message...")
    try:
        hidden_message = extract_text(output_image)
        print(f"Extracted message: {hidden_message}")
    except ValueError as e:
        print(f"Error: {e}")
 