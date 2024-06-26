from esteganalise.lsb import bitplanes
from suporte.analisar_imagens import calculate_psnr, ssim_diff_images, get_calculation_psnr_ssim
from suporte.exibir_imagens import compare_histograms, show_image, frequency_domain_analysis_single
from suporte.tratar_dados import image_to_array, message_to_bits, salvar_imagem, bits_to_message, gray_scale, \
    interpolacao_replicacao
import numpy as np


def encode_lsb(image_path, message, image_title, output_path, grayscale=False):
    image_array = image_to_array(image_path, grayscale)

    message_bits = message_to_bits(message)
    message_length = len(message_bits)

    if message_length > image_array.size:
        raise ValueError("Mensagem muito longa para a imagem fornecida.")

    flat_image_array = image_array.flatten()

    for i in range(message_length):
        bit = int(message_bits[i])
        pixel_value = int(flat_image_array[i])
        flat_image_array[i] = (pixel_value & ~1) | bit

    modified_imge = flat_image_array.reshape(image_array.shape).astype(np.uint8)
    salvar_imagem(image_title, modified_imge, path=output_path)
    print(f"Mensagem embutida com sucesso e salva em {output_path}/{image_title}")


def encode_image_lsb(cover_image_path, secret_image_path, image_title, output_path, grayscale=False):
    cover_image = image_to_array(cover_image_path, grayscale)
    secret_image = image_to_array(secret_image_path, grayscale)

    # Verificar se as duas imagens têm o mesmo tamanho
    if cover_image.shape != secret_image.shape:
        secret_image = interpolacao_replicacao(secret_image, cover_image.shape[0], cover_image.shape[1])
        # raise ValueError("A imagem de cobertura e a imagem secreta devem ter o mesmo tamanho.")

    # Achatar as imagens
    flat_cover = cover_image.flatten()
    flat_secret = secret_image.flatten()

    # Modificar os bits menos significativos da imagem de cobertura
    for i in range(len(flat_secret)):
        pixel_cover = int(flat_cover[i])
        pixel_secret = int(flat_secret[i])
        flat_cover[i] = (pixel_cover & ~1) | (pixel_secret & 1)

    # Reformar a imagem de cobertura modificada
    encoded_image = flat_cover.reshape(cover_image.shape)

    # Salvar a imagem codificada
    salvar_imagem(image_title, encoded_image, output_path)
    print(f"Imagem secreta embutida com sucesso e salva em {output_path}")


def decode_lsb(image_path, message_length, grayscale=False):
    image_array = image_to_array(image_path, grayscale)

    flat_image_array = image_array.flatten()

    message_bits = []
    for i in range(message_length * 8):
        message_bits.append(str(flat_image_array[i] & 1))

    message_bits = ''.join(message_bits)
    message = bits_to_message(message_bits)
    return message


# def decode_image_lsb(encoded_image_path):
#     encoded_image = image_to_array(encoded_image_path)
#
#     # Achatar a imagem codificada
#     flat_encoded = encoded_image.flatten()
#
#     # Recuperar os bits menos significativos
#     secret_bits = [pixel & 1 for pixel in flat_encoded]
#
#     # Reformar a imagem secreta
#     secret_image = np.array(secret_bits).reshape(encoded_image.shape) * 255
#
#     return secret_image


def decode_image_lsb(encoded_image_path, grayscale=False):
    encoded_image = image_to_array(encoded_image_path, grayscale)

    # Recuperar a imagem secreta dos bits menos significativos
    secret_image = encoded_image & 1
    secret_image = secret_image * 255  # Converter bits de volta para a escala completa de 0 a 255

    return secret_image


# cover_folder = "../imagens_diversas"
# save_folder = "stego_images"
# cover_image = "mulher_chapeu.png"
# stego_image = "mulher_chapeu_segredo.png"
# secret = "../imagens_diversas/qrcode_hello_world.png"

cover_folder = "cover_images"
save_folder = "stego_images"
cover_image = "../imagens_diversas/qrcode_hello_world.png"
stego_image = "gray_halloween_segredo.png"
secret = "stego_images/kaggle_gray_1.png"

# ESCONDER TEXTO
# encode_lsb(f"{cover_folder}/{cover_image}", secret, stego_image, save_folder)
#
# secret_message = decode_lsb(f"{save_folder}/{stego_image}", len(secret))
#
# print(f"Mensagem Secreta: {secret_message}")

# ESCONDER IMAGEM
# encode_image_lsb(f"{cover_image}", secret, stego_image, save_folder, True)

# secret_image = decode_image_lsb(f"{save_folder}/{stego_image}", True)
#
# print(f"Mensagem Secreta:")
# show_image(secret_image)

img1 = image_to_array(f"{secret}", True)
# img2 = image_to_array(f"{save_folder}/{stego_image}", True)
bit_planes = bitplanes(img1)

show_image(bit_planes)
# compare_histograms([img1, img2], ["Imgem 1", "Imgem 2"])
# frequency_domain_analysis_single(img1)
# frequency_domain_analysis_single(img2)
# calculate_psnr(img1, img2)
# ssim_diff_images(img1, img2)
# get_calculation_psnr_ssim(img1, img2)

# https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2
