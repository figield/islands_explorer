import sys

from utils.lands import connect_neighbours, discover_land, forget_the_land_beyond_the_horizon, is_land
from utils.streams import stream_data_from_array2d, stream_data_from_file

DEBUG = False


def main(file_name: str, data_streamer=stream_data_from_file) -> int:
    """

    :param data_streamer:
    :param file_name:
    :return:
    """
    positions = {}
    lands = {}
    row_len = 0
    forgotten_lands = 0
    row = 0
    row_to_clean = 0
    column = 0
    for position in data_streamer(file_name):
        if position == "\n":
            row_len = column
            row += 1
            column = 0
            continue

        if is_land(position):
            discover_land(row, column, positions, lands)
            connect_neighbours(row, column, positions, lands)

        # for memory optimalization
        if row_to_clean + 2 == row:
            forgotten_lands += forget_the_land_beyond_the_horizon(row_len, row, column, positions, lands)
            row_to_clean += 1

        column += 1

    if DEBUG:
        sys.stderr.write(f"{positions}\n")
        sys.stderr.write(f"{lands}\n")
    return len(lands) + forgotten_lands


if __name__ == "__main__":
    from timeit import default_timer as timer

    file_path = "tests/test_data/map.txt"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    method = "stream"
    DEBUG = False
    if len(sys.argv) > 2:
        if "stream" in sys.argv:
            method = "stream"
        elif "matrix" in sys.argv:
            method = "matrix"
        if "--debug" in sys.argv:
            DEBUG = True

    start = timer()
    if method == "stream":
        reuslt = main(file_path)
    else:
        reuslt = main(file_path, stream_data_from_array2d)
    end = timer()
    elapsed = end - start
    if DEBUG:
        sys.stderr.write(f"Finished in {elapsed} seconds, method: {method}, file: {file_path}\n")
    sys.stdout.write(str(reuslt))
