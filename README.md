# Automaze
*A simple maze video game with procedurally-generated levels and automatic difficulty adjustment per player performance*

This was my final project of the 12-week SPICED data science bootcamp, completed in 10 person days by me and presented 19 May 2023. It was entirely my own design from concept through project/sprint plan, programming, and testing. Many thanks to my instructors, classmates, friends, and other first playtesters who gave feedback and were the best rubber ducks a mewling engineer could hope for!

To run, check that you have pip installed the packages listed in requirements.txt and then run main.py.

## Modules
This repository contains:

├── config.py  
├── img  
│   ├── background.png  
│   ├── colosseum.png  
│   ├── player.png  
│   └── player_small.png  
├── level_generator.py  
├── LICENSE  
├── main.py  
├── player_stats  
├── README.md  
├── requirements.txt  
├── rooms.py  
├── sprites.py  
└── variables.ipynb  

Of note are the following:
- **main.py** contains the main game loop, tying together all other modules, managing keypress events, triggering new level generation, and recording player performance
- **level_generator.py** is the backend file where maze levels are randomly generated (as 2D NumPy arrays) and validated for playability and difficulty
- **config.py** manages basic features like window size, font size, and the key for difficulty setting
- **rooms.py** and **sprites.py** are simple modules each containing a single class
- All images are located in the **img** directory
- The **player_stats** directory is intentionally left blank, it is populated with player performance .csv as the game is played
- **variables.ipynb** is a byproduct of my dev process and contains a list of every variable used in each of the Python modules and what they do; it is in addition to doc strings in the Python modules

## Design and Implementation
The objective was to create a basic maze video game with multiple levels, each to be bordered by and containing randomly generated walls, a start point, and goal point. Each maze was to be auto-/procedurally generated, must be playable (possible to reach the goal point from the start point), and should be appropriate for the player's current difficulty setting. The player controls their sprite with simple arrow keys.

As part of level auto-generation, a minimum number of steps (MNS, the minimum number of moves required to reach the goal point from the start point) is calculated using the A* pathfinding algorithm. MNS is a proxy for level difficulty -- the higher the MNS, the higher the difficulty. The number of steps the player takes to reach the goal (PNS) is recorded as the player navigates through the maze and the difference between MNS and PNS is used to automatically adjust the difficulty setting.
- If PNS is >= 5 higher than MNS, the game automatically decreases the difficulty setting so the next maze has a lower MNS and is easier to complete.
- If PNS is <= 2 higher than MNS, the game automatically increases the difficulty setting so the next maze has a higher MNS and is more difficult to complete.

### Level Process
1. Level auto-generated
2. Level pathfinder run:
    a. If path not found, return to 1
    b. If path found, does MNS fall within desired difficulty level? If not, return to 1, if so continue to 3
3. Art mapped to level and displayed to player
4. Player runs level; once completed, cf. MNS with PNS; if beyond threshold (TBD), increase or decrease difficulty as appropriate
5. Repeat

### Production
- Prepare game design
- Write pathfinder
- Design level auto-generator; randomize inner walls, ensure path possible, calculate MNS and validate difficulty level
- Combine and test full level generation backend functions, test for stability
- Auto-generate ca. 100 levels and record MNS, run EDA (poss. standardize) and divide range into 5 to represent difficulty
- Design frontend pygame classes and program to ensure background art mapped, player sprite controllable and main game loop functions
- Adjust main program to include auto-generator, pathfinder, and difficulty
- Pre-prod testing

## Next
I really enjoyed making this and there are a lot of fun directions I could take it, these are the things I'd like to look into sometime (on no particular timeline, simply to tinker with on occasion):
- I want to add time spent in a maze as a factor in player performance, so that the longer spent in a maze, the worse the performance, to discourage players from fully planning out their moves before taking a step
- Currently, the player performance dataframe is printed to a simple .csv and stored locally on escape, I very much want to host this as a web app and connect it to a postgreSQL database and set up a simple dashboard on player preferences, when they stop playing, how good they become, etc.
- Having 2 enemies on an approach vector were part of my original project sketch but became very difficult to program simply because of how they impact the pathfinding function (LevelGenerator.find_path), so sounds like a fun puzzle for me to figure out
- To make it more interesting, I want to provide more difficult levels perhaps with more inner walls to make the path more difficult; the downside is that level generation will then take longer, so I want to experiment with saving unplayed level arrays with a path (e.g. those which are of the wrong difficulty for the player's immediate setting) so the game can index and iterate through those first before generating new ones, in particular as levels become more difficult
- Look and feel can be improved on, with different graphics to mix up the UX (e.g. a forest, a desert, etc.), music and general flash, the player sprite turning in the direction it's moved, basic animation
