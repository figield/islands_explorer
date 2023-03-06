import sys
from typing import List, Tuple


def get_input_arguments() -> Tuple[int, int, int]:
    if len(sys.argv) < 2:
        sys.stderr.write("Provide path to the file with the map\n")
        exit(1)
    file_path = sys.argv[1]
    method = "stream"
    debug = False
    if len(sys.argv) > 2:
        if "stream" in sys.argv:
            method = "stream"
        elif "matrix" in sys.argv:
            method = "matrix"
        if "--debug" in sys.argv:
            debug = True
    return file_path, method, debug


def read_matrix_from_file(file_name: str) -> List[List[int]]:
    matrix2d = []
    with open(file_name, 'r') as file:
        for line in file.readlines():
            row = []
            for data in line:
                if data == "\n":
                    break
                row.append(int(data))
            if row:
                matrix2d.append(row)
    return matrix2d
