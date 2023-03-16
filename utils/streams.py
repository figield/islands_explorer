from abc import ABC, abstractmethod

from typing import List


class LandDataStreamer(ABC):

    @staticmethod
    @abstractmethod
    def is_land(data:any) -> bool:
        return False

    @abstractmethod
    def stream_data(self):
        yield None


class LandDataStreamerFromFile(LandDataStreamer):

    def __init__(self, file_path):
        self.file_path: str = file_path

    @staticmethod
    def is_land(data: str) -> bool:
        return data == "1"

    def stream_data(self):
        """
         Stream data from file_path, character by character.
        """
        with open(self.file_path, 'r') as file:
            while True:
                # Get one by one since the file might be very big.
                data = file.read(1)
                if not data:
                    break
                yield data if data != '\n' else None


class LandDataStreamerFromMatrix(LandDataStreamer):

    def __init__(self, file_path):
        self.file_path: str = file_path

    @staticmethod
    def is_land(data: int) -> bool:
        return data == 1

    def stream_data(self):
        """
         Load data from the file to the matrix and then stream it, item by iteam.
        """
        array2d = self.read_matrix_from_file()
        for row in array2d:
            for data in row:
                yield data
            yield None

    def read_matrix_from_file(self) -> List[List[int]]:
        matrix2d = []
        with open(self.file_path, 'r') as file:
            for line in file.readlines():
                row = []
                for data in line:
                    if data == "\n":
                        break
                    row.append(int(data))
                if row:
                    matrix2d.append(row)
        return matrix2d
