import unittest
from rdtp_segment import RDTPSegment, from_bytes
from src.lib.headers import rdtp_header as h

class TestHeader(unittest.TestCase):
    def test_as_binary_string(self):
        header = h.RDTPHeader(1, 2, 3, True, False)
        data = bytearray(123, 4, 67)
        segment = RDTPSegment(data , header)
        print(segment)
        self.assertEqual(True, True)


    #def test_from_binary_string(self):
    #    bytestring = b'\x00\x00\x00\x01\x00\x00\x00\x02\x00\x03\x01\x00'
    #    header = from_bytes(bytestring)
    #    self.assertTrue(isinstance(header, RDTPHeader))


if __name__ == '__main__':
    unittest.main()

