from suporte.tratar_dados import image_to_array, message_to_bits, salvar_imagem, bits_to_message, gray_scale
import numpy as np

"""
def encode_lsb(image_path, message):
    # Carrega a imagem
    img = image_to_array(image_path)

    # Converte a mensagem para binário
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Verifica se a imagem é grande o suficiente para a mensagem
    if len(binary_message) > img.width * img.height:
        print("Erro: A mensagem é muito longa para a imagem.")
        return

    # Esconde a mensagem nos bits menos significativos dos pixels
    index = 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            if index < len(binary_message):
                r = (r & 0xFE) | int(binary_message[index])
                index += 1
            pixels[x, y] = (r, g, b)

    # Salva a imagem com a mensagem escondida
    img.save("imagem_com_mensagem.png")
    print("Mensagem escondida com sucesso!")
"""


def embed_message(image_path, message, image_title, output_path):
    image_array = image_to_array(image_path)
    # gray_img = gray_scale(image_array, False)
    gray_img = image_array

    message_bits = message_to_bits(message)
    message_length = len(message_bits)

    if message_length > gray_img.size:
        raise ValueError("Mensagem muito longa para a imagem fornecida.")

    flat_image_array = gray_img.flatten()

    for i in range(message_length):
        bit = int(message_bits[i])
        pixel_value = int(flat_image_array[i])
        flat_image_array[i] = (pixel_value & ~1) | bit

    image_array = flat_image_array.reshape(gray_img.shape).astype(np.uint8)
    salvar_imagem(image_title, image_array, path=output_path)
    print(f"Mensagem embutida com sucesso e salva em {output_path}/{image_title}")


def extract_message(image_path, message_length):
    image_array = image_to_array(image_path)

    flat_image_array = image_array.flatten()

    message_bits = []
    for i in range(message_length * 8):
        message_bits.append(str(flat_image_array[i] & 1))

    message_bits = ''.join(message_bits)
    message = bits_to_message(message_bits)
    return message


# def hide_message_in_image(image_array, message_bits):
#     bit_idx = 0
#     for i in range(image_array.shape[0]):
#         for j in range(image_array.shape[1]):
#             for k in range(image_array.shape[2]):
#                 if bit_idx < len(message_bits):
#                     # Pegando o bit menos significativo e substituindo pelo bit da mensagem
#                     image_array[i, j, k] = (int(image_array[i, j, k]) & ~1) | int(message_bits[bit_idx])
#                     bit_idx += 1
#     return image_array
#
#
# def extract_message_from_image(image_array, message_length):
#     bits = []
#     bit_idx = 0
#     for i in range(image_array.shape[0]):
#         for j in range(image_array.shape[1]):
#             for k in range(image_array.shape[2]):
#                 if bit_idx < message_length * 8:
#                     bits.append(str(image_array[i, j, k] & 1))
#                     bit_idx += 1
#     return bits_to_message(bits)


cover_folder = "cover_images"
save_folder = "stego_images"
cover_image = "halloween.jpg"
stego_image = "halloween_secreto.png"
secret = "Hello World!"

embed_message(f"{cover_folder}/{cover_image}", secret, stego_image, save_folder)

secret_message = extract_message(f"{save_folder}/{stego_image}", len(secret))

print(f"Mensagem Secreta: {secret_message}")

# https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2
