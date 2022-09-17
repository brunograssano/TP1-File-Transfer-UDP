import logging

class FileManagerError(Exception):
    pass

class FileManager:

    def __init__(self, file_name: str, mode: str, read_size: int):
        """Creates a file manager
        Params:
        * file_name: The name of the file to open
        * mode: 'r','w'
        * read_size: The read size size in bytes

        Logs in error mode and raises FileNotFoundError if the file could not be opened
        """
        self.file_name = file_name
        self.mode = mode
        self.read_size = read_size
        try:
            self.file = open(file_name,mode)
            logging.debug("Opened file with name: " + file_name)
        except Exception:
            logging.error("Error opening file with name: " + file_name)
            raise FileNotFoundError("Error opening file")

    def close(self):
        """Closes the file, must be called to free resources and to make sure the last bytes were written to the disk"""
        self.file.close()
        logging.debug("Closed file with name: " + self.file_name)

    def read(self):
        """
        Returns at most read_size bytes from the file. 
        If EOF has been reached returns an empty string ('')

        Logs and raises FileManagerError if there is an error
        """
        try:
            data = self.file.read(self.read_size)
            logging.debug("Wrote to file with name: " + self.file_name)
            return data
        except Exception:
            logging.error("Error reading from file with name: " + self.file_name)
            raise FileManagerError("Error reading from file")

    def write(self, data):
        """
        * data: Data to be written

        Logs and raises FileManagerError if there is an error
        """
        try:
            self.file.write(data)
            logging.debug("Wrote to file with name: " + self.file_name)
        except Exception:
            logging.error("Error writing to file with name: " + self.file_name)
            raise FileManagerError("Error writing to file")