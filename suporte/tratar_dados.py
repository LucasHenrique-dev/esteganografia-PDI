import cv2
import numpy as np
import imageio.v2 as imageio
from IPython.display import HTML
from base64 import b64encode


def image_to_array(image_path, gray=True):
    if gray:
        return imageio.imread(image_path)
    else:
        return imageio.imread(image_path, pilmode='RGBA')


def sumarize(image_array):
    # Calcular o menor valor
    menor_valor = np.min(image_array)

    # Calcular o maior valor
    maior_valor = np.max(image_array)

    # Calcular o valor médio
    valor_medio = np.mean(image_array)

    # Encontrar os valores únicos no array
    valores_unicos = np.unique(image_array)

    # Obter a altura e largura da imagem
    altura, largura = image_array.shape[:2]

    # Obter dimensões de profundidade
    canais_cores = 1 if len(image_array.shape) < 3 else image_array.shape[2]

    print(f"Menor Valor: {menor_valor}\nMaior Valor: {maior_valor}\nValor Médio: {valor_medio}\n"
          f"Valores Únicos: {valores_unicos}\nResolução da imagem (Largura X Altura): {largura} X {altura}\n"
          f"Canais de Cores: {canais_cores}")


def gray_scale(imagem_array, verbose=False):
    # Converter a imagem para escala de cinza
    cinza_array = np.dot(imagem_array[..., :3],
                         [0.2989, 0.5870, 0.1140])  # Ponderação das cores baseado na percepção humana

    if len(np.shape(imagem_array)) > 2 and imagem_array.shape[2] > 3:
        alpha = imagem_array[..., 3]

        # Ajustar os valores de escala de cinza para preservar o fundo branco
        cinza_array[alpha < 255] = 255

    if verbose:
        print(f"Imagem Original: {imagem_array}\n")
        print(f"Imagem Alterada: {cinza_array}\n")

    return cinza_array.astype(np.uint8)


def salvar_imagem(nome_arquivo, imagem, path=""):
    """
    Salva uma imagem em um arquivo.

    Args:
    - nome_arquivo: O nome do arquivo de destino.
    - imagem: A imagem a ser salva.
    """
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)  # Convertendo de BGR para RGB
    cv2.imwrite(path + "/" + nome_arquivo, imagem)
    print(f"Imagem salva como '{nome_arquivo}'.")


def transicao_visual(nome_video, imagens):
    # Criar o arquivo de vídeo
    imageio.mimsave(nome_video, imagens, fps=1)

    mp4 = open(nome_video, 'rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()

    return HTML("""
  <video width={img_width} controls loop>
        <source src="%s" type="video/mp4">
  </video>
  """ % data_url)


def message_to_bits(message):
    bits = ''.join(format(ord(char), '08b') for char in message)
    return bits


def bits_to_message(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message = ''.join(chr(int(char, 2)) for char in chars)
    return message
