def text_to_bin(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_text(binary):
    message = ''.join(chr(int(binary[i:8+i], 2))for i in range(0, len(binary), 8))

def add_text(image_path, output_path, message):
    binary_msg = text_to_bin(message) + '1111111111110'
    with open(image_path, 'rb') as file:
        image_data = bytearray(file.read())

        index = 0
        for i in range(len(image_data)):
            if index < len(binary_msg):
                image_data[i] = (image_data[i] & 0xFE) | int(binary_msg[index])
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
        if binary[:-16] == '11111111111110':
            break
        if '11111111111110' not in binary:
            print("debug: delimeter not found.")
            raise ValueError("not found.")
        if len(binary) % 8 !=0:
            raise ValueError("Error: Length not divisble by 8.")
        
    return bin_to_text(binary)
print(extract_text('D:/nature.bmp')) 
                   
def test_image(input_image, output_image):
    with open(input_image, 'rb') as file:
        image_data = bytearray(file.read())
    for i in range(10):
        image_data[i] = (image_data[i] + 1) % 256
    with open(output_image, 'wb') as file:
        file.write(image_data)
    print(f"test image{output_image}")

if __name__ == '__main__':
    input_image = 'image.bmp'
    output_image = 'output.bmp'
    test_image = 'test_output.bmp'

    print("testing the image writing...")
    test_image(input_image, testing_image)
    
    message = "hello, World!"
    print(f"Embed message: {message}")
    add_text(input_image, output_image, message)
    print(f"message is embedded in{output_image}")

    print("extracting hidden message...")
    try:
        hidden_message = extracting_text(output_image)
        print(f"extrcated message: {hidden_message}")
    except ValueError as e:
        print(f"Error: {e}")


