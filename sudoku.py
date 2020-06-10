import pygame
import sys

from settings import *

class Sudoku():
    """
    Sudoku game representation
    """

    def __init__(self):

        pygame.init()

        # Set window title and window icon
        pygame.display.set_caption("SudokuAI")
        icon = pygame.image.load("sudoku.png")
        pygame.display.set_icon(icon)

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.board = test_board
        print(self.board)


    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
        pygame.quit()
        # sys.exit()

    def events(self):
        # Check if game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        pass

    def draw(self):
        self.window.fill(WHITE)
        self.draw_grid(self.window)
        pygame.display.update()

    def draw_grid(self, window):
        pygame.draw.rect(
            window,
            BLACK,
            (
                board_pos["x"],
                board_pos["y"],
                WIDTH - 150,
                HEIGHT - 150 
            ), 2
        )

        for x in range(9):
            pygame.draw.line(
                window,
                BLACK,
                (board_pos["x"] + (x * cell_size), board_pos["y"]),
                (board_pos["x"] + (x * cell_size), board_pos["y"] + 450),
                1 if x % 3 != 0 else 2
            )

            pygame.draw.line(
                window,
                BLACK,
                (board_pos["x"], board_pos["y"] + (x * cell_size)),
                (board_pos["x"] + 450, board_pos["y"] + (x * cell_size)),
                1 if x % 3 != 0 else 2
            )


