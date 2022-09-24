import lib.headers.rdtp_header as rdtp_h


class RDTPSegment:
    def __init__(self, data, header):
        self.header: rdtp_h.RDTPHeader = header
        self.data: bytearray = data

    def as_bytes(self):
        header_bytes = self.header.as_bytes()
        return header_bytes + self.data

def from_bytes(bytes):
    header_size = rdtp_h.size() 
    header = bytes[:header_size]
    data = bytes[header_size:]

    return RDTPSegment(data, header)
