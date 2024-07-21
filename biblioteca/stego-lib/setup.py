from setuptools import setup, find_packages

setup(
    name="stego-lib",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "Pillow",
        "matplotlib",
        "seaborn",
    ],
    author="Jose Quel, Felipe Romero, Lucas Henrique, Nathalia Ellen",
    author_email="jalq@ecomp.poli.br",
    description="A library for image processing and steganalysis",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
