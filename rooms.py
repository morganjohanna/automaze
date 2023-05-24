"""
This file is a module for the game Automaze. It contains room (aka level or page) classes and initiates requisite variables on instantiation. It is imported into the Automaze main.py module and references the config.py module.
"""

from config import *

class Room():
    
    """
    Instantiates requisite variables for each room (aka level or page) required to render background graphics, sprite graphics, and text.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    None

    """
    
    def __init__(self):
        self.heading = None
        self.text = None
        self.background = None
        self.map_open_cell = None
        self.map_wall_cell = None
        self.map_finish_cell = None
        self.player_sprite = None