import cv2
import matplotlib.pyplot as plt
import seaborn as sns

def display_single_image(image):
    plt.figure(figsize=(5, 5))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

def plot_single_histogram(image):
    plt.figure(figsize=(15, 5))
    if image.ndim == 2:  # Grayscale image
        sns.histplot(image.ravel(), bins=256, kde=True, color='gray', label='Grayscale')
    else:  # RGB image
        for j, color in enumerate(['r', 'g', 'b']):
            sns.histplot(image[:, :, j].ravel(), bins=256, kde=True, color=color, label=f'Channel {color.upper()}')
    plt.title('Pixel Value Distribution')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

def compare_images(images, titles=[], gray=True):
    num_images = len(images)
    fig, axs = plt.subplots(1, num_images, figsize=(5 * num_images, 5))
    for i in range(num_images):
        if gray:
            axs[i].imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
        else:
            axs[i].imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
        if i < len(titles):
            axs[i].set_title(titles[i])
        axs[i].axis('off')
    plt.show()

def compare_histograms(images, titles=[], gray=True):
    num_images = len(images)
    fig, axs = plt.subplots(1, num_images + 1, figsize=(5 * (num_images + 1), 5))
    for i in range(num_images):
        if images[i].ndim == 2:  # Grayscale image
            sns.histplot(images[i].ravel(), bins=256, kde=True, color='gray', label='Grayscale', ax=axs[i])
        else:  # RGB image
            for j, color in enumerate(['r', 'g', 'b']):
                sns.histplot(images[i][:, :, j].ravel(), bins=256, kde=True, color=color, label=f'Channel {color.upper()}', ax=axs[i])
        if i < len(titles):
            axs[i].set_title(titles[i])
    if num_images == 2:
        hist1, bins1 = np.histogram(images[0], bins=256, range=(0, 256))
        hist2, bins2 = np.histogram(images[1], bins=256, range=(0, 256))
        hist_diff = hist2 - hist1
        bin_centers = (bins1[:-1] + bins1[1:]) / 2
        axs[2].bar(bin_centers, hist_diff, width=(bins1[1] - bins1[0]), color='green')
        axs[2].set_title('Difference in Histograms (Modified - Original)')
        axs[2].set_xlabel('Value')
        axs[2].set_ylabel('Difference in Count')
        axs[2].set_ylim([0, 50])
    plt.show()

def display_sample_images(images, n=1):
    plt.figure(figsize=(5, 5))
    for i in range(n):
        plt.subplot(1, n, i + 1)
        plt.imshow(cv2.cvtColor(images[i][1], cv2.COLOR_BGR2RGB))
        plt.title(images[i][0].split(os.path.sep)[-1])  # Display subfolder name
        plt.axis('off')
    plt.show()

def plot_pixel_histograms(images, num_histograms=10):
    for i in range(min(num_histograms, len(images))):
        _, img = images[i]
        plt.figure(figsize=(15, 5))

        if img.ndim == 2:  # Grayscale image
            sns.histplot(img.ravel(), bins=256, kde=True, color='gray', label='Grayscale')
        else:  # RGB image
            for j, color in enumerate(['r', 'g', 'b']):
                sns.histplot(img[:, :, j].ravel(), bins=256, kde=True, color=color, label=f'Channel {color.upper()}')

        plt.title(f'Pixel Value Distribution for Image {i + 1}')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

