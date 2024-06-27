import customtkinter as ctk
from tkinter import *
from Puzzle8 import Puzzle8


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Puzzle-8")
        self.geometry("550*700")

        initial_state = [[1, 4, 3],
                         [2, 0, 7],
                         [6, 5, 8]]
        puzzle = Puzzle8(self, initial_state)

        command_frame = ctk.CTkFrame(self, width=700)
        command_frame.pack(side='right', padx=10, pady=10, expand=True)

        label = ctk.CTkLabel(command_frame, text="Controls", width=200, height=60)
        label.pack(side="top")

        custom_button1 = ctk.CTkButton(command_frame, text="Start Hill Climbing", font=("Arial", 14), width=180,
                                       command=puzzle.solve_hill_climbing_bk)

        custom_button1.pack(side='bottom', fill='y', expand=True, padx=10, pady=10)

        custom_button2 = ctk.CTkButton(command_frame, text="Start Hill Climbing(no bk)", font=("Arial", 14), width=180,
                                       command=puzzle.solve_hill_climbing)

        custom_button2.pack(side='bottom', fill='y', expand=True, padx=10, pady=10)

        custom_button3 = ctk.CTkButton(command_frame, text="Start A*", font=("Arial", 14), width=180,
                                       command=puzzle.solve_puzzle_A)
        custom_button3.pack(side='bottom', fill='y', expand=True, padx=10, pady=10)

        label2 = ctk.CTkLabel(command_frame, text="Solve : ")
        label2.pack(side="bottom")

        custom_button4 = ctk.CTkButton(command_frame, text="Reset", font=("Arial", 14), width=180,
                                       command=puzzle.reset)
        custom_button4.pack(side='bottom', fill='y', expand=True, padx=10, pady=10)

        custom_button5 = ctk.CTkButton(command_frame, text="Randomize", font=("Arial", 14), width=180,
                                       command=puzzle.randomize)
        custom_button5.pack(side='bottom', fill='y', expand=True, padx=10, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
