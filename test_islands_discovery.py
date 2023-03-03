import unittest

from islands_discovery import discover_amount_of_islands


class TestIslandsDiscovery(unittest.TestCase):

    def _test_islands_discovery(self, test_data_file, expected_result):
        actual_result = discover_amount_of_islands(test_data_file)
        self.assertEqual(expected_result, actual_result,
                         f"Expected to discover {expected_result} islands, file: {test_data_file}")

    def test_typical_case_random_map(self):
        """
        Testing typical case for a random map
        """
        self._test_islands_discovery('test_data/map.txt', expected_result=4)
        self._test_islands_discovery('test_data/map4.txt', expected_result=15)
        self._test_islands_discovery('test_data/map5.txt', expected_result=5)
        self._test_islands_discovery('test_data/map6.txt', expected_result=5)
        self._test_islands_discovery('test_data/map13.txt', expected_result=5)

    def test_empty_map(self):
        """
        Testing map without islands or water
        """
        self._test_islands_discovery('test_data/map0.txt', expected_result=0)

    def test_water_only_map(self):
        """
        Testing map without islands
        """
        self._test_islands_discovery('test_data/map8.txt', expected_result=0)


    def test_milion_islands_sauce(self):
        """
        Testing very large map
        """
        self._test_islands_discovery('test_data/map_milion.txt', expected_result=516096)

    def test_map_with_one_island(self):
        """
        Testing different maps with one island only
        """
        for file_postfix in [1, 2, 3, 10, 11, 12]:
            self._test_islands_discovery(f'test_data/map{file_postfix}.txt', expected_result=1)

    def test_column_islands(self):
        """
        Testing nap with column shaped islands
        """
        self._test_islands_discovery('test_data/map7.txt', expected_result=8)

    def test_row_islands(self):
        """
        Testing nap with row shaped islands
        """
        self._test_islands_discovery('test_data/map9.txt', expected_result=5)

