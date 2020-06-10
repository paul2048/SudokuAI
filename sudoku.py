from settings import *

class Sudoku():
    """
    Sudoku game representation
    """

    def __init__(self):

        self.board = test_board
        self.selected_cell = None
        self.mouse_pos = None

    # def run(self):
    #     """
    #     This will be the first called method after the `runner.py` was executed.
    #     While the program is running:
    #         - check if events took place (e.g: clicks)
    #         - get the position of the mouse
    #         ...
    #     """


    # def events(self):
    #     """

    #     """

    
    # def update(self):
    #     """

    #     """


    # def draw(self):
    #     """
        
    #     """


    # def draw_board(self, window):
    #     """
    #     This method will draw the board; first the vertical lines,
    #     then the horizontal lines. Each pair of 9 cells will be
    #     contained within thicker lines.
    #     """

    #     # Draw the outline of the board
    #     # pygame.draw.rect(window, BLACK, (BOARD_POS[0], BOARD_POS[1], WIDTH - 150, HEIGHT - 150), 2)


    # def draw_selection(self, window, pos):
    #     """
    #     This function draws a rectancle on a cell of the board.
    #     It has the purpose of highlighting the selected cell.
    #     """
    

    def get_cell(self, board_rect):
        """
        If the mouse was clicked outside the board, the method returns
        `False`, else it returns the position of the clicked cell (e.g:
        `(8, 8)` will be returned for clicking the last cell). `board_rect`
        is a pygame `Rect` with the size and position of the board.
        """

        # If the clicked coordonates are inside the board
        if board_rect.collidepoint(self.mouse_pos):
            # Return the position of the clicked cell
            return (
                (self.mouse_pos[0] - BOARD_POS[0]) // CELL_SIZE,
                (self.mouse_pos[1] - BOARD_POS[1]) // CELL_SIZE
            )

        return False
