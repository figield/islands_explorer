# Islands Explorer

## Solution description



## Memory profiling

Starting the program in the standard configuration allows for the analysis of very large maps.
I used the `mprof` tool to generate the presented graphs.

```commandline
 mprof run python3 main.py tests/test_data/map_milion.txt
 mprof plot
```

I tested the algorithm on a dataset with over a million rows and nine columns (1030144 x 9).
I ran tests for the following scenarios.

1. Reading map data from a file, character by character, and calculating the result on the fly.

![Mprof for milion stream data from file](profiling/mprof_for_milion_stream_from_file.png)

2. Loading the whole map into memory and analyze it character by character using the same algorithm as in the first scenario.

![Mprof for milion stream data from array](profiling/mprof_for_milion_stream_from_array.png)

3. I also ran the above scenarios without optimizing the algorithm's memory.
More precisely, without removing unnecessary elements for further processing of data from the map.

- Streaming data direcly from the file.

![Mprof for milion stream data from file no optimalization](profiling/mprof_for_milion_stream_from_file_no_optimalization.png)

- Streaming of data from a previously loaded two-dimensional matrix.

![Mprof for milion stream data from matrix no optimalization](profiling/mprof_for_milion_stream_from_array_no_optimalization.png)


4. I also compared my solution with the graph based solution (taken from: https://www.geeksforgeeks.org/find-the-number-of-islands-using-dfs/)
     This algorithm is used as an arbitrary solution to see if mine produces the same result for a common set of tests.

![Mprof for milion from_graph](profiling/mprof_for_milion_from_graph.png)


## Summary

I spent about 4 hours coming up with this algorithm.
It took me much longer to write tests (TDD of course!), refactor the code and play around with memory profiling.
I'm being a bit too scientific in my approach, but I hope you like my solution.

And the results are quite surprising.

1. The algorithm I implemented runs comparably fast as graph-based solutions, and uses much less memory.
I achived this by processing data in the fly, when streaming it from the file.
Graph based algorithms need to have the whole map loaded into the memory, which is a disadvantage where it comes to handling huge data or specific ones (like `one big island`).

2. The recursion-based algorithm fails when encountering cases leading to a "RecursionError".

For example, a graph-based solution cannot cope with a filled matrix, i.e. with one large 25x40 or 10x120 island.
(Unit tests fail for maps no. 12 and 14)

```code
           Error: `RecursionError: maximum recursion depth exceeded in comparison.`
```

3. At the last one, but not least. I have refactored the code to be more object oriented.
That has caused small drop in efficiency, but the code is easy to read and understood.


### What's left for improvement

I cover the logic with tests based on different maps and a reference solution for a common set of tests.
More unit tests would be good to add.
I was working in my virtual environment and the script has no external dependencies.
Only Python 3 is needed to run it.

- [x] invent an algorithm
- [x] add tests
- [x] add script `./run.sh <path_to_the_file>`
- [x] add arbitrary solution
- [x] profiling
- [x] check coverage
- [x] refactoring
- [ ] descriptions
- [ ] more tests
- [ ] docker file
