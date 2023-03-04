import sys

from utils.input_data_parser import get_input_arguments
from utils.islands_discovery import islands_discovery
from utils.streams import stream_data_from_array2d


def main():
    from timeit import default_timer as timer

    file_path, method, DEBUG = get_input_arguments()

    start = timer()
    if method == "stream":
        result = islands_discovery(file_path)
    else:
        result = islands_discovery(file_path, stream_data_from_array2d)
    end = timer()

    if DEBUG:
        elapsed = end - start
        sys.stderr.write(f"Finished in {elapsed} seconds, method: {method}, file: {file_path}\n")
    sys.stdout.write(str(result))


if __name__ == "__main__":
    main()
