"""
This file is a module for the game Automaze. It contains sprite classes and modulates their movement on update. It is imported into the Automaze main.py module and references the config.py module.
"""

from config import *

import arcade

class Player(arcade.Sprite):
    """
    Contains all moving sprites and moves them when Game.on_update from the main.py module is called; inherits from the Arcade Sprite parent class.
    """
    
    def update(self):
        """
        Moves player sprites on update.

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

        self.center_x += self.change_x
        self.center_y += self.change_y