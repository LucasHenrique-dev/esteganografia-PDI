import numpy as np
import matplotlib.pyplot as plt

from suporte.tratar_dados import gray_scale


def show_image(image_array, gray=True):
    if gray:
        # Exibir a imagem em escala de cinza
        plt.imshow(image_array, cmap="gray")
    else:
        plt.imshow(image_array)
    plt.axis('off')  # Desativar os eixos
    plt.show()


def comparar_imagens(*imagens, titulos=None, gray=True):
    if titulos is None:
        titulos = []
    num_imagens = len(imagens)

    if num_imagens == 2:
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    elif num_imagens == 3:
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    else:
        raise ValueError("Número de imagens inválido. A função só pode lidar com 2 ou 3 imagens.")

    for i in range(num_imagens):
        # Exibir a imagem na subplot correspondente
        if gray:
            axs[i].imshow(imagens[i], cmap="gray")
        else:
            axs[i].imshow(imagens[i])

        # Definir o título da imagem, se fornecido
        if i < len(titulos):
            axs[i].set_title(titulos[i])

        axs[i].axis('off')

    # Mostrar a figura
    plt.show()


def plotar_histograma(imagem, titulo_imagem='Imagem', titulo_histograma='Histograma'):
    # Configurar a figura e as subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Exibir a imagem na primeira subplot
    axs[0].imshow(imagem, cmap='gray')
    axs[0].set_title(titulo_imagem)
    axs[0].axis('off')

    # Calcular e plotar o histograma na segunda subplot
    histograma, bins = np.histogram(imagem.flatten(), bins=256, range=(0, 256))
    axs[1].bar(bins[:-1], histograma, width=1)
    axs[1].set_title(titulo_histograma)
    axs[1].set_xlabel('Intensidade de Pixel')
    axs[1].set_ylabel('Frequência')

    # Mostrar a figura
    plt.show()


def compare_histograms(images, titles=None):
    if titles is None:
        titles = []
    num_images = len(images)
    histograma = []

    fig, axs = plt.subplots(1, 3, figsize=(20, 5))
    histograma.append(np.histogram(images[0], bins=256, range=(0, 256)))
    histograma.append(np.histogram(images[1], bins=256, range=(0, 256)))
    hist_diff = abs(histograma[0][0] - histograma[1][0])
    bin_centers = (histograma[0][1][:-1] + histograma[0][1][1:]) / 2

    for i in range(num_images):
        if images[i].ndim <= 2:  # Grayscale image
            axs[i].bar(histograma[i][1][:-1], histograma[i][0], color='gray', label='Grayscale', width=1)
        else:  # RGB image
            for j, color in enumerate(['r', 'g', 'b']):
                axs[i].bar(histograma[i][1][:-1], histograma[i][0], color=color,
                           label=f'Channel {color.upper()}', width=1)

        # Definir o título da imagem, se fornecido
        if i < len(titles):
            axs[i].set_title(titles[i])

    axs[2].bar(bin_centers, hist_diff, width=(histograma[0][1][1] - histograma[0][1][0]), color='green')
    axs[2].set_title('Difference in Histograms (Modified - Original)')
    axs[2].set_xlabel('Value')
    axs[2].set_ylabel('Difference in Count')

    # Mostrar a figura
    plt.show()


def frequency_domain_analysis_single(image):
    if image.ndim == 3:
        gray = gray_scale(image, verbose=False)
    else:
        gray = image
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))

    plt.figure(figsize=(12, 6))
    plt.subplot(121), plt.imshow(gray, cmap='gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.show()
