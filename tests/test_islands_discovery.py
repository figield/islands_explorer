import os
import unittest
from abc import ABC, abstractmethod

from islands_discovery import main
from tests.arbitrary.islands_discovery_arbitrary_solution_1 import Graph
from utils.streams import read_matrix_from_file, stream_data_from_array2d, stream_data_from_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "test_data")


class TestIslandsDiscovery(ABC):

    @abstractmethod
    def _test_islands_discovery(self, test_data_file, expected_result):
        pass

    def test_typical_case_random_map(self):
        """
        Testing typical case for a random map
        """
        self._test_islands_discovery(f'{DATA_PATH}/map.txt', expected_result=4)
        self._test_islands_discovery(f'{DATA_PATH}/map4.txt', expected_result=15)
        self._test_islands_discovery(f'{DATA_PATH}/map5.txt', expected_result=5)
        self._test_islands_discovery(f'{DATA_PATH}/map6.txt', expected_result=5)
        self._test_islands_discovery(f'{DATA_PATH}/map13.txt', expected_result=5)

    def test_empty_map(self):
        """
        Testing map without islands or water
        """
        self._test_islands_discovery(f'{DATA_PATH}/map0.txt', expected_result=0)

    def test_water_only_map(self):
        """
        Testing map without islands
        """
        self._test_islands_discovery(f'{DATA_PATH}/map8.txt', expected_result=0)

    # def test_milion_islands_sauce(self):
    #     """
    #     Testing very large map
    #     """
    #     self._test_islands_discovery(f'{DATA_PATH}/map_milion.txt', expected_result=516096)

    def test_map_with_one_island(self):
        """
        Testing different maps with one island only
        """
        for file_postfix in [1, 2, 3, 10, 11]:
            self._test_islands_discovery(f'{DATA_PATH}/map{file_postfix}.txt', expected_result=1)

    def test_map_with_one_big_island_covering_whole_map(self):
        """
        Testing different maps with one big island only covering the whole map
        """
        for file_postfix in [12, 14]:
            self._test_islands_discovery(f'{DATA_PATH}/map{file_postfix}.txt', expected_result=1)

    def test_column_islands(self):
        """
        Testing nap with column shaped islands
        """
        self._test_islands_discovery(f'{DATA_PATH}/map7.txt', expected_result=8)

    def test_row_islands(self):
        """
        Testing nap with row shaped islands
        """
        self._test_islands_discovery(f'{DATA_PATH}/map9.txt', expected_result=5)


class TestIslandsDiscoveryFromFile(unittest.TestCase, TestIslandsDiscovery):

    def _get_data_streamer(self):
        return stream_data_from_file

    def _test_islands_discovery(self, test_data_file, expected_result):
        actual_result = main(test_data_file, self._get_data_streamer())
        self.assertEqual(expected_result, actual_result,
                         f"Expected to discover {expected_result} islands, file: {test_data_file}")


class TestIslandsDiscoveryFromMatrix(unittest.TestCase, TestIslandsDiscovery):

    def _get_data_streamer(self):
        return stream_data_from_array2d

    def _test_islands_discovery(self, test_data_file, expected_result):
        actual_result = main(test_data_file, self._get_data_streamer())
        self.assertEqual(expected_result, actual_result,
                         f"Expected to discover {expected_result} islands, file: {test_data_file}")


class TestIslandsDiscoveryByArbitrarySolution(unittest.TestCase, TestIslandsDiscovery):
    """
    Notes:
        Arbitrary solution base on Graph (by Shivam Shrey) cannot handle matrix filled
        with one island of size 25x40, 10x120 or bigger. Test is failing for maps no. 12 and 14.

        In addition to the disadvantages, this test scenario serves as a validation of the test data
        and the tests themselves.
    """

    def _test_islands_discovery(self, test_data_file, expected_result):
        array2d = read_matrix_from_file(test_data_file)
        if not array2d:
            array2d = [[]]
        row = len(array2d)
        col = len(array2d[0])
        g = Graph(row, col, array2d)
        actual_result = g.countIslands()
        self.assertEqual(expected_result, actual_result,
                         f"Expected to discover {expected_result} islands, file: {test_data_file}")

    def test_map_with_one_big_island_covering_whole_map(self):
        """
         Error: `RecursionError: maximum recursion depth exceeded in comparison.`
        """
        pass
