import os
import warnings
from modules.nmaps_processor import is_supported_texture
from modules.nmaps_processor import SUPPORTED_FORMATS






def is_folder_mode(textures_folder):
    """Checks if program will work in the 'folder mode' """
    return textures_folder is not None


def single_texture_check(texture):
    """Checks for single texture file"""
    if not os.path.exists(texture):
        raise FileNotFoundError(f"File {texture} was not found!")
    if not os.path.isfile(texture):
        raise AttributeError(f"Expected file! Got something else!")
    if not is_supported_texture(texture):
        raise AttributeError(f"Texture format of {texture} is not supported!")


def double_input_check(x_normal, y_normal):
    """Checks input file when works only with one texture pair"""
    single_texture_check(x_normal)
    single_texture_check(y_normal)


def texture_folders_check(textures_folder):
    """Checks if input folder is valid" for processing"""

    # Existance check
    if not os.path.exists(textures_folder):
        raise FileNotFoundError(f" Error! Path {textures_folder} was not found!")

    # Is Directory check
    if not os.path.isdir(textures_folder):
        raise IsADirectoryError(f"{textures_folder} is not a directory!")

    # Checks related to amount of files in the folder
    files_amount = len(os.listdir(textures_folder))
    if not files_amount:
        raise FileExistsError(f"Folder {textures_folder} is empty")

    texture_files_counter = 0
    for i in os.listdir(textures_folder):
        for j in SUPPORTED_FORMATS:
            if j in i:
                texture_files_counter += 1
                break

    if not texture_files_counter:
        raise FileNotFoundError(f"There aren't any texture file in the folder {textures_folder}")

    if texture_files_counter == 1:
        raise FileNotFoundError(
            f"Only one texture file was found in the folder {textures_folder}! As minimum 2 are required for processing!")

    if texture_files_counter % 2 != 0:
        warnings.warn(f"Folder {textures_folder} contains odd number of files, so not every texture will be processed!")


def postfix_len_check(postfix):
    """Checks if postfixes length is ok"""
    if not len(postfix):
        raise AttributeError("Got invalid postfix! Length must be greated, than 0!")


def postfix_checks(xpostfix, ypostfix):
    """Checks input postfix"""
    postfix_len_check(xpostfix)
    postfix_len_check(ypostfix)


def get_texture_pairs(texture_folder, x_postftix, y_postfix):
    """Returns dictionary of pairs: Normal X - Normal Y """
    x_normals = []
    y_normals = []
    pairs = {}
    for i in os.listdir(texture_folder):
        if is_supported_texture(i):
            if x_postftix in i:
                x_normals.append(i)
            elif y_postfix in i:
                y_normals.append(i)
    if (not len(x_normals)) and (not len(y_normals)):
        raise ValueError("Unable to find pairs NormalX - NormalY! Check postfix(es)!")

    for i in range(len(x_normals)):
        current_x = os.path.splitext(x_normals[i])[0]
        current_x = current_x[:len(current_x) - len(x_postftix)]
        for j in range(len(y_normals)):
            current_y = os.path.splitext(x_normals[j])[0]
            current_y = current_y[:len(current_y) - len(y_postfix)]
            if current_x == current_y:
                pairs[texture_folder + '\\' + x_normals[i]] = texture_folder + '\\' + y_normals[j]

    if len(pairs) == 0:
        raise ValueError("Unable to find pairs NormalX - NormalY! Check postfix(es)!")
    return pairs
