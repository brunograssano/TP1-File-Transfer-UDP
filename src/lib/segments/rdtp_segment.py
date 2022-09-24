from src.lib.headers import rdtp_header as h

class RDTPSegment:
    def __init__(self, data, header):
        self.header: h.RDTPHeader = header
        self.data: bytearray = data

    def as_bytes(self):
        header_bytes = self.header.as_bytes()
        return header_bytes + self.data

def from_bytes(bytes):
    header_size = h.size() 
    header_bytes = bytes[:header_size]
    rdtp_header = from_bytes(header_bytes)

    data = bytes[header_size:]

    return RDTPSegment(data, rdtp_header)