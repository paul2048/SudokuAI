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
        self.selected_cell = None
        self.mouse_pos = None
        self.state = "playing"

    def run(self):
        """
        This will be the first called method after the `runner.py` was executed.
        While the program is running:
            - check if events took place (e.g: clicks)
            - get the position of the mouse
            ...
        """

        while self.running:
            self.events()
            self.update()
            self.draw()

        pygame.quit()
        # sys.exit()

    def events(self):
        """

        """

        # Check if game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # self.update()
                self.selected_cell = self.mouse_on_board()
    
    def update(self):
        """

        """

        self.mouse_pos = pygame.mouse.get_pos()

    def draw(self):
        """
        
        """

        self.window.fill(WHITE)
        self.draw_board(self.window)

        if self.selected_cell:
            self.draw_selection(self.window, self.selected_cell)
        pygame.display.update()

    def draw_board(self, window):
        """
        This method will draw the board; first the vertical lines,
        then the horizontal lines. Each pair of 9 cells will be
        contained within thicker lines.
        """

        # Draw the outline of the board
        # pygame.draw.rect(window, BLACK, (board_pos[0], board_pos[1], WIDTH - 150, HEIGHT - 150), 2)

        for x in range(10):
            # Draw vertical lines
            pygame.draw.line(
                window,
                BLACK,
                (board_pos[0] + (x * cell_size), board_pos[1]),
                (board_pos[0] + (x * cell_size), board_pos[1] + board_size),
                # The 3rd, 6th and 9th lines are thicker
                1 if x % 3 != 0 else 2
            )

            # Draw horizontal lines
            pygame.draw.line(
                window,
                BLACK,
                (board_pos[0], board_pos[1] + (x * cell_size)),
                (board_pos[0] + board_size, board_pos[1] + (x * cell_size)),
                # The 3rd, 6th and 9th lines are thicker
                1 if x % 3 != 0 else 2
            )

    def draw_selection(self, window, pos):
        """
        This function draws a rectancle on a cell of the board.
        It has the purpose of highlighting the selected cell.
        """

        pygame.draw.rect(
            window,
            LIGHTPURPLE,
            (
                pos[0] * cell_size + board_pos[0] + 1,
                pos[1] * cell_size + board_pos[1] + 1,
                cell_size - 1,
                cell_size - 1
            )
        )

    def mouse_on_board(self):
        """
        If the mouse was clicked outside the board, the method returns
        `False`, else it returns the position of the clicked cell
        (e.g: `(8, 8)` will be returned for clicking the last cell).
        """

        # If the clicked coordonates are outside of the board
        if (self.mouse_pos[0] < board_pos[0] or
                self.mouse_pos[1] < board_pos[1] or
                self.mouse_pos[0] > board_pos[0] + board_size or
                self.mouse_pos[1] > board_pos[1] + board_size):
            return False

        # Return the position of the clicked cell
        return (
            (self.mouse_pos[0] - board_pos[0]) // cell_size,
            (self.mouse_pos[1] - board_pos[1]) // cell_size
        )
