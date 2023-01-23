import os
import numpy as np
import colortrans
from blend_modes import addition
from PIL import Image, ImageOps
from PIL.Image import Palette

NORMAL_X = ''
NORMAL_Y = ''
RED_REFERENCE = 'references/red_model.png'
SUPPORTED_FORMATS = [".png", ".bmp", ".tga", ".jpg", ".jpeg"]


def is_supported_texture(texture_name):
    for i in SUPPORTED_FORMATS:
        if texture_name.lower().endswith(i):
            return True
    return False


def check_image(texture_name):
    """Checks if input file is an image. If it's not one, throws an exception. Requres file path as an input argument"""
    if not os.path.exists(texture_name):
        raise FileNotFoundError(f"File {texture_name} was not found!")
    if not is_supported_texture(texture_name):
        raise ValueError(f"{texture_name} is not a graphics file!")


def get_alpha_channel(texture_image):
    """Returns only Alpha Channel of the Texture"""
    image = Image.open(texture_image).convert('RGBA')
    alpha_channel_image = image.getchannel('A')  # Mode 'L'
    alpha_channel_image.convert('L', palette=Palette.ADAPTIVE)
    alpha_channel_image = ImageOps.invert(alpha_channel_image)
    return alpha_channel_image


def prepare_input_images(normal_x_file, normal_y_file):
    """Prepares input images for subsequent  work: checks files existence, converts textures to png format"""
    global NORMAL_X
    global NORMAL_Y
    check_image(normal_x_file)
    check_image(normal_y_file)
    NORMAL_X = normal_x_file
    NORMAL_Y = normal_y_file


def process_red(image):
    """Changes texture color palette from gray to red"""
    content = np.array(image.convert('RGB'))
    reference = np.array(Image.open(RED_REFERENCE).convert('RGB'))
    return Image.fromarray(colortrans.transfer_reinhard(content, reference))


def process_green(image):
    """Changes texture color palette from gray to green"""
    red_variation = process_red(image)
    R, G, B = red_variation.split()
    result = Image.merge('RGB', [G, R, B])
    return result


def generate_mikk(red_image, green_image, output_file_name="result.png"):
    """Blends R and G teures in format 'Screen' and inverts"""
    bg = np.array(red_image.convert("RGBA")).astype(float)
    foreground = np.array(green_image.convert("RGBA")).astype(float)
    blended_float = addition(foreground, bg, 1.0)
    blended_img = np.uint8(blended_float)
    blended_img_raw = Image.fromarray(blended_img).convert('RGB')
    r, g, b = blended_img_raw.split()
    result = ImageOps.invert(Image.merge('RGB', (g, r, b)))
    result.save(output_file_name)


def generate_normal_map_mikk(normal_x_file, normal_y_file, output_file_name="result.png"):
    """Generates one Mikk format normal map by 2 files: X and Y normals"""
    prepare_input_images(normal_x_file, normal_y_file)
    x_merged = get_alpha_channel(NORMAL_X)
    y_merged = get_alpha_channel(NORMAL_Y)
    red_option = process_red(y_merged)
    green_option = process_green(x_merged)
    generate_mikk(red_option, green_option, output_file_name)
