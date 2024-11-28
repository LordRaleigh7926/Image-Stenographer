from PIL import Image
import base64

def encode_message_to_image(image_path:str, message:str, output_path:str):
    """
    Encode a message into an image.
    
    Parameters:
        image_path (str): Path to the input image.
        message (str): Text message to encode.
        output_path (str): Path to save the output image.
    """
    #  message.encode('utf-8'): Converts the text message into a byte sequence (UTF-8 format).
    # base64.b64encode(): Encodes the byte sequence in base64 format.
    # .decode('utf-8'): Converts the base64-encoded byte sequence back to a string.
    encoded_message = base64.b64encode(message.encode('utf-8')).decode('utf-8')
    
    # Open the image
    img = Image.open(image_path)
    img = img.convert('RGBA')  # Ensure image is in RGBA format
    
    # Converts all the pixels in the image into a list, where each pixel is a tuple (R, G, B, A).
    pixels = list(img.getdata())
    
    # Each character in the base64 message is converted to 8 bits (binary).
    # If the message exceeds the available pixels, it raises an error.
    if (len(encoded_message) * 8)//3 > len(pixels):
        raise ValueError("Message is too long to hide in this image.")
    
    # Modify pixel values to encode the message
    new_pixels = []

    # ord(char): Converts each character in the base64 message to its ASCII value.
    # f"{ord(char):08b}": Converts the ASCII value to an 8-bit binary string.
    # Example: "A" → ASCII 65 → Binary 01000001.
    # '1111111111111110': Appends the EOF marker, signaling the end of the hidden message.
    binary_message = ''.join(f"{ord(char):08b}" for char in encoded_message) + '1111111111111110'  # EOF marker

    message_index = 0
    
    for pixel in pixels:

        r, g, b, a = pixel
        check_rgb = 1

        '''
        r: Represents the red channel value of the current pixel (an integer between 0 and 255).

        0xFE: A hexadecimal value, equivalent to the binary 11111110.

        What It Does:
        & is a bitwise AND operator.
        r & 0xFE clears the LSB of r (makes it 0) while keeping all other bits unchanged.

        Example:
        Let's say r = 155 (binary 10011011):

        0xFE = binary 11111110.
        Perform the bitwise AND operation:

        10011011   (r)
        &
        11111110   (0xFE)
        --------
        10011010

        And then using OR operator we then change the last digit back to our desired number.
        '''

        for _ in range(3):
            if message_index < len(binary_message):
                if check_rgb == 3:
                    b = (b & 0xFE) | int(binary_message[message_index])
                    check_rgb = 1
                elif check_rgb == 2:
                    g = (g & 0xFE) | int(binary_message[message_index])
                    check_rgb = 3
                else:
                    r = (r & 0xFE) | int(binary_message[message_index])
                    check_rgb = 2

                message_index += 1
            else:
                break

        new_pixels.append((r, g, b, a))

        
    
    # Create a new image with the modified pixels
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path)
    print(f"Message encoded and saved to {output_path}")



def decode_message_from_image(image_path:str) -> str:
    """
    Decode a hidden message from an image.

    Parameters:
        image_path (str): Path to the image containing the hidden message.
    
    Returns:
        str: The decoded message.
    """

    img = Image.open(image_path)
    img = img.convert('RGBA')

    # Extract all the pixel data
    pixels = list(img.getdata())
    
    binary_message = ""
    check_rgb = 1

    # Extract binary data from the least significant bits of the RGB channels
    for pixel in pixels:
        r, g, b, a = pixel
        
        for _ in range(3):
            if check_rgb == 3:
                binary_message += str(b & 1)
                check_rgb = 1
            elif check_rgb == 2:
                binary_message += str(g & 1)
                check_rgb = 3
            else:
                binary_message += str(r & 1)
                check_rgb = 2

            # Stop if the EOF marker is detected
            if binary_message.endswith('1111111111111110'):  # EOF marker
                break
        if binary_message.endswith('1111111111111110'):
            break
    
    # Remove the EOF marker
    binary_message = binary_message[:-16]  # Remove 16 bits of the EOF marker
    
    # Group binary data into chunks of 8 bits (1 byte each)
    decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    
    # Decode the Base64 encoded message to get the original text
    return base64.b64decode(decoded_message).decode('utf-8')


# Example Usage:
if __name__ == "__main__":

    msg = "Hello World :D"

    # Hide a message
    encode_message_to_image("dummy.jpeg", msg, "hidden_msg.png")
    
    # Retrieve the message
    hidden_message = decode_message_from_image("hidden_msg.png")
    print("Decoded Message:", hidden_message)
