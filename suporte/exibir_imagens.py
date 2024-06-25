import numpy as np
import matplotlib.pyplot as plt


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
