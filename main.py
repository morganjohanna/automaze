"""
This file is a module for the game Automaze. It procedurally generates a random level as a 2D numpy array and ensures it is passable from start to finish and within the player's current difficulty level. It references the config.py, level_generator.py, rooms.py, and sprites.py modules.
"""

from config import *
from level_generator import *
from sprites import *
from rooms import *

import arcade
import numpy as np
import pandas as pd
from datetime import datetime as dt

min_number_steps_global = 0
player_number_steps_global = 0
player_difficulty_global = "Level 1"
iteration_global = 0

class Game(arcade.Window):
    """
    Main application class which manages graphics rendering, keypress events, and sprite movement calculation and validation and triggers room setup and maze level generation and validation; inherits from the Arcade Window parent class. The game consists of four rooms, keypress event controls, and a simple game loop:
    
    A. From room 0 (intro page 'intro') to room 1 (maze level 'level') with SPACE
    B. From room 1 (maze level 'level) to room 2 (level finish page 'finish_level') by reaching the finish cell (user navigates stepwise by use of UP, DOWN, LEFT, RIGHT, and diagonally by pressing at least two keys)
    C. From room 2 (level finish page 'finish_level') to room 1 (maze level 'level') with SPACE
    D. From any room to room 3 (game over page 'finish_game') with ESCAPE
    E. From room 3 (game over page 'finish_game') the program is ended with SPACE or ESCAPE

    The user moves in a loop A -> B -> C -> B -> C ... -> D -> E. The user chooses when to end the game and close the program and can do so at any time.

    """

    def __init__(self, width, height, title):
        """
        Initializes class instance.

        Parameters
        ----------
        width: integer
            The width of the game window in pixels
        height: integer
            The height of the game window in pixels
        title: string
            The title of game as it should appear on the window title bar

        Returns
        -------
        None

        Raises
        ------
        None

        """

        super().__init__(width, height, title)
        self.current_room = 0
        self.rooms = []

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.min_number_steps = 0
        self.player_number_steps = 0

        self.running = False
        self.iteration = 1
        self.player_stats = pd.DataFrame(columns=["timestamp", "username", "iteration", "difficulty", "MNS", "PNS", "completed"])
        self.player_difficulty = "Level 1"

        self.new_y_coordinates = 0
        self.new_x_coordinates = 0
        self.new_y = 0
        self.new_x = 0

        self.map_grid = np.array([
        [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
        [1., 2., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 3., 1.],
        [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]])
    
    def setup(self):
        """
        Replaces the rooms list with newly setup rooms (aka pages and level), triggers new level generation, and resets self.player_number_steps for next maze level.

        Parameters
        ----------
        None

        Returns
        -------
        self.rooms: list
            List of room (aka pages and level) objects for rendering
        self.player_number_steps: integer
            The number of steps the player made to reach the finish cell for the current level, here reset to 0 in preparation for the next maze level

        Raises
        ------
        None

        """

        global min_number_steps_global
        global player_number_steps_global
        global player_difficulty_global
        global iteration_global
        
        self.rooms = []

        self.generate_new_level()

        room = setup_intro()
        self.rooms.append(room)

        room = setup_level(self.map_grid)
        self.rooms.append(room)
        
        room = setup_finish_level()
        self.rooms.append(room)

        room = setup_finish_game()
        self.rooms.append(room)

        self.player_number_steps = 0

        return self.rooms, self.player_number_steps

    def generate_new_level(self):
        """
        Generates and validates a new level array and records the minimum number of steps required to travel from the start to finish cells by instantiating a LevelGenerator and calling its functions (see the level_generator.py module for more information).

        Parameters
        ----------
        None

        Returns
        -------
        self.map_grid: array
            2D numpy array containing coded cells, derived from LevelGenerator.generate_level (see level_generator.py module for codes)
        self.min_number_steps: integer
            The minimum number of steps to travel from the start to finish cells, derived from LevelGenerator.find_path

        Raises
        ------
        None

        """

        new_level = LevelGenerator(TILES_WIDE, TILES_HIGH)
        new_level.generate_level()
        new_level.find_path()
        new_level.validate_difficulty(self.player_difficulty)

        while new_level.path_found == False or new_level.difficulty_validated == False:
            new_level.generate_level()
            new_level.find_path()
            new_level.validate_difficulty(self.player_difficulty)

        self.map_grid = new_level.level_raw
        self.min_number_steps = new_level.min_number_steps

        return self.map_grid, self.min_number_steps

    def on_draw(self):
        """
        Clears the window of graphics before rendering background and sprite graphics and text for the current room.

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

        self.clear()

        if self.current_room == 1:
            for row in range(TILES_HIGH):
                for column in range(TILES_WIDE):
                    x = (column) * TILE_SIZE + HORIZONTAL_MARGIN
                    y = (TILES_HIGH - (row) - 1) * TILE_SIZE + VERTICAL_MARGIN

                    if self.map_grid[[row], [column]] == 0 or self.map_grid[[row], [column]] == 2:
                        arcade.draw_lrwh_rectangle_textured(x, y, TILE_SIZE, TILE_SIZE, self.rooms[self.current_room].map_open_cell)
                    
                    elif self.map_grid[[row], [column]] == 1:
                        arcade.draw_lrwh_rectangle_textured(x, y, TILE_SIZE, TILE_SIZE, self.rooms[self.current_room].map_wall_cell)
                    
                    else:
                        arcade.draw_lrwh_rectangle_textured(x, y, TILE_SIZE, TILE_SIZE, self.rooms[self.current_room].map_finish_cell)

            self.rooms[self.current_room].player_sprite.draw()
    
        else:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.rooms[self.current_room].background)

            self.rooms[self.current_room].heading.draw()
            self.rooms[self.current_room].text.draw()

    def on_update(self, delta_time):
        """
        Updates movable sprite locations in playable levels (mazes only).

        Parameters
        ----------
        delta_time: 
            How often the game is updated in number of seconds

        Returns
        -------
        None

        Raises
        ------
        None

        """

        if self.current_room == 1:
            self.rooms[self.current_room].player_sprite.update()
        
        else:
            pass

    def on_key_press(self, key, modifiers):
        """
        Key event handler, called whenever a key is pressed. In the level, only UP, DOWN, LEFT, RIGHT, and combinations of 2 are used for movement. ESCAPE will end the game, add the final row to self.player_stats and print it to .csv in the ./player_stats directory then bring the player to the final page at any time and, if pressed again from that page, end the program. SPACE will move the player from a page to the next room or end the game if already on the final page.

        Parameters
        ----------
        key: object
            Key being pressed
        modifiers: object
            Modifying key, not currently used

        Returns
        -------
        self.current_room: integer
            The current room in which the player is located, refers to a value in list self.rooms

        Raises
        ------
        None

        """

        if key == arcade.key.SPACE:
            if self.current_room == 0:
                self.current_room = 1
                
                return self.current_room
            
            elif self.current_room == 1:
                pass

            elif self.current_room == 2:
                self.current_room = 1

                return self.current_room

            elif self.current_room == 3:
                arcade.exit()
        
        elif key == arcade.key.ESCAPE:
            if self.current_room == 3:
                arcade.exit()

            else:
                self.player_stats = pd.concat([self.player_stats, pd.DataFrame([[dt.now().strftime("%Y-%m-%d %H:%M:%S"), "noname", self.iteration, self.player_difficulty, self.min_number_steps, self.player_number_steps, "no"]], columns = self.player_stats.columns)], ignore_index = True)
                self.player_stats.to_csv(f"./player_stats/player_stats_noname_{dt.now().strftime('%Y%m%d%H%M')}.csv")
                self.current_room = 3

        if self.current_room == 1:
            self.new_y = 0
            self.new_x = 0

            if key == arcade.key.UP:
                self.up_pressed = True

            if key == arcade.key.DOWN:
                self.down_pressed = True

            if key == arcade.key.LEFT:
                self.left_pressed = True

            if key == arcade.key.RIGHT:
                self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """
        Key event handler, called whenever a key is released and manages processes that result from specific keypress events. Player sprite movement is determined by calling self.move_player (which then calls self.check_valid_move) and keypress variables reset (to enable diagonal movement). If the player sprite has reached the finish cell, info is added as a row to self.player_stats, user difficulty setting is recalculated for the next maze level, global variables required for the level finish page 'finish_level' and game over page 'finish_game' are set, new rooms (aka level and pages) are setup, and the player is move to the level finish page 'finish_level'.

        Parameters
        ----------
        key: object
            Key being released, not currently referenced (meaning that if in a level, self.move_player will be called if at least one direction key is pressed and any other key is also pressed and then released)
        modifiers: object
            Modifying key, not currently used 

        Returns
        -------
        self.current_room: integer
            The current room the player is located, refers to a value in list self.rooms
        self.player_difficulty: string
            A class variable recording current player difficulty setting, string expressed as "Level n" where n is between 1 (easiest) and 4 (hardest); see config.py module for more information
        self.iteration: integer
            A class variable recording the number of maze levels completed
        player_difficulty_global: string
            A global variable recording current player difficulty setting (for use in setup_finish_level and setup_finish_game), string expressed as "Level n" where n is between 1 (easiest) and 4 (hardest); see config.py module for more information
        iteration_global: integer
            A global variable recording the number of maze levels completed (for use in setup_finish_level and setup_finish_game)
        player_number_steps_global: integer
            A global variable recording number of steps the player made to reach the finish cell for the current level (for use in setup_finish_level and setup_finish_game)
        min_number_steps_global: integer
            A global variable recording minimum number of steps required from start to finish cells for the current level (for use in setup_finish_level and setup_finish_game)

        Raises
        ------
        None

        """

        global player_difficulty_global
        global player_number_steps_global
        global min_number_steps_global
        global iteration_global

        if self.up_pressed or self.down_pressed or self.left_pressed or self.right_pressed:
            self.move_player()

            self.up_pressed = False
            self.down_pressed = False
            self.left_pressed = False
            self.right_pressed = False

        if self.map_grid[[self.new_y_coordinates], [self.new_x_coordinates]] == 3:
            player_difficulty_global = self.player_difficulty
            player_performance = self.player_number_steps - self.min_number_steps

            if player_performance <= 2:
                if self.player_difficulty == "Level 4":
                    pass
                else:
                    self.player_difficulty = "Level " + str(int(difficulty_scale(self.min_number_steps)[-1:]) + 1)

            elif player_performance >= 5:
                if self.player_difficulty == "Level 1":
                    pass
                else:
                    self.player_difficulty = "Level " + str(int(difficulty_scale(self.min_number_steps)[-1:]) - 1)
            
            iteration_global = self.iteration
            player_number_steps_global = self.player_number_steps
            min_number_steps_global = self.min_number_steps

            self.player_stats = pd.concat([self.player_stats, pd.DataFrame([[dt.now().strftime("%Y-%m-%d %H:%M:%S"), "noname", self.iteration, self.player_difficulty, self.min_number_steps, self.player_number_steps, "yes"]], columns = self.player_stats.columns)], ignore_index = True)

            self.setup()
            self.iteration = self.iteration + 1
            self.current_room = 2

            return self.current_room, self.player_difficulty, self.iteration, player_difficulty_global, iteration_global, player_number_steps_global, min_number_steps_global

    def move_player(self):
        """
        Called by self.on_key_release, determines the new location for the player sprite to move to depending on the keys pressed and then calls self.check_valid_move to validate if the cell located in the destination is accessible (e.g. an open cell or the finish cell) or not (e.g. a wall). Because self.key_on_release does not specify which key is released, this function will be called if at least one direction key is pressed and any other key is also pressed and then released. If opposing direction keys are pressed (e.g. UP and DOWN), this function prioritizes the UP and LEFT movements. If more than 2 direction keys are pressed (e.g. UP, LEFT, and RIGHT), this function prioritizes UP-LEFT, then UP-RIGHT, then DOWN-LEFT diagonal movements in this order.

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

        if self.up_pressed and self.left_pressed:
            self.new_y = self.rooms[self.current_room].player_sprite.center_y + TILE_SIZE
            self.new_x = self.rooms[self.current_room].player_sprite.center_x - TILE_SIZE

        elif self.up_pressed and self.right_pressed:
            self.new_y = self.rooms[self.current_room].player_sprite.center_y + TILE_SIZE
            self.new_x = self.rooms[self.current_room].player_sprite.center_x + TILE_SIZE

        elif self.down_pressed and self.left_pressed:
            self.new_y = self.rooms[self.current_room].player_sprite.center_y - TILE_SIZE
            self.new_x = self.rooms[self.current_room].player_sprite.center_x - TILE_SIZE

        elif self.down_pressed and self.right_pressed:
            self.new_y = self.rooms[self.current_room].player_sprite.center_y - TILE_SIZE
            self.new_x = self.rooms[self.current_room].player_sprite.center_x + TILE_SIZE

        elif self.up_pressed:
            self.new_y = self.rooms[self.current_room].player_sprite.center_y + TILE_SIZE
            self.new_x = self.rooms[self.current_room].player_sprite.center_x

        elif self.down_pressed:
            self.new_y = self.rooms[self.current_room].player_sprite.center_y - TILE_SIZE
            self.new_x = self.rooms[self.current_room].player_sprite.center_x

        elif self.left_pressed:
            self.new_y = self.rooms[self.current_room].player_sprite.center_y
            self.new_x = self.rooms[self.current_room].player_sprite.center_x - TILE_SIZE

        elif self.right_pressed:
            self.new_y = self.rooms[self.current_room].player_sprite.center_y
            self.new_x = self.rooms[self.current_room].player_sprite.center_x + TILE_SIZE

        self.check_valid_move()

    def check_valid_move(self):
        """
        This function checks if the cell the player sprite would next enter is accessible (e.g. an open or the finish cell) or not (e.g. a wall) by calculating its exact position in pixels and referencing that against self.map_grid; if accessible, the player_sprite is moved to the new cell; if not, nothing happens. It is triggered by self.move_player which is itself triggered by self.on_key_release.

        Parameters
        ----------
        None

        Returns
        -------
        self.player_number_steps: integer
            The number of steps the player made to reach the finish cell for the current level, here added to by 1 every time the player sprite moves to a new cell

        Raises
        ------
        None

        """

        self.new_y_coordinates = TILES_HIGH - int((self.new_y - TILE_SIZE/2 - VERTICAL_MARGIN) / TILE_SIZE) - 1
        self.new_x_coordinates = int((self.new_x - TILE_SIZE/2 - HORIZONTAL_MARGIN) / TILE_SIZE)
        
        if self.map_grid[[self.new_y_coordinates], [self.new_x_coordinates]] == 1:
            pass

        else:
            self.rooms[self.current_room].player_sprite.center_y = self.new_y
            self.rooms[self.current_room].player_sprite.center_x = self.new_x
            self.player_number_steps += 1
            return self.player_number_steps

def setup_intro():
    """
    Instantiates and returns the Room intro page with graphics and text containing functional information for the user at the start of game.

    Parameters
    ----------
    None

    Returns
    -------
    intro_page: object
        Contains graphics and text specifications for the intro page to be rendered

    Raises
    ------
    None

    """

    intro_page = Room()
    intro_page.background = arcade.load_texture("./img/colosseum.png")

    start_x = 0
    start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5
    intro_page.heading = arcade.Text(
        "Welcome to Automaze!",
        start_x,
        start_y,
        arcade.color.BLACK,
        DEFAULT_FONT_SIZE * 2,
        width=SCREEN_WIDTH,
        align="center"
    )

    start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 3
    intro_page.text = arcade.Text(
        "Automaze is a procedurally-generated maze game whose difficulty automatically adapts to your skill level. You control a dragon who desperately wants to get to The Sparkly in as few steps as possible. Once you reach the Sparkly, a new level will be generated which may be more or less difficult, depending on how well you did on the last one. \n\nMove your player with the arrow keys (UP, DOWN, LEFT, or RIGHT, or diagonally by pressing two keys at once, like UP and LEFT). You can only move one step at a time, and only on the grassy squares. \n\nTo quit, press the ESCAPE key at any time. \n\nWhen you're ready, please press SPACE to continue",
        start_x,
        start_y,
        arcade.color.BLACK,
        DEFAULT_FONT_SIZE*0.8,
        multiline = True,
        width = SCREEN_WIDTH,
        align="center"
    )

    return intro_page

def setup_level(map_grid):
    """
    Instantiates and returns the Room maze level with graphics and the location of the player sprite.

    Parameters
    ----------
    None

    Returns
    -------
    level: object
        Contains graphics and player sprite specifications for the maze level to be rendered

    Raises
    ------
    None

    """

    level = Room()
    level.map_open_cell = arcade.load_texture("./img/background.png", x=0, y=0, width=50, height=50)
    level.map_wall_cell = arcade.load_texture("./img/background.png", x=50, y=0, width=50, height=50)
    level.map_finish_cell = arcade.load_texture("./img/background.png", x=0, y=50, width=50, height=50)

    level.player_sprite = None
    level.player_sprite = arcade.Sprite("./img/player_small.png")
    level.player_sprite.center_x = (list(zip(*np.where(map_grid == 2)))[0][1]) * TILE_SIZE + TILE_SIZE/2 + HORIZONTAL_MARGIN
    level.player_sprite.center_y = (TILES_HIGH - list(zip(*np.where(map_grid == 2)))[0][0] - 1) * TILE_SIZE + TILE_SIZE/2 + VERTICAL_MARGIN

    return level

def setup_finish_level():
    """
    Instantiates and returns the Room level finish page with graphics and text containing functional information for the user after completing a maze level. Note that although the player sprite is also referred to, it is not rendered for the user.

    Parameters
    ----------
    None

    Returns
    -------
    finish_level_page: object
        Contains graphics and text specifications for the level finish page to be rendered

    Raises
    ------
    None

    """

    global min_number_steps_global
    global player_number_steps_global
    global player_difficulty_global
    global iteration_global

    finish_level_page = Room()

    finish_level_page.background = arcade.load_texture("./img/colosseum.png")

    start_x = 0
    start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5
    finish_level_page.heading = arcade.Text(
        "You did it!",
        start_x,
        start_y,
        arcade.color.BLACK,
        DEFAULT_FONT_SIZE * 2,
        width=SCREEN_WIDTH,
        align="center"
    )

    if player_number_steps_global == min_number_steps_global and player_number_steps_global == 1:
        start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 3
        finish_level_page.text = arcade.Text(
            f"Maze number {iteration_global} completed! \nYou are currently at Difficulty {player_difficulty_global}\nYou found the fastest route, only {str(player_number_steps_global)} step!\n\nPress SPACE to continue or ESCAPE to quit.",
            start_x,
            start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE*0.8,
            multiline = True,
            width = SCREEN_WIDTH,
            align="center"
        )
    
    elif player_number_steps_global == min_number_steps_global:
        start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 3
        finish_level_page.text = arcade.Text(
            f"Maze number {iteration_global} completed! \nYou are currently at Difficulty {player_difficulty_global}\nYou found the fastest route, only {str(player_number_steps_global)} steps!\n\nPress SPACE to continue or ESCAPE to quit.",
            start_x,
            start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE*0.8,
            multiline = True,
            width = SCREEN_WIDTH,
            align="center"
        )

    elif min_number_steps_global == 1:
        start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 3
        finish_level_page.text = arcade.Text(
            f"Maze number {iteration_global} completed! \nYou are currently at Difficulty {player_difficulty_global}\nIt took you {str(player_number_steps_global)} steps to get there but it took math only {str(min_number_steps_global)} step.\n\nPress SPACE to continue or ESCAPE to quit.",
            start_x,
            start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE*0.8,
            multiline = True,
            width = SCREEN_WIDTH,
            align="center"
        )

    else:
        start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 3
        finish_level_page.text = arcade.Text(
            f"Maze number {iteration_global} completed! \nYou are currently at Difficulty {player_difficulty_global}\nIt took you {str(player_number_steps_global)} steps to get there but it took math only {str(min_number_steps_global)} steps.\n\nPress SPACE to continue or ESCAPE to quit.",
            start_x,
            start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE*0.8,
            multiline = True,
            width = SCREEN_WIDTH,
            align="center"
        )
    
    finish_level_page.player_sprite = arcade.Sprite("./img/player_small.png")
    
    return finish_level_page

def setup_finish_game():
    """
    Instantiates and returns the Room game over page with graphics and text containing functional information for the user after quitting the game. Note that although the player sprite is also referred to, it is not rendered for the user.

    Parameters
    ----------
    None

    Returns
    -------
    finish_game_page: object
        Contains graphics and text specifications for the game over page to be rendered

    Raises
    ------
    None

    """

    global min_number_steps_global
    global player_number_steps_global
    global player_difficulty_global
    global iteration_global

    finish_game_page = Room()
    finish_game_page.background = arcade.load_texture("./img/colosseum.png")

    start_x = 0
    start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5
    finish_game_page.heading = arcade.Text(
        "Thanks for playing!",
        start_x,
        start_y,
        arcade.color.BLACK,
        DEFAULT_FONT_SIZE * 2,
        width=SCREEN_WIDTH,
        align="center"
    )

    start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 3
    finish_game_page.text = arcade.Text(
        f"Your dragon reached the Sparkly {iteration_global} times and is very grateful!\n\nPress SPACE or ESCAPE to exit the window.",
        start_x,
        start_y,
        arcade.color.BLACK,
        DEFAULT_FONT_SIZE*0.8,
        multiline = True,
        width = SCREEN_WIDTH,
        align="center"
    )

    finish_game_page.player_sprite = arcade.Sprite("./img/player_small.png")

    return finish_game_page

def main():
    """
    The main game loop which instantiates the window, calls for the first setup, and calls for the Arcade library to run the game.

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
    
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()