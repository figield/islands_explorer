import sys

from utils.explorer import Explorer
from utils.input_data_parser import get_input_arguments
from utils.streams import stream_data_from_file, stream_data_from_matrix


def main():
    from timeit import default_timer as timer

    file_path, method, DEBUG = get_input_arguments()

    start = timer()
    if method == "stream":
        explorer = Explorer(file_path, stream_data_from_file)
        result = explorer.count_islands()
    else:
        explorer = Explorer(file_path, stream_data_from_matrix)
        result = explorer.count_islands()
    end = timer()

    if DEBUG:
        elapsed = end - start
        sys.stderr.write(f"Finished in {elapsed} seconds, method: {method}, file: {file_path}\n")
    sys.stdout.write(str(result))


if __name__ == "__main__":
    main()
