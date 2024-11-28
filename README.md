# Steganography: Hiding Messages in Images

This Python program demonstrates a steganography technique for hiding text messages within images using the least significant bit (LSB) method. The hidden message is encoded into the image's pixel data and can be decoded later to retrieve the original message.

---

## Features

- **Encode Message**: Hide a text message inside an image.
- **Decode Message**: Extract the hidden message from an image.
- **EOF Marker**: Uses a unique end-of-file (EOF) marker to signal the end of the hidden message.
- **Base64 Encoding**: Ensures the hidden message is safely stored in binary form.

---

## Requirements

- Python 3.6+
- Libraries:
  - `Pillow` (for image manipulation)

Install dependencies:
```bash
pip install pillow
```

---

## Usage

### 1. Encode a Message into an Image
The `encode_message_to_image` function hides a message in an image.

**Function Parameters**:
- `image_path` (str): Path to the input image (e.g., `input.jpg`).
- `message` (str): Text message to encode (e.g., `"Hello, World!"`).
- `output_path` (str): Path to save the output image (e.g., `output.png`).

**Example**:
```python
msg = "Hello World :D"

# Encode the message into the image
encode_message_to_image("input.jpg", msg, "output.png")
```

**Output**:
An image file (`output.png`) containing the hidden message.

---

### 2. Decode a Message from an Image
The `decode_message_from_image` function retrieves the hidden message from an image.

**Function Parameter**:
- `image_path` (str): Path to the image containing the hidden message.

**Example**:
```python
# Decode the hidden message
hidden_message = decode_message_from_image("output.png")
print("Decoded Message:", hidden_message)
```

**Output**:
The decoded message as a string.

---

## How It Works

1. **Encoding**:
   - The text message is Base64 encoded.
   - The encoded message is converted to a binary string.
   - Binary data is embedded in the least significant bits (LSB) of the RGB channels of the image pixels.
   - An EOF marker (`1111111111111110`) is appended to indicate the end of the message.

2. **Decoding**:
   - Binary data is extracted from the LSBs of the image pixels.
   - The EOF marker is used to determine the end of the hidden message.
   - The binary data is grouped into bytes, converted back to characters, and decoded from Base64 to retrieve the original text.

---

## Example Output

### Encoding
Input:
```python
encode_message_to_image("input.jpg", "Secret Message!", "output.png")
```

Output:
- An image file (`output.png`) with the hidden message.

---

### Decoding
Input:
```python
hidden_message = decode_message_from_image("output.png")
print("Decoded Message:", hidden_message)
```

Output:
```
Decoded Message: Secret Message!
```

---

## Limitations

1. **Message Length**: The length of the hidden message is limited by the number of pixels in the image. For hiding every 3 character it needs 8 pixels.
2. **Input Image Format**: The input image should support RGBA or RGB modes.
3. **Message Visibility**: While the message is hidden, modifying the image (e.g., resizing or re-encoding) may corrupt the hidden data.
4. **Output Image Format**:  The output image cannot be jpeg or jgp and has to be png due to its lossless format.

---

## License

This project is licensed under the MIT License.

---

Enjoy hiding and retrieving secret messages with images! 🚀