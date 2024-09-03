# 8 Puzzle Game

## Description

This project implements the classic "8 puzzle" game using Python and the `CustomTkinter` graphics library.
The game consists of a 3x3 grid containing eight tiles numbered 1 to 8 and one empty space.
The objective is to move the tiles to arrange them in numerical order using the empty space.

The project includes several features:
1. **Grid Creation and Display**: The grid is graphically displayed with numbered tiles, and tiles can be moved by clicking on them.
2. **Dynamic Display Update**: Each tile move updates the grid display.
3. **Automatic Solving**: The project implements two automatic solving algorithms:
   - **Hill Climbing**: A local search algorithm that attempts to minimize the number of misplaced tiles at each step.
   - **A*** **(A Star)**: An optimal pathfinding algorithm using Manhattan distance as a heuristic to find the shortest solution.
4. **Move Visualization**: The solving algorithms visually show each tile movement until the solution is found.
5. **Success and Failure Indication**: Tiles change color to indicate if the grid is solved (green) or if the algorithm fails to find a better solution (red), playing the appropriate soundtrack.

Take in consideration that the MP3 files have been ignored to keep the repository clean.

To run the project, ensure you have installed the necessary dependencies mentionned below and launch the main file `ui.py`, which handles the user interface. `Puzzle8.py` handles the game logic.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/joe-9104/8Puzzle-game.git
   cd 8Puzzle-game
   ```
2. Make sure you have Python 3.12 or a newer version installed
3. Install the required libraries:
   ```
   > pip install customtkinter
   > pip install pygame
   > pip install numpy
   ```

## Usage

To start the game, run the following command:
```bash
python Puzzle8.py
```
The game window will open, displaying the 8 puzzle grid.
You can click on the tiles to move them and attempt to solve the puzzle manually.
Alternatively, you can use the implemented algorithms to solve the puzzle automatically.
The algorithms will visualize each move and indicate the success or failure of the solution.
