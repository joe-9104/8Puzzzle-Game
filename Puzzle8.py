from customtkinter import *
import time
from queue import PriorityQueue
from tkinter import TclError
import random
import pygame


class Puzzle8:
    def __init__(self, window, initial_state):
        self.state = initial_state
        self.initial_state = [row[:] for row in
                              initial_state]  # Create a deep copy of the initial state to allow resetting later
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # Goal state
        self.window = CTkFrame(window)  # Create a frame inside CustomTkinter window instance
        self.window.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        self.tiles = self.create_tiles()  # Calls the method create_tiles() to create the graphical representation of the puzzle
        self.state_history = [self.state]  # Initialize state_history with the initial state

    def play_audio(self, file_name):
        pygame.mixer.init()
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()

    def reset(self):
        self.state = [row[:] for row in self.initial_state]  # Create a deep copy of the initial state
        self.play_audio("super-mario-bros_reset.mp3")
        for tiles in self.window.winfo_children():
            tiles.destroy()
        self.create_tiles()

    def update(self):
        for tiles in self.window.winfo_children():
            tiles.destroy()
        self.create_tiles()

    def move_tile(self, i, j):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Defines the possible movement directions
        for dx, dy in directions:
            x, y = i + dx, j + dy
            if x >= 0 and x < 3 and y >= 0 and y < 3 and self.state[x][y] == 0:
                self.state[x][y], self.state[i][j] = self.state[i][j], self.state[x][y]
                # Attempts to move a tile at position (i, j) to an adjacent empty position
                # and swaps if an empty position is found.
                for tiles in self.window.winfo_children():
                    tiles.destroy()
                self.create_tiles()  # Updates the graphical representation after moving a tile
                break

    def print_state(self):
        for row in self.state:
            print(row)

    def generate_neighbors(self, state):
        neighbors = []
        zero_row, zero_col = self.find_zero_position(state)
        for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            # For each direction, calculates the new position of the empty tile
            new_row, new_col = zero_row + i, zero_col + j
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = [row[:] for row in state]  # Create a deep copy
                new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], \
                    new_state[zero_row][zero_col]
                neighbors.append(new_state)
        return neighbors

    def find_zero_position(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j
        return None

    def compare_to_goal(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != self.goal_state[i][j]:
                    return False
        return True

    def create_tiles(self, color="#08639c"):
        # Clear any existing tiles
        for widget in self.window.winfo_children():
            widget.destroy()  # Ensure the window is cleared

        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                if self.state[i][j] == 0:
                    # Represent the blank space with a placeholder (could be a blank space or empty Frame)
                    placeholder = CTkFrame(self.window, width=100, height=100)  # Optional: create a blank area
                    placeholder.grid(row=i, column=j, padx=5, pady=5)
                    row.append(None)  # No button for the blank space
                else:
                    # Determine the background color
                    if self.compare_to_goal():
                        bg_color = "green"
                        self.play_audio("Super Mario Bros. Music - Level Complete.mp3")
                    else:
                        bg_color = color

                    # Create a button for non-zero tiles
                    tile = CTkButton(
                        self.window,
                        text=str(self.state[i][j]),
                        width=100,
                        height=100,
                        font=("Arial", 22),
                        fg_color=bg_color,
                        command=lambda i=i, j=j: self.move_tile(i, j)
                    )
                    tile.grid(row=i, column=j, padx=5, pady=5)
                    row.append(tile)
            tiles.append(row)
        return tiles

    def solve_hill_climbing(self):
        current_state = self.state
        start_time = time.time()
        nb_iter = 0

        while self.state != self.goal_state:
            nb_iter += 1
            self.window.update_idletasks()
            self.window.update()
            time.sleep(0.5)  # delay for visualization

            neighbors = self.generate_neighbors(current_state)
            best_neighbor = min(neighbors, key=lambda x: self.h(x))

            if self.h(best_neighbor) >= self.h(current_state):
                self.create_tiles("red")
                self.play_audio("super-mario-death-sound-sound-effect.mp3")
                print("no best neighbours")
                end_time = time.time()
                print(f"solved in {nb_iter} move(s)")
                print(f"solved in {end_time - start_time - 0.5 * nb_iter} seconds")
                return None  # No better neighbor found, return None

            if best_neighbor == self.goal_state:
                current_state == self.goal_state
                return  # Path found

            # Find the position of the empty tile (0) in the best neighbor
            zero_row, zero_col = self.find_zero_position(best_neighbor)

            # Move the tile in the GUI
            self.move_tile(zero_row, zero_col)

            current_state = best_neighbor

    def solve_hill_climbing_bk(self):
        current_state = self.state
        start_time = time.time()  # Start the timer
        iteration_count = 0
        stack = []  # Use a stack to keep track of states for backtracking
        visited_states = set()  # Keep track of visited states

        while self.state != self.goal_state:
            self.window.update_idletasks()
            self.window.update()
            iteration_count += 1
            time.sleep(0.5)  # delay for visualization

            neighbors = self.generate_neighbors(current_state)
            unvisited_neighbors = [state for state in neighbors if str(state) not in visited_states]

            if not unvisited_neighbors and not stack:
                self.create_tiles("red")
                self.play_audio("super-mario-death-sound-sound-effect.mp3")
                end_time = time.time()
                print("no best neighbours")
                print(f"solved in {iteration_count} move(s)")
                print(f"solved in {end_time - start_time - 0.5 * iteration_count} seconds")
                return None  # No better neighbor found, return None

            if unvisited_neighbors:
                best_neighbor = min(unvisited_neighbors, key=lambda x: self.h(x))
                visited_states.add(str(best_neighbor))  # Add the best neighbor to visited states
            else:
                best_neighbor = stack.pop()  # Backtrack to the last state in the stack

            if best_neighbor == self.goal_state:
                current_state = self.goal_state
                self.state = current_state
                end_time = time.time()
                print(f"solved in {iteration_count} move(s)")
                temps = end_time - start_time - 0.5 * iteration_count
                print(f"solved in {temps} seconds")
                self.create_tiles()
                return  # Path found

            # Find the position of the empty tile (0) in the best neighbor
            zero_row, zero_col = self.find_zero_position(best_neighbor)

            # Move the tile in the GUI
            self.move_tile(zero_row, zero_col)

            # Add the current state to the stack before moving to the best neighbor
            stack.append(current_state)
            current_state = best_neighbor

    def h(self, state):
        # Heuristic function: Manhattan distance: la somme de la distance horizontale et la distance verticale
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:
                    value = state[i][j]
                    goal_row, goal_col = (value - 1) // 3, (value - 1) % 3
                    distance += abs(i - goal_row) + abs(j - goal_col)
        return distance

    def a_star(self):
        start_time = time.time()
        nb_iteration = 0
        frontier = PriorityQueue()  #ouvert
        start_state_tuple = tuple(map(tuple, self.state))  # Convert initial state to tuple
        frontier.put((0, start_state_tuple))
        came_from = {}
        cost_so_far = {start_state_tuple: 0}

        while not frontier.empty():
            nb_iteration += 1
            current_cost, current_state_tuple = frontier.get()
            current_state = [list(row) for row in current_state_tuple]  # Convert tuple back to list

            if current_state == self.goal_state:
                path = self.reconstruct_path(came_from, current_state_tuple)
                end_time = time.time()
                return path, end_time - start_time, nb_iteration

            for next_state in self.generate_neighbors(current_state):
                next_state_tuple = tuple(map(tuple, next_state))
                new_cost = cost_so_far[current_state_tuple] + 1
                if next_state_tuple not in cost_so_far or new_cost < cost_so_far[next_state_tuple]:
                    cost_so_far[next_state_tuple] = new_cost
                    priority = new_cost + self.h(next_state)
                    frontier.put((priority, next_state_tuple))
                    came_from[next_state_tuple] = current_state_tuple

        return None, 0, 0

    def reconstruct_path(self, came_from, current_state_tuple):
        path = []
        while current_state_tuple in came_from:
            path.append(current_state_tuple)
            current_state_tuple = came_from[current_state_tuple]
        path.reverse()
        return path

    def solve_puzzle_A(self):
        #self.state = [row[:] for row in self.initial_state]  # Create a deep copy of the initial state
        path, duration, iterations = self.a_star()

        if path is None:
            self.play_audio("super-mario-death-sound-sound-effect.mp3")
            self.create_tiles("red")
            print("No solution found.")
            return

        print(f"Solved in {duration} seconds.")
        nb_moves = 0
        for state_tuple in path:
            nb_moves += 1
            self.state = [list(row) for row in state_tuple]
            self.update()
            self.window.update_idletasks()
            self.window.update()
            time.sleep(0.5)
        print(f"Solved in {nb_moves} move(s).")

    def is_goal_state(self, state):
        return state == self.goal_state

    def randomize(self):  # creates a random initial state for the 8-puzzle game
        board = []
        numbers = list(range(1, 9)) + [0]
        random.shuffle(numbers)
        # Shuffles the numbers list to create a random arrangement of the puzzle tiles.
        # This ensures that the initial state generated is different each time.
        self.play_audio("super-mario-bros_randomize.mp3")
        for i in range(3):
            row = []
            for j in range(3):
                tile_number = numbers[i * 3 + j]
                row.append(tile_number)
            board.append(row)
        self.state = board
        print(self.state)
        self.create_tiles()
