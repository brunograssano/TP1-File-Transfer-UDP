import ctypes
import struct

RDTP_FORMAT_STRING = "!II?"


class RDTPHeader:
    def __init__(self, seq_num, ack_num, fin):
        self.seq_num: ctypes.c_uint32 = seq_num
        self.ack_num: ctypes.c_uint32 = ack_num
        self.fin: bool = fin

    def is_fin(self):
        return self.fin

    def is_ack(self):
        return self.ack_only

    def get_ack(self):
        return self.ack_num

    def get_seq(self):
        return self.seq_num

    def as_bytes(self):
        return struct.pack(
            RDTP_FORMAT_STRING,
            self.seq_num,
            self.ack_num,
            self.fin)

    @staticmethod
    def size():
        return struct.calcsize(RDTP_FORMAT_STRING)

    @staticmethod
    def from_bytes(bytes):
        data = struct.unpack(RDTP_FORMAT_STRING, bytes)
        header = RDTPHeader(data[0], data[1], data[2])
        return header
