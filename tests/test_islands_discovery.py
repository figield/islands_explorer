import os
import unittest
from unittest import skip

from arbitrary.islands_discovery_with_graph import Graph
from utils.explorer import Explorer
from utils.input_data_parser import read_matrix_from_file
from utils.streams import stream_data_from_file, stream_data_from_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "test_data")


class CommonTestsForIslandsDiscovery:

    def __init__(self, *args, **kwargs):
        super(CommonTestsForIslandsDiscovery, self).__init__(*args, **kwargs)
        if self.__class__ == CommonTestsForIslandsDiscovery:
            self.run = lambda self, *args, **kwargs: None

    def _test_island_explorer(self, test_data_file, expected_result):
        pass

    def test_typical_case_random_map(self):
        """
         Testing typical case for a random map
        """
        self._test_island_explorer(f'{DATA_PATH}/map.txt',
                                   expected_result=4)
        self._test_island_explorer(f'{DATA_PATH}/map4.txt',
                                   expected_result=15)
        self._test_island_explorer(f'{DATA_PATH}/map5.txt',
                                   expected_result=5)
        self._test_island_explorer(f'{DATA_PATH}/map6.txt',
                                   expected_result=5)
        self._test_island_explorer(f'{DATA_PATH}/map13.txt',
                                   expected_result=5)
        self._test_island_explorer(f'{DATA_PATH}/map15.txt',
                                   expected_result=2)

    def test_empty_map(self):
        """
         Testing map without islands or water
        """
        self._test_island_explorer(f'{DATA_PATH}/map0.txt',
                                   expected_result=0)

    def test_water_only_map(self):
        """
         Testing map without islands
        """
        self._test_island_explorer(f'{DATA_PATH}/map8.txt',
                                   expected_result=0)

    def test_milion_islands_sauce(self):
        """
         Testing very large map
        """
        self._test_island_explorer(f'{DATA_PATH}/map_milion.txt',
                                   expected_result=516096)

    def test_map_with_one_island(self):
        """
         Testing different maps with one island only
        """
        for file_postfix in [1, 2, 3, 10, 11]:
            self._test_island_explorer(f'{DATA_PATH}/map{file_postfix}.txt',
                                       expected_result=1)

    def test_map_with_one_big_island_covering_whole_map(self):
        """
         Testing different maps with one big island covering the whole map
        """
        for file_postfix in [12, 14]:
            self._test_island_explorer(f'{DATA_PATH}/map{file_postfix}.txt',
                                       expected_result=1)

    def test_column_islands(self):
        """
         Testing nap with column shaped islands
        """
        self._test_island_explorer(f'{DATA_PATH}/map7.txt', expected_result=8)

    def test_row_islands(self):
        """
         Testing nap with row shaped islands
        """
        self._test_island_explorer(f'{DATA_PATH}/map9.txt', expected_result=5)


class TestIslandsDiscoveryFromFile(unittest.TestCase,
                                   CommonTestsForIslandsDiscovery):

    def _test_island_explorer(self, test_data_file, expected_result):
        explorer = Explorer(test_data_file, stream_data_from_file)
        actual_result = explorer.count_islands()
        self.assertEqual(expected_result, actual_result,
                         f"Expected to discover {expected_result} islands,"
                         f" file: {test_data_file}")


class TestIslandsDiscoveryFromMatrix(unittest.TestCase,
                                     CommonTestsForIslandsDiscovery):

    def _test_island_explorer(self, test_data_file, expected_result):
        explorer = Explorer(test_data_file, stream_data_from_matrix)
        actual_result = explorer.count_islands()
        self.assertEqual(expected_result, actual_result,
                         f"Expected to discover {expected_result} islands,"
                         f" file: {test_data_file}")


class TestIslandsDiscoveryByArbitrarySolution(unittest.TestCase,
                                              CommonTestsForIslandsDiscovery):
    """
     This test scenario serves as a validation of the test data
     and the tests themselves.
    """

    def _test_island_explorer(self, test_data_file, expected_result):
        array2d = read_matrix_from_file(test_data_file)
        if not array2d:
            array2d = [[]]
        graph = Graph(len(array2d), len(array2d[0]), array2d)
        actual_result = graph.countIslands()
        self.assertEqual(expected_result, actual_result,
                         f"Expected to discover {expected_result} islands,"
                         f" file: {test_data_file}")

    @skip
    def test_map_with_one_big_island_covering_whole_map(self):
        """
         Arbitrary solution base on Graph (by Shivam Shrey)
         cannot handle matrix filled with e.x one island of size 25x40, 10x120
         or bigger. Test is failing for maps no. 12 and 14.

         Error:
          `RecursionError: maximum recursion depth exceeded in comparison.`
        """
        pass
