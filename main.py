import sys

from utils.explorer import Explorer
from utils.input_data_parser import get_input_arguments
from utils.streams import LandDataStreamerFromFile, LandDataStreamerFromMatrix


def main():
    from timeit import default_timer as timer

    file_path, method, DEBUG = get_input_arguments()

    start = timer()
    if method == "stream":
        data_streamer = LandDataStreamerFromFile(file_path)
        explorer = Explorer(data_streamer)
        result = explorer.count_islands()
    else:
        data_streamer = LandDataStreamerFromMatrix(file_path)
        explorer = Explorer(data_streamer)
        result = explorer.count_islands()
    end = timer()

    if DEBUG:
        elapsed = end - start
        sys.stderr.write(f"Finished in {elapsed} seconds,"
                         f" method: {method}, file: {file_path}\n")
    sys.stdout.write(str(result))


if __name__ == "__main__":
    main()
