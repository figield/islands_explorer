from utils.input_data_parser import read_matrix_from_file


def stream_data_from_file(file_name: str):
    """
    Stream data from file_path, character by character.
    """
    with open(file_name, 'r') as file:
        while True:
            # Get one by one since the file_path might be very big (in both dimensions)
            data = file.read(1)
            if not data:
                break
            yield data


def stream_data_from_array2d(file_name: str):
    """
    Load data from the file_path to the matrix and then stream it, item by iteam.
    """
    array2d = read_matrix_from_file(file_name)
    for row in array2d:
        for data in row:
            yield data
        yield "\n"
