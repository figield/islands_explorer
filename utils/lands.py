def get_first_neighbor_name(row: int, column: int, positions: dict) -> str:
    """

    2 3 4
    1-?
    """

    # get first neighbour name
    neighbour_name = positions.get((row, column - 1))
    if neighbour_name:
        return neighbour_name

    # get second neighbour name
    neighbour_name = positions.get((row - 1, column - 1))
    if neighbour_name:
        return neighbour_name

    # get third neighbour name
    neighbour_name = positions.get((row - 1, column))
    if neighbour_name:
        return neighbour_name

    # get third neighbour name
    neighbour_name = positions.get((row - 1, column + 1))
    if neighbour_name:
        return neighbour_name


def raname_neighbour_land(position: tuple, positions: dict, lands: dict, land_name: str) -> None:
    """

    2 3 4        1 3 4
    1-1     ->   1-1
    """
    neighbour_name = positions.get(position)
    if neighbour_name is not None and neighbour_name != land_name:
        neighbor_positions = lands[neighbour_name]
        for neighbor_position in neighbor_positions:
            positions[neighbor_position] = land_name
        lands[land_name].extend(lands[neighbour_name])
        del lands[neighbour_name]


def connect_neighbours(row: int, column: int, positions: dict, lands: dict) -> None:
    """

    2 3 4        1 1 1
    1-1     ->   1-1
    """
    land_name = positions[(row, column)]

    # renaming the first neighbor can be skipped because the current name is derived from it.

    # ranaming second neighbour land
    raname_neighbour_land((row - 1, column - 1), positions, lands, land_name)

    # ranaming third neighbour land
    raname_neighbour_land((row - 1, column), positions, lands, land_name)

    # ranaming fourth neighbour land
    raname_neighbour_land((row - 1, column + 1), positions, lands, land_name)


def discover_land(row: int, column: int, positions: dict, lands: dict) -> None:
    """

    """
    land_name = get_first_neighbor_name(row, column, positions)
    if not land_name:
        land_name = f"{row}-{column}"
    positions[(row, column)] = land_name
    recorded_positions = lands.get(land_name, [])
    recorded_positions.append((row, column))
    lands[land_name] = recorded_positions


def forget_lands_beyond_the_horizon(row_len: int, row: int, column: int, positions: dict, lands: dict) -> None:
    """
        xxxxxxxxx <- previous lands data is not needed
        xxxxx0100 <- also some positions in the upper row are not needed
        111000100
              ^- we are here
    """
    forgotten_lands = 0
    # delete row 2 lewel upper
    for i in range(row_len):
        position = (row - 2, column + i)
        land_name = positions.get(position)
        if land_name:
            land_positions = lands[land_name]
            land_positions.pop(land_positions.index(position))
            if not land_positions:
                del lands[land_name]
                forgotten_lands += 1
            del positions[position]

    # delete data from rows on the upper level, behind the current column
    for c in range(column - 1):
        position = (row - 1, c)
        land_name = positions.get(position)
        if land_name:
            land_positions = lands[land_name]
            land_positions.pop(land_positions.index(position))
            if not land_positions:
                del lands[land_name]
                forgotten_lands += 1
            del positions[position]

    return forgotten_lands
