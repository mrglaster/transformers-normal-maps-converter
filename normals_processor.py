import argparse
from pathlib import Path

from modules.nmaps_processor import *
from modules.args_processing import *


def before_start():
    # Default results output folder
    if not os.path.exists('results'):
        os.mkdir("results")

    # Check if the red reference exists
    if not os.path.exists('references/red_model.png'):
        raise FileNotFoundError("Error! File /references/red_model.png was not found! Without this file processing is "
                                "impossible!")

def main():

    # before we start
    before_start()


    # preparing of arguments parser
    parser = argparse.ArgumentParser(description='Utility generating one Mikk format normal map by 2 files: X  & Y '
                                                 'normals')
    parser.add_argument('-xnormal', '--x_normals_file', type=str, default=None, help='Path to X normals file')
    parser.add_argument('-ynormal', '--y_normals_file', type=str, default=None, help='Path to Y normals file')
    parser.add_argument('-texfolder', '--textures_folder', type=str, default=None,
                        help='Path to folder containing X and Y normals files')
    parser.add_argument('-xnpostfix', '--x_normals_postfix', type=str, default='_Color_NormX',
                        help='Postfix for X normals. It will be used if '
                             'you work with multiple textures in one '
                             'folder')
    parser.add_argument('-ynpostfix', '--y_normals_postfix', type=str, default='_Masks_NormY',
                        help='Postfix for Y normals. It will be used if '
                             'you work with multiple textures in one '
                             'folder')
    parser.add_argument('-ofile', '--output_file', type=str, default="results//result.png", help='Name of the output '
                                                                                                 'file')
    parser.add_argument('-ofolder', '--output_folder', type=str, default="results", help='Name of the folder in '
                                                                                         'which results will be '
                                                                                         'saved')
    # Getting values of arguments
    parser_namespace = parser.parse_args()
    x_normal = parser_namespace.x_normals_file
    y_normal = parser_namespace.y_normals_file
    textures_folder = parser_namespace.textures_folder
    xn_postfix = parser_namespace.x_normals_postfix
    yn_postfix = parser_namespace.y_normals_postfix
    o_file = parser_namespace.output_file
    o_folder = parser_namespace.output_folder

    # If we work with several files on the one folder
    if is_folder_mode(textures_folder):
        texture_folders_check(textures_folder)
        postfix_checks(xn_postfix, yn_postfix)
        if not os.path.exists(o_folder):
            raise ValueError(f"Folder {o_folder} doesn't exist!")
        pairs = get_texture_pairs(textures_folder, xn_postfix, yn_postfix)
        for i in pairs.keys():
            output_filename = Path(i).stem
            output_filename = o_folder + '\\' + output_filename[:-len(xn_postfix)] + "_mikk_nmap.png"
            generate_normal_map_mikk(i, pairs[i], output_filename)
        print("DONE!")
    else:
        # If we work with single normals pair
        double_input_check(x_normal, y_normal)
        if not os.path.exists(os.path.dirname(o_file)) and o_file != "results//result.png" and len(
                os.path.dirname(o_file)) != 0:
            raise IsADirectoryError(f"Unable to write result to directory: {os.path.dirname(o_file)}! Check the path!")
        generate_normal_map_mikk(x_normal, y_normal, o_file)
        print("DONE!")


if __name__ == '__main__':
    main()
