#!/usr/bin/python3

import unittest

from PIL import Image
import process_image, expected_results, math

def compareImageList(self, expected, actual):
    """
        Compares the provided lists on specific key:value pairs
        level_count, num_of_tiles_across, num_of_tiles_down
    """
    for imgObj1,imgObj2 in zip(expected,actual):
        self.assertEqual(imgObj1["level_count"], imgObj2["level_count"])
        self.assertEqual(imgObj1["num_of_tiles_across"], imgObj2["num_of_tiles_across"])
        self.assertEqual(imgObj1["num_of_tiles_down"], imgObj2["num_of_tiles_down"])

class TestProcessImage(unittest.TestCase):
    def test_threshold(self):
        """
            Testing that the Threshold which is used to determine if
            there are enough pixels left in the last tile is enough to
            process or not
        """
        mocked_width = 257
        mocked_height = 256

        default_tile_size = 256

        result_x = process_image.get_num_of_tiles(mocked_width, default_tile_size)
        result_y = process_image.get_num_of_tiles(mocked_height, default_tile_size)

        expected_result_x = math.floor(mocked_width/default_tile_size)
        expected_result_y = math.ceil(mocked_height/default_tile_size)

        self.assertEqual(expected_result_x, result_x)
        self.assertEqual(expected_result_y, result_y)

    def test_levels_and_num_of_tiles_are_correct(self):
        """
            Testing whether the returned levels and number of tiles are as expected
            for a image sizes: 256x256, 1024x1024, 1025x766
        """
        # testing 256x256 image base case first
        im = Image.new('RGB', (256, 256), color = 'red')
        actual_result = process_image.get_image_obj_list(9, im, 256, 256, '')

        self.assertEqual(len(expected_results.expected_256x256_result), len(actual_result))
        compareImageList(self, expected_results.expected_256x256_result, actual_result)

        # testing 1024x1024 image more complex
        im = Image.new('RGB', (1024, 1024), color = 'red')
        actual_result = process_image.get_image_obj_list(11, im, 1024, 1024, '')

        self.assertEqual(len(expected_results.expected_1024x1024_result), len(actual_result))
        compareImageList(self, expected_results.expected_1024x1024_result, actual_result)

        # testing 1025x766 image odd sized
        im = Image.new('RGB', (1025, 766), color = 'red')
        actual_result = process_image.get_image_obj_list(11, im, 1025, 766, '')

        self.assertEqual(len(expected_results.expected_1025x766_result), len(actual_result))
        compareImageList(self, expected_results.expected_1025x766_result, actual_result)


if __name__ == '__main__':
    unittest.main()
