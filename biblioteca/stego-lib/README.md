# 🕵️ Stego-lib

A library for image processing and stegoanalysis. 

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## :dart: Projeto da Cadeira de Processamento Digital de Imagem 2024.1

## Installation

```bash
pip install stego-lib
```

## Example
```python
from stego_lib import load_single_image, display_single_image, plot_single_histogram, compare_images, compare_histograms, load_images, display_sample_images

# Load a single image
image = load_single_image('path/to/image.png')

# Display a single image
display_single_image(image)

# Plot histogram of a single image
plot_single_histogram(image)

# Compare multiple images
compare_images([image1, image2], titles=['Image 1', 'Image 2'])

# Compare histograms of multiple images
compare_histograms([image1, image2], titles=['Image 1', 'Image 2'])

# Load multiple images from a directory
images = load_images('path/to/directory')

# Display sample images
display_sample_images(images, n=2)
```

Original scripts developed for the project:
- [LSB](https://github.com/LucasHenrique-dev/esteganografia-PDI/tree/main/LSB)
- [DCT](DCT)
- [FFT](FFT)
- [SSB](https://github.com/LucasHenrique-dev/esteganografia-PDI/tree/main/SSB)

## 📝 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
