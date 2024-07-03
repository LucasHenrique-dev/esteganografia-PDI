import numpy as np
import matplotlib.pyplot as plt
# from skimage import img_as_float
from skimage.metrics import structural_similarity as ssim, structural_similarity
import cv2

from suporte.tratar_dados import gray_scale


def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr_value = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr_value


def calculate_ssim(original_image, noisy_image):
    K1 = 0.01
    K2 = 0.03
    L = 255
    c1 = (K1 * L) ** 2
    c2 = (K2 * L) ** 2

    # Se a imagem for colorida (3 canais), calcular SSIM para cada canal e tirar a média
    if original_image.ndim == 3:
        ssim = 0
        for i in range(original_image.shape[2]):
            mu1 = np.mean(original_image[:, :, i])
            mu2 = np.mean(noisy_image[:, :, i])
            sigma1_sq = np.var(original_image[:, :, i])
            sigma2_sq = np.var(noisy_image[:, :, i])
            sigma12 = np.mean((original_image[:, :, i] - mu1) * (noisy_image[:, :, i] - mu2))
            ssim += ((2 * mu1 * mu2 + c1) * (2 * sigma12 + c2)) / (
                        (mu1 ** 2 + mu2 ** 2 + c1) * (sigma1_sq + sigma2_sq + c2))
        ssim /= original_image.shape[2]
    else:
        mu1 = np.mean(original_image)
        mu2 = np.mean(noisy_image)
        sigma1_sq = np.var(original_image)
        sigma2_sq = np.var(noisy_image)
        sigma12 = np.mean((original_image - mu1) * (noisy_image - mu2))
        ssim = ((2 * mu1 * mu2 + c1) * (2 * sigma12 + c2)) / ((mu1 ** 2 + mu2 ** 2 + c1) * (sigma1_sq + sigma2_sq + c2))

    return ssim


def numeric_psnr_ssim(original, noisy):
    psnr_value = calculate_psnr(original, noisy)
    print(f'PSNR: {psnr_value} dB')

    # Calculate SSIM
    ssim_value = calculate_ssim(original, noisy)
    print(f'SSIM: {ssim_value}')

    # Display images (sem mapa SSIM, apenas PSNR e SSIM)
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(original, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Modified Image')
    plt.imshow(noisy, cmap='gray')
    plt.axis('off')

    plt.show()


def get_calculation_psnr_ssim(original, noisy):
    # original = gray_scale(original)
    # noisy = gray_scale(noisy)

    # Calculate PSNR
    psnr_value = calculate_psnr(original, noisy)
    print(f'PSNR: {psnr_value} dB')

    # Calculate SSIM
    ssim_value, ssim_map = ssim(original, noisy, full=True, multichannel=True)
    print(f'SSIM: {ssim_value}')

    # Display images and SSIM map
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.title('Original Image')
    plt.imshow(original, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title('Modified Image')
    plt.imshow(noisy, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title('SSIM Map')
    plt.imshow(ssim_map, cmap='gray')
    plt.axis('off')

    plt.show()


def ssim_diff_images(before, after):
    # Convert images to grayscale
    # before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    # after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    (score, diff) = structural_similarity(before, after, full=True)
    print("Image similarity", score)

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1]
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(before.shape, dtype='uint8')
    filled_after = after.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(before, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(after, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
            cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

    cv2.imshow('before', before)
    cv2.imshow('after', after)
    cv2.imshow('diff', diff)
    cv2.imshow('mask', mask)
    cv2.imshow('filled after', filled_after)
    cv2.waitKey(0)
