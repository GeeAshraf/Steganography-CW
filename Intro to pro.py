def text_to_bin(text):  # Convert text to binary
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_text(binary):  # Convert binary back to text
    message = ''.join(chr(int(binary[i:8+i], 2)) for i in range(0, len(binary), 8))
    return message

def add_txt(image_location, output_path, message):  # Embed text into image
    binary_msg = text_to_bin(message) + '1111111111110'
    with open(image_location, 'rb') as file:
        image_info = bytearray(file.read())
    index = 0
    for i in range(len(image_info)):
        if index < len(binary_msg):
            image_info[i] = (image_info[i] & 0xFE) | int(binary_msg[index])
            index += 1
        else:
            break
    with open(output_path, 'wb') as file:
        file.write(image_info)

def extract_msg(image_location):  # Extract message from image
    with open(image_location, 'rb') as file:
        binary_topic = file.read()
    binary = ''
    for byte in binary_topic:
        digit = bin(byte)[-1]  # Extract the least significant bit
        binary += digit
        if binary.endswith('1111111111110'):  # Check for end-marker
            break

    if '1111111111110' not in binary:
        raise ValueError("End-marker not found in the binary data.")

    # Remove the delimiter
    binary = binary[:binary.index('1111111111110')]

    # Ensure binary length is a multiple of 8
    if len(binary) % 8 != 0:
        raise ValueError("Binary data length is not divisible by 8 after removing the end-marker.")

    return bin_to_text(binary)

def testing_image(input_image, output_image):
    with open(input_image, 'rb') as file:
        image_info = bytearray(file.read())
    for i in range(10):
        image_info[i] = (image_info[i] + 1) % 256
    with open(output_image, 'wb') as file:
        file.write(image_info)
    print(f"Test image written to {output_image}")

def new_func(add_txt, extract_msg, testing_image, input_image, output_image, test_image_path):
    print("Testing the image writing...")
    testing_image(input_image, test_image_path)

    message = "Hello, World!"
    print(f"Embed message: {message}")
    add_txt(input_image, output_image, message)
    print(f"Message is embedded in {output_image}")

    print("Extracting hidden message...")
    try:
        hidden_message = extract_msg(output_image)
        print(f"Extracted message: {hidden_message}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    input_image = 'nature.bmp'
    output_image = 'output.bmp'
    test_image_path = 'test_output.bmp'
    new_func(add_txt, extract_msg, testing_image, input_image, output_image, test_image_path)

