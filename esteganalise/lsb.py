import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import chi2

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
    # -(bits+1) * plane_width:-bits * plane_width -> Extrair um frame intermediario
    last_two_frames = bit_planes[:, -bits * plane_width:]
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


def calculate_entropy(image):
    histogram, _ = np.histogram(image.flatten(), bins=256, range=(0, 256))
    histogram_size = sum(histogram)
    entropy = 0

    for pixel in histogram:
        if pixel > 0:
            probability = pixel / histogram_size
            entropy -= probability * np.log2(probability)

    return entropy


def chi_square(image):
    pixels = np.array(image).flatten()
    n = len(pixels)

    observed = np.bincount(pixels, minlength=256)
    expected = np.full(256, n / 256)

    chi_square_stat = np.sum((observed - expected) ** 2 / expected)
    p_value = chi2.sf(chi_square_stat, df=255)

    return chi_square_stat, p_value


def calculate_correlation(image):
    pixels = np.array(image, dtype=np.float64)
    rows, cols = pixels.shape
    correlation_horizontal = []
    correlation_vertical = []

    for i in range(rows):
        for j in range(cols - 1):
            correlation_horizontal.append(pixels[i, j] * pixels[i, j + 1])

    for i in range(rows - 1):
        for j in range(cols):
            correlation_vertical.append(pixels[i, j] * pixels[i + 1, j])

    mean_horizontal = np.mean(correlation_horizontal)
    mean_vertical = np.mean(correlation_vertical)

    return mean_horizontal, mean_vertical


def visualize_differences(original_image, modified_image):
    diff = np.abs(np.array(original_image) - np.array(modified_image))
    plt.imshow(diff, cmap='hot')
    plt.title('Visualização de Diferenças de Pixels')
    plt.show()


def analyze_subimages(image, subimage_size=8):
    pixels = np.array(image)
    rows, cols = pixels.shape
    patterns = []

    for i in range(0, rows, subimage_size):
        for j in range(0, cols, subimage_size):
            subimage = pixels[i:i+subimage_size, j:j+subimage_size]
            if subimage.shape == (subimage_size, subimage_size):
                pattern = np.mean(subimage)
                patterns.append(pattern)

    return patterns
