import unittest

from utils.explorer import Explorer


class TestExplorer(unittest.TestCase):

    def setUp(self) -> None:
        test_data_file = ""
        data_streamer = None
        self.explorer = Explorer(test_data_file, data_streamer)

    def test_go_to_next_row(self) -> None:
        self.assertEqual(0, self.explorer.row)
        self.assertEqual(0, self.explorer.column)
        self.explorer.go_to_next_row()
        self.assertEqual(1, self.explorer.row)
        self.assertEqual(0, self.explorer.column)

    def test_move_forward(self) -> None:
        self.assertEqual(0, self.explorer.row)
        self.assertEqual(0, self.explorer.column)
        self.explorer.move_forward()
        self.assertEqual(0, self.explorer.row)
        self.assertEqual(1, self.explorer.column)

    def test_create_current_land_name(self) -> None:
        """
         map:
          1

         current position (before exploration):
          (0,0)
        """
        self.assertEqual('0-0', self.explorer.create_current_land_name())

    def test_explore_position_no_neighbours(self) -> None:
        """
         map:
          1

         current position (before exploration):
          (0,0)
        """
        self.assertDictEqual({}, self.explorer.positions)
        self.assertDictEqual({}, self.explorer.lands)
        self.explorer.explore_position()
        self.assertEqual(0, self.explorer.row)
        self.assertEqual(0, self.explorer.column)
        self.assertDictEqual({(0, 0): '0-0'}, self.explorer.positions)
        self.assertDictEqual({'0-0': [(0, 0)]}, self.explorer.lands)

    def test_explore_position_with_neighbour(self) -> None:
        """
         map:
          11

         current position (before exploration):
          (0,1)
        """
        self.explorer.positions = {(0, 0): '0-0'}
        self.explorer.lands = {'0-0': [(0, 0)]}
        self.explorer.move_forward()
        self.explorer.explore_position()
        self.assertEqual(0, self.explorer.row)
        self.assertEqual(1, self.explorer.column)
        self.assertDictEqual({(0, 0): '0-0', (0, 1): '0-0'},
                             self.explorer.positions)
        self.assertDictEqual({'0-0': [(0, 0), (0, 1)]},
                             self.explorer.lands)

    def test_explore_position_on_new_land(self) -> None:
        """
         map:
          1101

         current position (before exploration):
          (0,3)
        """
        self.explorer.positions = {(0, 0): '0-0', (0, 1): '0-0'}
        self.explorer.lands = {'0-0': [(0, 0), (0, 1)]}
        self.explorer.move_forward()
        self.explorer.move_forward()
        self.explorer.move_forward()
        self.explorer.explore_position()
        self.assertEqual(0, self.explorer.row)
        self.assertEqual(3, self.explorer.column)
        self.assertDictEqual({(0, 0): '0-0', (0, 1): '0-0', (0, 3): '0-3'},
                             self.explorer.positions)
        self.assertDictEqual({'0-0': [(0, 0), (0, 1)], '0-3': [(0, 3)]},
                             self.explorer.lands)

    def test_get_neighbour_name(self) -> None:
        """
         map:
          101
          011

         current position (before exploration):
          (1,1)
        """
        self.explorer.positions = {(0, 0): '0-0', (0, 2): '0-2'}
        self.explorer.lands = {'0-0': [(0, 0)], '0-2': [(0, 2)]}
        self.explorer.row = 1
        self.explorer.column = 1

        land_name = self.explorer.get_neighbour_name()
        self.assertEqual('0-0', land_name)

    def test_get_neighbour_name_from_first_neighbour(self) -> None:
        """
         map:
          101
          110

         current position:
          (1,1)
        """
        self.explorer.positions = {(0, 0): '0-0', (0, 2): '0-2', (1, 0): '0-0'}
        self.explorer.lands = {'0-0': [(0, 0), (1, 0)], '0-2': [(0, 1)]}
        self.explorer.row = 1
        self.explorer.column = 1

        land_name = self.explorer.get_neighbour_name()
        self.assertEqual('0-0', land_name)

    def test_connect_neighbours(self) -> None:
        """
         map:
          101
          010

         current position (after exploration):
          (1,1)
        """
        self.explorer.positions = {(0, 0): '0-0', (0, 2): '0-2', (1, 1): '0-0'}
        self.explorer.lands = {'0-0': [(0, 0), (1, 1)], '0-2': [(0, 2)]}
        self.explorer.row = 1
        self.explorer.column = 1

        self.explorer.connect_neighbours()
        self.assertDictEqual({(0, 0): '0-0', (0, 2): '0-0', (1, 1): '0-0'},
                             self.explorer.positions)
        self.assertDictEqual({'0-0': [(0, 0), (1, 1), (0, 2)]},
                             self.explorer.lands)

    def test_raname_land(self) -> None:
        """
         map:
          001
          101
          010

         current position (after exploration):
          (2,1)
        """
        self.explorer.positions = {(0, 2): '0-2', (1, 0): '1-0',
                                   (1, 2): '0-2', (2, 1): '1-0'
                                   }
        self.explorer.lands = {'0-2': [(0, 2), (1, 2)],
                               '1-0': [(0, 1), (2, 1)]
                               }
        self.explorer.row = 2
        self.explorer.column = 1

        self.explorer.connect_neighbours()
        self.assertDictEqual({(0, 2): '1-0', (1, 0): '1-0',
                              (1, 2): '1-0', (2, 1): '1-0'
                              },
                             self.explorer.positions)
        self.assertDictEqual({'1-0': [(0, 1), (2, 1), (0, 2), (1, 2)]},
                             self.explorer.lands)

    def test_count_lands_beyond_horizon(self) -> None:
        """
         map:
          001 <- lands to be forgotten
          ---
          100
          010

         current position (after exploration):
          (2,1)
        """

        self.explorer.positions = {(0, 2): '0-2',
                                   (1, 0): '1-0', (2, 1): '1-0'
                                   }
        self.explorer.lands = {'1-0': [(1, 0), (2, 1)],
                               '0-2': [(0, 2)]
                               }
        self.explorer.row = 2
        self.explorer.column = 1
        row_len = 3
        counted_lands = self.explorer.count_lands_beyond_horizon(row_len)
        self.assertEqual(1, counted_lands)
        self.assertDictEqual({(1, 0): '1-0', (2, 1): '1-0'},
                             self.explorer.positions)
        self.assertDictEqual({'1-0': [(1, 0), (2, 1)]},
                             self.explorer.lands)

    def test_count_islands(self) -> None:
        """
         map:
          001
          100
          010

         current position (after exploration):
          (0,0)
        """

        def data_streamer(_):
            array2d = [[0, 0, 1],
                       [1, 0, 0],
                       [0, 1, 0]]
            for row in array2d:
                for data in row:
                    yield data
                yield "\n"

        self.explorer.data_streamer = data_streamer
        counted_lands = self.explorer.count_islands()
        self.assertEqual(2, counted_lands)
        self.assertDictEqual({(1, 0): '1-0', (2, 1): '1-0'},
                             self.explorer.positions)
        self.assertDictEqual({'1-0': [(1, 0), (2, 1)]},
                             self.explorer.lands)
