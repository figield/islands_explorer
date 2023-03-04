import sys

from arbitrary.islands_discovery_with_graph import Graph
from utils.input_data_parser import get_input_arguments, read_matrix_from_file

# This solution is used as an arbitrary solution to see if mine gives the same result.

def main():
    from timeit import default_timer as timer

    file_path, _, DEBUG = get_input_arguments()

    array2d = read_matrix_from_file(file_path)
    row = len(array2d)
    col = len(array2d[0])

    g = Graph(row, col, array2d)

    start = timer()
    result = g.countIslands()
    end = timer()

    if DEBUG:
        elapsed = end - start
        sys.stderr.write(f"Finished in {elapsed} seconds, method: DFS, file: {file_path}\n")
    sys.stdout.write(str(result))


if __name__ == "__main__":
    main()
