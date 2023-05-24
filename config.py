"""
This file is a module for the game Automaze. It provides constants for the screen size, title, text rows, and number of maze cells, as well as the difficulty_scale function, which references a difficulty setting against the minimum number of steps required to get from the start to finish cells (see the level_generator.py module for more information). It is imported into the Automaze level_generator.py, main.py, rooms.py, and sprites.py modules.
"""

TILES_WIDE = 20
TILES_HIGH = 20
TILE_SIZE = 50
SCREEN_TITLE = "Automaze!"

HORIZONTAL_MARGIN = 0
VERTICAL_MARGIN = 0

SCALING = 1

SCREEN_WIDTH = TILES_WIDE * TILE_SIZE + HORIZONTAL_MARGIN * 2
SCREEN_HEIGHT = TILES_HIGH * TILE_SIZE + VERTICAL_MARGIN * 2

DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 20

def difficulty_scale(number_steps):
    """
    References the minimum number of steps required to get from the start to finish cells against a difficulty setting. Called by the level_generator.py and main.py modules.

    Parameters
    ----------
    number_steps: integer
        The minimum number of steps required to travel from the start to finish cells (see level_generator.py module documentation for more information)

    Returns
    -------
    string
        The equivalent difficulty setting, expressed as "Level n" where n is between 1 (easiest) and 4 (hardest)

    Raises
    ------
    None

    """

    if 1 <= number_steps < 6:
        return "Level 1"
    elif 6 <= number_steps < 11:
        return "Level 2"
    elif 11 <= number_steps < 16:
        return "Level 3"
    elif 16 <= number_steps:
        return "Level 4"