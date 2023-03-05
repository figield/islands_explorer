class Explorer:

    def __init__(self, file_path: str, data_streamer):
        self.positions = {}
        self.lands = {}
        self.row = 0
        self.column = 0
        self.file_path = file_path
        self.data_streamer = data_streamer

    def go_to_next_row(self):
        self.row += 1
        self.column = 0

    def move_forward(self):
        self.column += 1

    def create_current_land_name(self):
        return f"{self.row}-{self.column}"

    def discover_land(self) -> None:
        """

        """
        land_name = self.get_neighbor_name()
        current_position = (self.row, self.column)
        if not land_name:
            land_name = self.create_current_land_name()
        self.positions[current_position] = land_name
        recorded_positions = self.lands.get(land_name, [])
        recorded_positions.append(current_position)
        self.lands[land_name] = recorded_positions

    def get_neighbor_name(self) -> str:
        """
        Get the first existing neighbor's name in clockwise order.
        In the diagram below, the name will be taken from neighbour with number 1.
        Then from neighbours with number 2, 3 and 4.

            2 3 4
            1-?

        """

        for dr, dc in [(0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            neighbour_name = self.positions.get((self.row + dr, self.column + dc))
            if neighbour_name:
                return neighbour_name

    def count_lands_beyond_horizon(self, row_len):
        """
        Count islands beyond the horizon. Delete those wich are already counted.

            xxxxxxxxx <- previous lands data is not needed
            101100100
            111000100
                  ^- current position
        """
        forgotten_lands = 0
        for i in range(row_len):
            position = (self.row - 2, self.column + i)
            land_name = self.positions.get(position)
            if land_name:
                land_positions = self.lands[land_name]
                land_positions.pop(land_positions.index(position))
                if not land_positions:
                    del self.lands[land_name]
                    forgotten_lands += 1
                del self.positions[position]

        return forgotten_lands

    def connect_neighbours(self) -> None:
        """
        Considered neighbours to be connected are lands next to the explored position.
        First land is with the position behind the explorer. Next lands may start with the posistion
        above the explorer (2, 3, 4).
        Neighbour lands are connected in the clockwise order. When lands are conneced then they have the same name.

            2 3 4        1 1 1
            1-1     ->   1-1

        Note:
            Renaming the first neighbour can be skipped because the current name is derived from it.
        """

        for dr, dc in [(-1, -1), (-1, 0), (-1, 1)]:
            neighbour_position = (self.row + dr, self.column + dc)
            self.raname_land(neighbour_position)

    def raname_land(self, position: tuple) -> None:
        """

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
        """
        row_len = 0
        lands_beyond_horizon = 0
        row_to_clean = 0

        for data in self.data_streamer(self.file_path):
            if data == "\n":
                row_len = self.column
                self.go_to_next_row()
                continue

            if int(data) == 1:
                self.discover_land()
                self.connect_neighbours()

            # for memory optimalization
            if row_to_clean + 2 == self.row:
                lands_beyond_horizon += self.count_lands_beyond_horizon(row_len)
                row_to_clean += 1

            self.move_forward()

        return len(self.lands) + lands_beyond_horizon
