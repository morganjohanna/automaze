"""
This file is a module for the game Automaze. It procedurally generates a random level as a 2D numpy array and ensures it is passable from start to finish and within the player's current difficulty level. It is imported into the Automaze main.py module and references the config.py module.
"""

from config import *

import numpy as np
import pandas as pd
import random
import copy

class LevelGenerator():
    """
    Generates the level map as a 2D numpy array (generate_level), validates it is passable from start to finish cells (find_path), and checks that it is within the player's current difficulty level (validate_difficulty).
    
    Key for individual cells in level array
    created with generate_level:
    0 == open cell
    1 == wall cells
    2 == start cell
    3 == finish cell

    created with find_path:
    4 == h cost calculated, recorded in pathway_df
    5 == cell neighbors assessed from this cell already, marked with assessed "yes" in pathway_df

    Difficulty level settings are in the config.py module.
    """

    def __init__(self, width, height):
        """
        Initializes class instance

        Parameters
        ----------
        self.width: integer
            The width of the numpy array, must be minimum 4
        self.height: integer
            The height of the numpy array, must be minimum 4

        Returns
        -------
        None
        
        Raises
        ------
        NameError: name 'abc' is not defined
            Raised when width or height input is a string (here, 'abc')
        """
                
        self.width = width
        self.height = height

        self.level_raw = np.ones((self.width, self.height))

        self.start_x = 0
        self.start_y = 0
        self.finish_x = 0
        self.finish_y = 0

        self.pathway_df = pd.DataFrame(columns = ["x", "y", "parent_x", "parent_y", "h_cost", "assessed"])
        self.pathway_df.reset_index()
        self.pathway_df = self.pathway_df.astype("int")

        self.path_found = False
        self.min_number_steps = 0
        self.difficulty_validated = False

    def generate_level(self):
        """
        Generates a 2D numpy array of height and width (as provided in __init__) to serve as a level map; includes border walls, randomized internal walls, and randomly-identified start and finish cells.

        Parameters
        ----------
        None

        Returns
        -------
        self.level_raw: array
            Two-dimensional, contains cell values coded as indicated in the class documentation
        self.start_x: integer
            Randomly selected inside array walls, the x coordinate of the start cell (where the player begins in the level)
        self.start_y: integer
            Randomly selected inside array walls, the y coordinate of the start cell (where the player begins in the level)
        self.finish_x: integer
            Randomly selected inside array walls, the x coordinate of the target cell (where the player is trying to get to in the level)
        self.finish_y: integer
            Randomly selected inside array walls, the y coordinate of the target cell (where the player is trying to get to in the level)

        Raises
        ------
        ValueError: empty range for randrange() (1, n, 0)
            Raised when width or height provided at class instantiation is 2
        ValueError: empty range for randrange() (1, n, -1)
            Raised when width or height provided at class instantiation is 1
        ValueError: empty range for randrange() (1, -1, -2)
            Raised when width or height provided at class instantiation is 0
        TypeError: 'float' object cannot be interpreted as an integer
            Raised when width or height provided at class instantiation is a float
        """

        self.level_raw[1:-1, 1:-1] = 0

        self.start_x = random.randint(1, self.width-2)
        self.start_y = random.randint(1, self.height-2)
        self.finish_x = random.randint(1, self.width-2)
        self.finish_y = random.randint(1, self.height-2)

        self.level_raw[self.start_y, self.start_x] = 2
        self.level_raw[self.finish_y, self.finish_x] = 3

        starter_cells = [0, 1]

        for y in range (1, self.height-1):
            for x in range(1, self.width-1):
                if self.level_raw[y, x] == 0:
                    cell = random.choices(starter_cells, weights = (70, 30), k = 1)
                    self.level_raw[y, x] = cell[0]

                else:
                    pass

        return self.level_raw, self.start_x, self.start_y, self.finish_x, self.finish_y
    
    def find_path(self):
        """
        Determines if there is a path along open cells from the start to finish cells (see cell value codes in the class documentation) and, if so, what the minimum number of steps required to reach it is. Vertical (0, +/-1), horizontal (+/-1, 0), and diagonal (+/-1, +/-1) movement are all possible.

        Parameters
        ----------
        None
        
        Returns
        -------
        self.path_found: boolean
            Returns True when a path can be found from the start to finish cells and False when it cannot be
        self.min_number_steps: integer
            The minimum number of steps required to get from the start coordinates to the target coordinates; only returned if path found
        pathway_df: dataframe
            With columns "level_raw" (2D numpy array, the level array with cells coded as indicated in the class documentation), 
            "start_x" (integer, the x coordinate of the start cell), 
            "start_y" (integer, the y coordinate of the start cell), 
            "finish_x" (integer, the x coordinate of the target cell), 
            "finish_y" (integer, the y coordinate of the target cell), and 
            "MNS" (integer, the minimum number of steps required to reach the finish cell from the start cell)

        Raises
        ------
        IndexError: index 0 is out of bounds for axis 0 with size 0
            Raised when width or height provided at class instantiation is 3
        """

        self.pathway_df = pd.DataFrame(columns = ["x", "y", "parent_x", "parent_y", "h_cost", "assessed"])
        self.pathway_df.reset_index()
        self.pathway_df = self.pathway_df.astype("int")

        current_x = self.start_x
        current_y = self.start_y

        parent_x = self.start_x
        parent_y = self.start_y

        level_path = copy.deepcopy(self.level_raw)

        self.path_found = False
        self.min_number_steps = 1

        while self.path_found == False:
            stop_looping = False

            for y in range(current_y-1, current_y+2):
                if stop_looping == True:
                    break

                for x in range(current_x-1, current_x+2):
                    if (y == current_y and x == current_x) or level_path[y, x] == 1 or level_path[y, x] == 2 or level_path[y, x] == 5 or level_path[y, x] == 4: # not the current cell, a wall, the start cell, or previously assessed
                        pass

                    elif level_path[y, x] == 3: # finish cell
                        f_cost = (abs(abs(x - self.start_x) - abs(y - self.start_y)) + min(abs(x - self.start_x), abs(y - self.start_y)))
                        g_cost = (abs(abs(x - self.finish_x) - abs(y - self.finish_y)) + min(abs(x - self.finish_x), abs(y - self.finish_y)))
                        h_cost = f_cost + g_cost

                        self.pathway_df = pd.concat([self.pathway_df, pd.DataFrame([[x, y, current_x, current_y, h_cost, "no"]], columns = self.pathway_df.columns)], ignore_index = True)
                    
                        
                        path_x = int(self.pathway_df.loc[self.pathway_df.index[-1], "parent_x"])
                        path_y = int(self.pathway_df.loc[self.pathway_df.index[-1], "parent_y"])
                        
                        if path_x == self.start_x and path_y == self.start_y:
                            pass
                        
                        else: #open cells not previously assessed
                            while path_x != self.start_x or path_y != self.start_y:
                                path_x_interim = self.pathway_df.loc[((self.pathway_df["x"] == path_x) & (self.pathway_df["y"] == path_y)), "parent_x"]
                                path_x_interim = path_x_interim.iloc[0].item()
                                
                                path_y = self.pathway_df.loc[((self.pathway_df["x"] == path_x) & (self.pathway_df["y"] == path_y)), "parent_y"]
                                path_y = path_y.iloc[0].item()

                                path_x = path_x_interim

                                self.min_number_steps = self.min_number_steps + 1
                        
                        self.path_found = True
                        stop_looping = True
                        
                        return self.min_number_steps, self.path_found

                    else:
                        f_cost = (abs(abs(x - self.start_x) - abs(y - self.start_y)) + min(abs(x - self.start_x), abs(y - self.start_y)))
                        g_cost = (abs(abs(x - self.finish_x) - abs(y - self.finish_y)) + min(abs(x - self.finish_x), abs(y - self.finish_y)))
                        h_cost = f_cost + g_cost

                        self.pathway_df = pd.concat([self.pathway_df, pd.DataFrame([[x, y, current_x, current_y, h_cost, "no"]], columns = self.pathway_df.columns)], ignore_index = True)
                        level_path[y, x] = 4
                
            level_path[current_y, current_x] = 5
            self.pathway_df["assessed"] = np.where((self.pathway_df["x"] == current_x) & (self.pathway_df["y"] == current_y), "yes", self.pathway_df["assessed"])

            # filters by whether or not a cell has been assessed, sets new coordinates to assess surrounding cells and how we got there; returns False if no path can be found
            try:
                pathway_df_open = self.pathway_df[self.pathway_df["assessed"] == "no"]
                lowest_h = pathway_df_open["h_cost"].min(skipna = True)
                parent_x = pathway_df_open.loc[pathway_df_open["h_cost"] == lowest_h, "parent_x"].values[0]
                parent_y = pathway_df_open.loc[pathway_df_open["h_cost"] == lowest_h, "parent_y"].values[0]
                current_x = pathway_df_open.loc[pathway_df_open["h_cost"] == lowest_h, "x"].values[0]
                current_y = pathway_df_open.loc[pathway_df_open["h_cost"] == lowest_h, "y"].values[0]

            except:
                return self.path_found, self.min_number_steps, self.pathway_df

    def validate_difficulty(self, player_difficulty):
        """
        Checks that the minimum number of steps for the level generated is appropriate for the player's current difficulty level, by calling the function difficulty_scale from the config.py module.

        Parameters
        ----------
        player_difficulty: string
            The player's current difficulty setting, expressed as "Level n" where n is between 1 (easiest) and 4 (hardest)

        Returns
        -------
        self.difficulty_validated: boolean
            Returns True when minimum number of steps for the level is appropriate for the player's current difficulty setting and False when it is not

        Raises
        ------
        None
        """

        self.difficulty_validated = False

        if difficulty_scale(self.min_number_steps) == player_difficulty:
            self.difficulty_validated = True

        return self.difficulty_validated