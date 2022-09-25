import unittest
from RDTPSegment import RDTPSegment, from_bytes
from headers import RDTPHeader as h

class TestRDTPSegment(unittest.TestCase):
    def test_as_binary_string(self):
        header = h.RDTPHeader(1, 2, 3, True, False)
        data = bytearray([123, 4, 67])
        segment = RDTPSegment(data , header)
        self.assertEqual(segment.as_bytes(), b'\x00\x00\x00\x01\x00\x00\x00\x02\x00\x03\x01\x00{\x04C')


    def test_from_binary_string(self):
        bytestring = b'\x00\x00\x00\x01\x00\x00\x00\x02\x00\x03\x01\x00{\x04C'
        segment = from_bytes(bytestring)
        self.assertEqual(segment.header.ack_only, True)


if __name__ == '__main__':
    unittest.main()

