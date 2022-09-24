import unittest
from headers.RDTPHeader import RDTPHeader, from_bytes

class TestHeader(unittest.TestCase):
    def test_as_binary_string(self):
        header = RDTPHeader(1, 2, 3, True, False)
        self.assertEqual(header.as_bytes(), b'\x00\x00\x00\x01\x00\x00\x00\x02\x00\x03\x01\x00')


    def test_from_binary_string(self):
        bytestring = b'\x00\x00\x00\x01\x00\x00\x00\x02\x00\x03\x01\x00'
        header = from_bytes(bytestring)
        self.assertTrue(isinstance(header, RDTPHeader))


if __name__ == '__main__':
    unittest.main()

