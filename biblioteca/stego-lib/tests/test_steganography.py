import unittest
import numpy as np
from stego_lib import (message_to_binary, binary_to_message, extract_bit, modify_bits, embed_message_ssbn, 
                              extract_bits, decrypt_message_ssbn, bit_plane_slicing, plot_bit_planes, calculate_psnr)

class TestSteganography(unittest.TestCase):

    def test_message_to_binary(self):
        message = "hello"
        binary_message = message_to_binary(message)
        self.assertEqual(binary_message, '0110100001100101011011000110110001101111')

    def test_binary_to_message(self):
        binary_str = '0110100001100101011011000110110001101111'
        message = binary_to_message(binary_str)
        self.assertEqual(message, "hello")

    def test_extract_bit(self):
        value = 0b10101010
        self.assertEqual(extract_bit(value, 0), 0)
        self.assertEqual(extract_bit(value, 1), 1)

    def test_modify_bits(self):
        value = 0b10101010
        bit_positions = [0, 1]
        bit_values = [1, 0]
        new_value = modify_bits(value, bit_positions, bit_values)
        self.assertEqual(new_value, 0b10101001)

    def test_calculate_psnr(self):
        img1 = np.ones((10, 10), dtype=np.uint8) * 255
        img2 = np.ones((10, 10), dtype=np.uint8) * 254
        psnr_value = calculate_psnr(img1, img2)
        self.assertGreater(psnr_value, 20)

if __name__ == '__main__':
    unittest.main()
