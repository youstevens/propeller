#!/usr/bin/python3

import argparse
import os
import sys
import math
from PIL import Image
from multiprocessing import Process

# default tile sizes
default_tile_size_x = 256
default_tile_size_y = 256

# default output directory
build_dir = "./output"

# used to determine if there are enough left over
# pixels in the last tile to be viable for processing
threshold = 20


def write_file(output_filepath, im, begin, end):
    """
        Crop the given image based on the coordinates provided
        and saves it against the provided output path
    """

    # setting the output_filename to the coordinates you are generating
    output_filename = str(begin[0]) + "_" + str(begin[1]) + ".jpg"
    output_file = os.path.join(output_filepath, output_filename)

    # creating cropping area
    box = (begin[0], begin[1], end[0], end[1])
    region = im.crop(box)

    output_im = Image.new(im.mode, (default_tile_size_x, default_tile_size_y))
    # hardcoding the position where we want to paste the cropped image in memory
    # to cos we always want the cropped image to be pasted from position (0,0) - top left corner
    output_im.paste(region, (0, 0))
    # output tile
    output_im.save(output_file, "JPEG")


def process_img(im, level_count, num_of_tiles_across, num_of_tiles_down, output_dir):
    """
        Processes the provided image based on the number of calculated across and down tiles
        passed in
    """
    tile_count_x = 0
    tile_count_y = 0

    tile_point_x_begin = 0
    tile_point_y_begin = 0

    tile_point_x_end = tile_point_x_begin + default_tile_size_x
    tile_point_y_end = tile_point_y_begin + default_tile_size_y

    # loop down
    while tile_count_y < num_of_tiles_down:
        # loop across
        while tile_count_x < num_of_tiles_across:
            print(".", end="")

            output_filepath = os.path.join(output_dir, str(level_count))
            if not os.path.exists(output_filepath):
                # creating the level folder e.g. 0
                os.makedirs(output_filepath)

            # write the level file
            write_file(output_filepath, im, (tile_point_x_begin,
                                             tile_point_y_begin), (tile_point_x_end, tile_point_y_end))

            tile_point_x_begin += default_tile_size_x
            tile_point_x_end += default_tile_size_x

            tile_count_x += 1

        tile_point_y_begin += default_tile_size_y
        tile_point_y_end += default_tile_size_y

        # restart from the beginning of the row
        tile_count_x = 0
        tile_point_x_begin = 0
        tile_point_x_end = tile_point_x_begin + default_tile_size_x

        tile_count_y += 1


def get_num_of_tiles(measurement, default_size):
    remainder = measurement % default_size
    _res = 0
    if remainder < threshold:
        _res = math.floor(measurement/default_size)
    else:
        _res = math.ceil(measurement/default_size)

    # When there are not enough tiles across or down, we want to take
    # a crop of the full image
    if _res == 0:
        _res = 1

    return _res


def get_image_obj_list(total_levels, im, width, height, output_dir):
    """
        loop through the number of total levels and grab all required info
        to prepare for processing later
    """
    level_count = 0
    imageObjList = []
    while level_count < total_levels:
        print(f"Size of Image: {width} x {height}, level {level_count}")

        num_of_tiles_across = get_num_of_tiles(width, default_tile_size_x)
        num_of_tiles_down = get_num_of_tiles(height, default_tile_size_y)

        imageObjList.append({
            "im": im,
            "level_count": level_count,
            "num_of_tiles_across": num_of_tiles_across,
            "num_of_tiles_down": num_of_tiles_down,
            "output_dir": output_dir
        })

        # half the image size
        (width, height) = (math.ceil(im.width / 2), math.ceil(im.height / 2))

        # check to make sure that either the height or width is not zero before resizing
        if height == 0 or width == 0:
            break
        im = im.resize((width, height))

        level_count += 1
    return imageObjList


def process_image_file(input_file, output_dir):
    try:
        with Image.open(input_file) as im:

            # separating the width and height from returned image size
            width, height = im.size

            # calculating the total number of levels we will need
            total_levels = math.floor(1 + math.log2(max(width, height)))
            print("Total number of levels: ", total_levels)

            # loop through first and grab all the necessary info before processing
            imageObjList = get_image_obj_list(
                total_levels, im, width, height, output_dir)

            # loop through to fork/spawn new processes to handle creating the tiles
            for imageObj in imageObjList:
                # process the provided image against the current level
                Process(target=process_img, args=(
                    imageObj["im"], imageObj["level_count"], imageObj["num_of_tiles_across"], imageObj["num_of_tiles_down"], imageObj["output_dir"])).start()

    except IOError:
        print("Was unable to open: ", input_file, sys.exc_info())
    except OSError:
        print("Was unable to create directory: ", output_dir, sys.exc_info())
    except:
        print("Unexpected error:", sys.exc_info())


def main():
    """
        Main function which accepts one commandline argument
    """
    parser = argparse.ArgumentParser(
        description='Process provided image into tiles')
    parser.add_argument('inputFile', action="store",
                        help='path and filename you wish to process')

    args = parser.parse_args()

    # Get filename to process
    input_file = args.inputFile

    output_folder_name = os.path.split(input_file)
    output_folder_name = output_folder_name[len(output_folder_name)-1]

    _folder_name, _extension = os.path.splitext(output_folder_name)

    # Decide where to store the outputted files in
    output_dir = os.path.join(build_dir, _folder_name)

    # Start processing the file
    process_image_file(input_file, output_dir)


if __name__ == "__main__":
    main()
