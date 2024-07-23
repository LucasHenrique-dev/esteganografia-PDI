import numpy as np
from PIL import Image
import random

def message_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    print('Length: ' + str(len(binary_message)))
    return binary_message

def binary_to_message(binary_str):
    # Split the binary string into chunks of 8 bits
    bytes_list = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    # Convert each chunk to the corresponding ASCII character
    characters = [chr(int(byte, 2)) for byte in bytes_list]
    # Combine the characters to form the original message
    message = ''.join(characters)
    return message

def extract_bit(value, bit_position):
    return (value >> bit_position) & 1

def modify_bits(value, bit_positions, bit_values):
    for bit_position, bit_value in zip(bit_positions, bit_values):
        mask = 1 << bit_position
        value &= ~mask  # Clear the bit at bit_position
        if bit_value:
            value |= mask  # Set the bit if bit_value is 1
    return value

def embed_message_ssbn(image_path, message, password, N):
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    pixels = np.array(image)
    h, w = pixels.shape
    l_c = h * w
    l_m = len(message)
    E_l = l_c // l_m

    # Divide the image into regions and calculate central pixels
    regions = [(i * E_l, (i + 1) * E_l) for i in range(l_m)]

    # Seed the PRNG with the password
    random.seed(password)
    random_regions = random.sample(regions, l_m)

    for i in range(0, len(message), N):
        bits = message[i:i+N]
        start, end = random_regions[i // N]
        central_pixel_index = (start + end) // 2
        y, x = divmod(central_pixel_index, w)

        # Modify the N LSBs of the central pixel
        original_value = pixels[y, x]
        bit_positions = list(range(N))  # Bit positions to modify
        bit_values = [int(bit) for bit in bits]
        new_value = modify_bits(original_value, bit_positions, bit_values)
        pixels[y, x] = new_value

    # Save the modified image
    modified_image = Image.fromarray(pixels)
    modified_image.save('modified_ssbn_' + image_path.split('/')[-1])

def extract_bits(value, bit_positions):
    return [((value >> bit_position) & 1) for bit_position in bit_positions]

def decrypt_message_ssbn(image_path, password, message_length, N):
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    pixels = np.array(image)
    h, w = pixels.shape
    l_c = h * w
    l_m = message_length
    E_l = l_c // l_m

    # Divide the image into regions and calculate central pixels
    regions = [(i * E_l, (i + 1) * E_l) for i in range(l_m)]

    # Seed the PRNG with the password
    random.seed(password)
    random_regions = random.sample(regions, l_m // N)

    extracted_bits = []
    for start, end in random_regions:
        central_pixel_index = (start + end) // 2
        y, x = divmod(central_pixel_index, w)
        # Extract the N LSBs of the central pixel
        pixel_value = pixels[y, x]
        bit_positions = list(range(N))
        bits = extract_bits(pixel_value, bit_positions)
        extracted_bits.extend(bits)

    # Combine extracted bits to reconstruct the message
    message = ''.join(map(str, extracted_bits[:message_length]))
    return message

def bit_plane_slicing(image_path):
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    pixels = np.array(image)
    bit_planes = []
    for bit in range(8):  # 8 bit-planes for an 8-bit grayscale image
        bit_plane = (pixels >> bit) & 1  # Extract the bit-plane
        bit_planes.append(bit_plane * 255)  # Scale to 0-255 for visualization
    return bit_planes

def plot_bit_planes(bit_planes, image_title):
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    fig.suptitle(image_title)
    for i, ax in enumerate(axes.flatten()):
        ax.imshow(bit_planes[7 - i], cmap='gray')
        ax.set_title(f'Bit-plane {i + 1}')
        ax.axis('off')
    plt.show()

def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr_value = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr_value
