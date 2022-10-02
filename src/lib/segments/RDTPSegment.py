import lib.segments.headers.RDTPHeader as h
from lib.segments.headers.RDTPHeader import RDTPHeader

class RDTPSegment:
    def __init__(self, data, header):
        self.header: h.RDTPHeader = header
        self.data: bytearray = data

    def as_bytes(self):
        header_bytes = self.header.as_bytes()
        return header_bytes + self.data

    def get_header(self) -> h.RDTPHeader:
        return self.header

    def get_data(self):
        return self.data


    @staticmethod
    def from_bytes(bytes):
        header_size = RDTPHeader.size()
        header_bytes = bytes[:header_size]
        rdtp_header = h.from_bytes(header_bytes)

        data = bytes[header_size:]

        return RDTPSegment(data, rdtp_header)
