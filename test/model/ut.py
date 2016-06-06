import unittest
import csv
import enc_frame


class TestRGBMethods(unittest.TestCase):
    def readBlockCSV(self,name):
        with open(name, 'r') as test_data:
            self.test_data_filename = '24x24.bmp'
            self.csv_handle = csv.reader(test_data)
            self.data = []
            for row in self.csv_handle:
                self.data += list(map(int, row))
            (r, g, b) = enc_frame.readRgbImageBlocks(self.test_data_filename)
            return (r,g,b)

    def test_block_1(self):
        (r,g,b) = self.readBlockCSV('n1_red_block.csv')
        self.assertEqual(r[0], self.data)

    def test_block_2(self):
        (r, g, b) = self.readBlockCSV('n2_blue_block.csv')
        self.assertEqual(b[1], self.data)

    def test_block_3(self):
        (r, g, b) = self.readBlockCSV('n9_green_block.csv')
        self.assertEqual(g[8], self.data)

class TestRLE(unittest.TestCase):
    def test_RLE_0(self):
        self.assertEqual(enc_frame.rle_code([1,1,1,1,2,2,2,3,3,3,3,3,3,1,1,1,1,2,2,2,2]),
                         [1,4,2,3,3,6,1,4,2,4])
    def test_RLE_1(self):
        input  = [ -10, 0, 0, 0, 0, 0, 0, 0, -6, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0]
        output = [-10, 1, 0, 7, -6, 1, 0, 1, 1, 1, 0, 20, 1, 1, 0, 14, 1, 1, 0, 6, -1, 1, 0, 3, -1, 1, 0, 5]
        self.assertEqual(enc_frame.rle_code(input),output)


class TestHuffman(unittest.TestCase):
    def test_Huff_1(self):
        self.assertEqual(0, 1)


if __name__ == '__main__':
    unittest.main()
