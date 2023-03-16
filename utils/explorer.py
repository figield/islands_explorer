from utils.streams import LandDataStreamer


class Explorer:

    def __init__(self, data_streamer: LandDataStreamer):
        self.positions: dict = {}
        self.lands: dict = {}
        self.row: int = 0
        self.column: int = 0
        self.data_streamer: LandDataStreamer = data_streamer

    def _go_to_next_row(self):
        self.row += 1
        self.column = 0

    def _move_forward(self):
        self.column += 1

    def _create_current_land_name(self) -> str:
        return f"{self.row}-{self.column}"

    def _explore_position(self) -> None:
        """
         Explore the position require the following steps:
         - if there are neighbours next to the current position,
           then the name is taken from the first neigbour.
           The position with the same name as a neighbor becomes
           part of the adjacent land.
         - if there is no neighbours, then name is based on coordinates,
           like `0-0`.
         - information about the position and name of the land is saved
           in the appropriate dictionaries.
        """
        land_name = self._get_neighbour_name()
        current_position = (self.row, self.column)
        if not land_name:
            land_name = self._create_current_land_name()
        self.positions[current_position] = land_name
        recorded_positions = self.lands.get(land_name, [])
        recorded_positions.append(current_position)
        self.lands[land_name] = recorded_positions

    def _get_neighbour_name(self) -> str:
        """
         Get the first existing neighbour's name in clockwise order.
         In the diagram below, the name will be taken from neighbour
         with number 1.
         Then from neighbours with number 2, 3 and 4.

            2 3 4
            1-?

        """
        neighbour_name = ""
        for dr, dc in [(0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            row = self.row + dr
            column = self.column + dc
            if row < 0 or column < 0:
                continue
            neighbour_name = self.positions.get((row, column))
            if neighbour_name:
                return neighbour_name
        return neighbour_name

    def _count_lands_beyond_horizon(self, row_len: int) -> int:
        """
         Count islands beyond the horizon.
         Delete those which are already counted.

            xxxxxxxxx <- previous lands data is not needed
            --------- <- horizon
            101100100
            111000100
                  ^- current position
        """
        lands_beyond_horizon = 0
        for i in range(row_len):
            position = (self.row - 2, self.column + i)
            land_name = self.positions.get(position)
            if land_name:
                land_positions = self.lands[land_name]
                land_positions.pop(land_positions.index(position))
                if not land_positions:
                    del self.lands[land_name]
                    lands_beyond_horizon += 1
                del self.positions[position]

        return lands_beyond_horizon

    def _connect_neighbours(self) -> None:
        """
         Considered neighbours to be connected are lands next
         to the explored position.
         First land is with the position behind the explorer.
         Next lands may start with the posistion above the explorer (2, 3, 4).
         When lands are conneced then they have the same name.

            2 3 4        1 1 1
            1-1     ->   1-1

         Note:
             Renaming the first neighbour can be skipped because
             the current name is derived from it.
        """

        for dr, dc in [(-1, -1), (-1, 0), (-1, 1)]:
            neighbour_position = (self.row + dr, self.column + dc)
            self._raname_land(neighbour_position)

    def _raname_land(self, position: tuple) -> None:
        """
         Neighbour lands are connected in the clockwise order.

         2 3 4        1 3 4
         1-1     ->   1-1

        """
        neighbour_name = self.positions.get(position)
        land_name = self.positions[(self.row, self.column)]
        if neighbour_name is not None and neighbour_name != land_name:
            neighbor_positions = self.lands[neighbour_name]
            for neighbor_position in neighbor_positions:
                self.positions[neighbor_position] = land_name
            self.lands[land_name].extend(self.lands[neighbour_name])
            del self.lands[neighbour_name]

    def count_islands(self) -> int:
        """
         This method is the entry point for the whole algorithm.
         The explorer, moving from left to right, explores only neighboring
         positions and connects neighbors around.

         Counting islands require the following steps:
         1. Explore the position
         2. Connecting neighbors
         3. Counting islands beyond the horizon (optional step for memory
            efficiency).
         4. Islands stored in the `lands` dictionary must be counted and added
            to the `lands_beyond_horizon` from step 3.
        """
        row_len = 0
        lands_beyond_horizon = 0
        row_to_clean = 0

        for data in self.data_streamer.stream_data():
            if data is None:
                row_len = self.column
                self._go_to_next_row()
                continue

            if self.data_streamer.is_land(data):
                self._explore_position()
                self._connect_neighbours()

            # for memory optimalization
            if row_to_clean + 2 == self.row:
                lands_beyond_horizon += \
                    self._count_lands_beyond_horizon(row_len)
                row_to_clean += 1

            self._move_forward()

        return len(self.lands) + lands_beyond_horizon
