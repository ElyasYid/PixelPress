from PIL import Image
import imageio

def compress_jpeg(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img.save(output_path, "JPEG", quality=quality)

def compress_png(input_path, output_path, compress_level=9):
    with Image.open(input_path) as img:
        img.save(output_path, "PNG", optimize=True, compress_level=compress_level)

def compress_gif(input_path, output_path, colors=256):
    img = imageio.mimread(input_path)
    imageio.mimsave(output_path, img, format='GIF', palettesize=colors)

def compress_webp(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img.save(output_path, "WEBP", quality=quality)

def compress_bmp(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img.save(output_path, "JPEG", quality=quality)  # Converting to JPEG for compression

def compress_tiff(input_path, output_path, compression="tiff_lzw"):
    with Image.open(input_path) as img:
        img.save(output_path, "TIFF", compression=compression)
