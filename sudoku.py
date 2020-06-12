from settings import *

class Sudoku():
    """
    Sudoku game representation
    """

    def __init__(self):

        self.board = test_board
        self.selected_cell = None
        self.mouse_pos = None

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

    def draw_nums(self, window, font):
        """
        This function draws each number of the `board` into the `window`.
        `board` is a 2D list containing the rows of the board.
        Each row contain numbers from 0 to 9, 0 meaning that the
        corresponding cell is empty.
        """

        # Iterate through the rows
        for i, row in enumerate(self.board):
            # Iterate through each number of the row
            for j, num in enumerate(row):
                curr_num = str(self.board[i][j])

                if curr_num != "0":
                    # Render the font and center the number in the corresponding cell
                    styled_text = font.render(curr_num, True, BLACK)
                    styled_text_rect = styled_text.get_rect()
                    styled_text_rect.center = (
                        i * CELL_SIZE + BOARD_POS[0] + CELL_SIZE / 2,
                        j * CELL_SIZE + BOARD_POS[1] + CELL_SIZE / 2
                    )

                    # Draw the number
                    window.blit(styled_text, styled_text_rect)
