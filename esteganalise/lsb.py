import cv2
import numpy as np

from suporte.exibir_imagens import show_image
from suporte.tratar_dados import bits_to_message


def bitplanes(image):
    # im = Image.open(im)
    # data = np.array(im)
    out = []
    # create an image for each k bit plane
    for k in range(7, -1, -1):
        # extract kth bit (from 0 to 7)
        res = image // 2 ** k & 1
        out.append(res * 255)
    # stack generated images
    b = np.hstack(out)

    return b.astype(np.uint8)


def recover_message(bit_planes, bits=1, n_pixels_height=340):
    # Assumindo que a imagem possui 8 bit planes horizontais (8 sub-imagens)
    height, width = bit_planes.shape
    plane_width = width // 8  # Altura de cada bit plane

    # Extrair bit planes
    last_two_frames = bit_planes[:, -(bits+1) * plane_width:-bits * plane_width]
    show_image(last_two_frames)

    # # Definir a altura da região superior (ajuste conforme necessário)
    upper_region = last_two_frames[:n_pixels_height, :]
    words = n_pixels_height * (last_two_frames.shape[1])

    flat_image_array = upper_region.flatten()

    message_bits = []
    for i in range(words):
        message_bits.append(str(flat_image_array[i] & 1))

    message_bits = ''.join(message_bits)
    message = bits_to_message(message_bits)

    print(message)

    return message


# Função para selecionar a ROI
def select_roi(image):
    # Selecionar a ROI manualmente
    roi = cv2.selectROI("Selecione a ROI", image, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Selecione a ROI")
    return roi
