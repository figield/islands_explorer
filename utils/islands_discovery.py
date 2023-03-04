import sys

from utils.lands import connect_neighbours, discover_land, forget_lands_beyond_the_horizon
from utils.streams import stream_data_from_file

DEBUG = False


def islands_discovery(file_path: str, data_streamer=stream_data_from_file) -> int:
    """
    """
    positions = {}
    lands = {}
    row_len = 0
    forgotten_lands = 0
    row = 0
    row_to_clean = 0
    column = 0
    for position in data_streamer(file_path):
        if position == "\n":
            row_len = column
            row += 1
            column = 0
            continue

        if int(position) == 1:
            discover_land(row, column, positions, lands)
            connect_neighbours(row, column, positions, lands)

        # for memory optimalization
        # if row_to_clean + 2 == row:
        #     forgotten_lands += forget_lands_beyond_the_horizon(row_len, row, column, positions, lands)
        #     row_to_clean += 1

        column += 1

    if DEBUG:
        sys.stderr.write(f"{positions}\n")
        sys.stderr.write(f"{lands}\n")
    return len(lands) + forgotten_lands
