import copy
import random

from settings import *


class Sudoku():
    """
    Sudoku game representation
    """

    def __init__(self):

        self.board = self.new_board()
        self.initial_board = copy.deepcopy(self.board)
        self.selected_cell = None
        self.mouse_pos = (0, 0)

    def new_board(self):
        """
        """

        return copy.deepcopy(board)

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
                (self.mouse_pos[1] - BOARD_POS[1]) // CELL_SIZE,
                (self.mouse_pos[0] - BOARD_POS[0]) // CELL_SIZE
            )

        return False

    def insert_num(self, window, board_rect, key):
        """
        This method checks if the pressed key is a number, and if so,
        the number will be inserted in the selected cell.
        """

        # Get the click cell position (e.g: `(8, 8)` is the last cell)
        i, j = self.get_cell(board_rect)

        # Check if the `(i, j)` is a valid board position
        if self.initial_board[i][j] == 0:
            # If the key is a number, add it to the board
            try:
                int(key)
                self.board[i][j] = int(key)
                # Check for a win
                self.is_win()
            except:
                pass
    
    def is_win(self):
        """
        This method checks if the current state of the board represents
        a win. If it's a win, "lock" the board
        """

        # Iterate through each row of the board
        for i, row in enumerate(self.board):
            # The `i`-th column
            col = [row2[i] for row2 in self.board]

            # Check if the `i`-th row and column are valid
            if not (set(row) == set(col) == set(range(1, 10))):
                return False

        # Mark the victory by "locking" every cell
        self.initial_board = self.board
        return True


class SudokuAI():
    """
    Sudoku game player
    """

    def __init__(self, board):

        self.board = board
        # A dictionary that has pairs of a cell mapping to a set of
        # possible numbers in that cell (e.g: `(1, 4): {1, 2, 9}`)
        self.knowledge = {}
        # When a SudokuAI object is created, initial knowledge
        # will be created
        self.update_knowledge()

    def update_knowledge(self, board=None, knowledge=None):
        """
        Updates the knowledge of 1 or more cells by reducing the number of
        valid numbers that can be inserted in the specfic cell. The optional
        arguments `board` and `knowledge` are used when the live board and
        knowledge musn't be updated (while using the `get_safe_move` method). 
        """

        board = board if board else self.board
        knowledge = knowledge if knowledge else self.knowledge

        # Iterate through the rows of the board
        for i, row in enumerate(board):
            # Iterate through each number of the row
            for j, num in enumerate(row):
                # Add knowledge only to the empty cells
                if board[i][j] == 0:
                    cell = (i, j)
                    knowledge[cell] = self.possible_nums(cell, board)

    def possible_nums(self, cell, board):
        """
        This method returns a set of possible numbers that can be inserted
        in `cell` on the specified `board`.
        """

        i, j = cell
        # A set of the numbers in the row where `cell` is
        row = set(board[i])
        # A set of the numbers in the column where `cell` is
        col = set(row[j] for row in board)
        # The position of the first cell of the region where `cell` is
        ri, rj = ((i // 3) * 3, (j // 3) * 3)
        # A set of the numbers in the region where `cell` is
        reg = set(
            num for row in board[ri:ri+3]
            for num in row[rj:rj+3]
        )

        # A set of the numbers that can't be inserted in `cell`
        not_available_nums = row.union(col.union(reg))
        not_available_nums.remove(0)

        return set(range(1, 10)).difference(not_available_nums)

    def is_win(self, board=None):
        """
        This method checks if the current state of the board represents
        a win. The optional argument `board` is used when the live board
        musn't be updated.
        """

        board = board if board else self.board

        # Iterate through each row of the board
        for i, row in enumerate(board):
            # The `i`-th column
            col = [row2[i] for row2 in board]

            # Check if the `i`-th row and column are valid
            if not (set(row) == set(col) == set(range(1, 10))):
                return False

        return True

    def is_board_valid(self, board, knowledge):
        """
        This method return `True` if the board is valid, `False` otherwise
        The board is invalid if:
            1) There are at least 2 identical numbers in the same row,
            column or region or
            2) There are empty cells on the board that don't have any possible
            numbers to insert into them (there is no knowledge about).
        """

        # Iterate through each row of the board
        for i, row in enumerate(board):
            # If an empty cell has no knowledge associated with the cell
            for j, num in enumerate(row):
                cell = (i, j)
                if num == 0 and len(knowledge[cell]) == 0:
                    return False

            # The numbers of the i-th row (without 0s)
            row = [num for num in row if num]
            # The numbers of the i-th column (without 0s)
            col = [row2[i] for row2 in board if row2[i]]
            # The numbers of the i-th region (without 0s)
            ri, rj = (i * 3, (i // 3) * 3)
            reg = [
                num for row2 in self.board[ri:ri+3]
                for num in row2[rj:rj+3] if num
            ]

            # If a number was repeated in a row, column or region
            if len(row) != len(set(row)) or \
               len(col) != len(set(col)) or \
               len(reg) != len(set(reg)):
                return False

        return True

    def make_move(self):
        """
        This method makes a safe move and returns the cell in which a
        number was inserted. Two kinds of moves can be made.
            1) A simple safe move that consists of a cell that has only
            one possible number or
            2) A more complex move that involves picking random numbers
            until a win is achieved.
        """

        # A list of cells with 1 possible number
        safe_cells = [
            cell for cell in self.knowledge
            if len(self.knowledge[cell]) == 1
        ]

        # If 1 or more safe moves are available
        if safe_cells:
            # Get a safe cell and insert its number there
            safe_cell = i, j = random.choice(safe_cells)
            self.board[i][j] = self.knowledge[safe_cell].pop()
            # Update the knowledge because more safe moves can be infered
            self.update_knowledge()
            # Return the safe cell so it can be highlighted on the board
            return safe_cell
        # If no safe moves are available
        else:
            # Create a copy of the current game's board and knowledge
            # that can be used for experimenting with random moves
            board_cpy = copy.deepcopy(self.board)
            knowledge_cpy = copy.deepcopy(self.knowledge)
            # Get a safe cell and insert its number there
            safe_cell, safe_num = self.get_safe_move(board_cpy, knowledge_cpy)
            i, j = safe_cell
            self.board[i][j] = safe_num
            self.knowledge[safe_cell] = set()
            # Update the knowledge because more safe moves can be infered
            self.update_knowledge()
            # Return the safe cell so it can be highlighted on the board
            return safe_cell

    def get_safe_move(self, board, knowledge, guess=None):
        """
        This is a recursive function that creates different paths by
        choosing random numbers.
        It's used when there are no simple safe moves left. It can return:
            1) `False` if a win state was not detected on the path or
            2) A tuple that consists of a cell and the safe number to
            insert into that cell if a win state was found.
        """

        # A list of cells with 1 possible number
        safe_cells = [
            cell for cell in knowledge
            if len(knowledge[cell]) == 1
        ]

        # Iterate through the safe cells
        while safe_cells:
            # Make sure the board is valid, since any previous random
            # moves might be wrong
            if self.is_board_valid(board, knowledge):
                # Get a safe cell and insert its number there
                safe_cell = i, j = random.choice(safe_cells)
                board[i][j] = knowledge[safe_cell].pop()
                # Update the knowledge because more safe moves can be infered
                self.update_knowledge(board, knowledge)
                
                # Get a list of new safe cells
                safe_cells = [
                    cell for cell in knowledge
                    if len(knowledge[cell]) == 1
                ]
            else:
                return False

        # Return a safe (previously random) cell and its number
        if self.is_win(board):
            return guess

        # If the board is still valid after the last safe move made
        if self.is_board_valid(board, knowledge):
            # Get the cells with the smallest amount of possible numbers
            # that a cell on the current board can have
            min_num = min(
                len(nums) for nums in knowledge.values()
                if len(nums)
            )
            best_moves = [
                cell for cell in knowledge
                if len(knowledge[cell]) == min_num
            ]

            # Get a random cell with the minimum number of possible numbers
            rand_cell = i, j = random.choice(best_moves)

            # Iterate through each of the `rand_cell`'s possible numbers
            for num in knowledge[rand_cell]:
                # Create a copy of the current board and knowledge
                new_board = copy.deepcopy(board)
                new_knowledge = copy.deepcopy(knowledge)
                # Insert the current number on new board and update the new knowledge
                new_board[i][j] = num
                new_knowledge[rand_cell] = set()
                self.update_knowledge(new_board, new_knowledge)
                # Try to get a safe move of the new board and knowledge
                result = self.get_safe_move(new_board, new_knowledge, (rand_cell, num))

                # If the returned result is a tuple return the result
                if type(result) == tuple:
                    return result
        else:
            return False
