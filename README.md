# PixelPress - Image Compression Tool

PixelPress is a simple image compression tool built using Python and Tkinter. It allows users to compress images in various formats such as JPEG, PNG, GIF, WEBP, BMP, and TIFF.

## Features

- **Image Compression:** Compress images in different formats.
- **Quality Adjustment:** Set the quality/compression level (0-100).
- **TIFF Compression Options:** Choose from various compression methods for TIFF images.
- **Threaded Compression:** Image compression is performed in a separate thread to prevent the GUI from freezing.
- **Simple GUI:** Easy-to-use graphical interface built using Tkinter.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- Pillow (for image processing)
- Compression library (specific to the image formats you want to support)

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/ElyasYid/PixelPress.git
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Run the application:

    ```
    python main.py
    ```

## Usage

1. Choose the image format you want to compress to.
2. Set the quality/compression level (0-100).
3. Select the compression method for TIFF images (if applicable).
4. Click the "Compress Image" button and select the input image file.
5. Choose the output file location and click "Save".

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Elias Yidnekachew** - [Github](https://github.com/ElyasYid)
