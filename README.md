# AEStego

## Overview
AEStego is a steganography tool that uses Pixel Value Differencing (PVD) to hide secret messages within an image by modifying pixel values while maintaining image quality. This project implements PVD steganography using Python with a graphical user interface (GUI) built using Tkinter.

## Features
- **Hide Secret Data:** Encode a secret message inside an image.
- **Extract Secret Data:** Retrieve hidden messages from an image.
- **GUI Interface:** Easy-to-use graphical interface for embedding and extracting data.
- **Supports RGB Images:** Works on PNG, JPG, and BMP image formats.

## Requirements
Ensure you have the following dependencies installed:
```sh
pip install opencv-python numpy tkinter
```

## Usage

### Running the Application
To launch AEStego, run:
```sh
python aesstego.py
```

### Hiding Data
1. Click on **"Hide Data"**.
2. Select an image file (PNG, JPG, BMP).
3. Enter the secret text to be embedded.
4. Choose a location to save the new stego-image.
5. A success message will confirm the data has been hidden.

### Extracting Data
1. Click on **"Extract Data"**.
2. Select a stego-image with hidden text.
3. The extracted message will be displayed in a pop-up.

## How It Works
- The difference between pixel pairs is used to determine how many bits can be embedded.
- The secret message is converted into binary and distributed among pixel pairs.
- The receiver extracts the differences to reconstruct the original message.

## Limitations
- Works only with grayscale or RGB images.
- No encryption, so data security depends on obscurity.
- Limited message capacity based on image size.

## License
This project is open-source and available under the MIT License.

