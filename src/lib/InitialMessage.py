import ctypes
import struct

INITIAL_MESSAGE_FORMAT_STRING = "!??Is"


class InitialMessage():

    def __init__(self,upload, is_saw : bool, file_size : int, filename : str = ''):
        self.upload : ctypes.c_bool = upload
        self.is_saw : ctypes.c_bool = is_saw
        self.file_size : ctypes.c_uint32 = file_size
        self.filename = filename

    @staticmethod
    def upload_message(file_size : int, filename : str, is_saw : bool):
        return InitialMessage(True, file_size, filename, is_saw)

    @staticmethod
    def download_message(filename : str, is_saw : bool):
        return InitialMessage(False, 0, filename, is_saw)

    def as_bytes(self):
        """Encodes the initial message in Big Endian"""
        return struct.pack(INITIAL_MESSAGE_FORMAT_STRING, self.upload,self.is_saw, self.file_size, self.filename.encode())

    def is_upload(self):
        return self.upload

    def is_stop_and_wait(self):
        return self.is_saw

    def get_file_size(self):
        return self.file_size

    def get_filename(self):
        return self.filename

    @staticmethod
    def from_bytes(bytes):
        """Decodes the bytes into an initial message in Big Endian"""
        data = struct.unpack(INITIAL_MESSAGE_FORMAT_STRING, bytes)
        return InitialMessage(data[0], data[1], data[2], data[3])
