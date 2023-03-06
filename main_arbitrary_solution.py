import sys

from arbitrary.islands_discovery_with_graph import Graph
from utils.input_data_parser import get_input_arguments, read_matrix_from_file


# This solution is used as an arbitrary solution.
# source: https://www.geeksforgeeks.org/find-the-number-of-islands-using-dfs/

def main():
    from timeit import default_timer as timer

    file_path, _, DEBUG = get_input_arguments()

    start = timer()
    array2d = read_matrix_from_file(file_path)
    row = len(array2d)
    col = len(array2d[0])
    g = Graph(row, col, array2d)
    result = g.countIslands()
    end = timer()

    if DEBUG:
        elapsed = end - start
        sys.stderr.write(f"Finished in {elapsed} seconds,"
                         f" method: DFS, file: {file_path}\n")
    sys.stdout.write(str(result))


if __name__ == "__main__":
    main()
