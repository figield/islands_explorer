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
