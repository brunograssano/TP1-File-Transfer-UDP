import ctypes
import struct

INITIAL_MESSAGE_FORMAT_STRING = "!?Is"


class InitialMessage():

    def __init__(upload, file_size : int, filename : str = ''):
        self.upload : ctypes.c_bool = upload
        self.file_size : ctypes.c_uint32 = file_size
        self.filename = filename

    def as_bytes(self):
        """Encodes the initial message in Big Endian"""
        return struct.pack(INITIAL_MESSAGE_FORMAT_STRING, self.upload, self.file_size, self.filename)

    def is_upload(self):
        return self.upload

    @staticmethod
    def from_bytes(bytes):
        """Decodes the bytes into an initial message in Big Endian"""
        data = struct.unpack(INITIAL_MESSAGE_FORMAT_STRING, bytes)
        return InitialMessage(data[0], data[1], data[2])
