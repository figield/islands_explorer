def read_matrix_from_file(file_name):
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


def stream_data_from_file(file_name: str):
    """
    Stream data from file_path, character by character.
    :param file_name:
    :return:
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

    :param file_name:
    :return:
    """
    array2d = read_matrix_from_file(file_name)
    for row in array2d:
        for data in row:
            yield data
        yield "\n"