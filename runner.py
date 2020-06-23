import pygame
import sys
import time

from sudoku import Sudoku, SudokuAI
from settings import *


def main():
    # Initialize pygame and create the window
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Fonts
    BMJAPAN = "assets/fonts/BMjapan.ttf"
    lg_bmjapan_font = pygame.font.Font(BMJAPAN, 42)
    md_bmjapan_font = pygame.font.Font(BMJAPAN, 32)
    regular_font = pygame.font.SysFont("Arial", 24)
    nums_font = pygame.font.SysFont("Arial", 24)

    # Set window title and window icon
    pygame.display.set_caption("SudokuAI")
    icon = pygame.image.load("assets/images/sudoku.png")
    pygame.display.set_icon(icon)

    # Play the music
    if SONG_PATH:
        pygame.mixer.init()
        pygame.mixer.music.load(SONG_PATH)
        pygame.mixer.music.play(-1, 0.0)

    # Show instructions initially
    instructions = True

    game = Sudoku()
    ai = SudokuAI(game.board)


    while True:
        window.fill(WHITE)

        if instructions:
            for event in pygame.event.get():
                # Check if game quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Play game button
            play_btn = draw_btn(
                window,
                (WIDTH / 4, (3 / 4) * HEIGHT),
                (WIDTH / 2, 50),
                BLACK, "Play Game", WHITE,
                md_bmjapan_font
            )

            # Check if play button was clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                game.mouse_pos = pygame.mouse.get_pos()
                if play_btn.collidepoint(game.mouse_pos):
                    instructions = False
                    time.sleep(.3)

            # Render the title
            title = lg_bmjapan_font.render("SudokuAI", True, BLACK)
            titleRect = title.get_rect()
            titleRect.center = (WIDTH / 2, 50)
            window.blit(title, titleRect)

            rules = [
                ["Sudoku is played over a 9x9 grid, divided to", "3x3 sub grids called \"regions\"."],
                ["Sudoku begins with some of the grid cells", "already filled with numbers."],
                ["The object of Sudoku is to fill the other", "empty cells with numbers between 1 and 9."],
                ["A number should appear only once on each", "row, column and a region."],
                ["SudokuAI will make optimal moves for you", "if you get stuck :)"]
            ]

            # Render the rules, segment by segment
            for i, rule in enumerate(rules):
                # Iterate over the segments of the current rule
                for j, rule_seg in enumerate(rule):
                    rule_seg = regular_font.render(rule_seg, True, BLACK)
                    rule_rect = rule_seg.get_rect()
                    rule_rect.center = (WIDTH / 2, 125 + (i * 60) + (j * 25))
                    window.blit(rule_seg, rule_rect)

            # Unpause the music
            pygame.mixer.music.unpause()

        # If the "Play Game" button was clicked
        else:
            # Draw the outline of the board
            board_rect = pygame.draw.rect(
                window, BLACK,
                (
                    BOARD_POS[0], BOARD_POS[1],
                    WIDTH - BOARD_POS[0] * 2, HEIGHT - BOARD_POS[0] * 2
                ), 2
            )

            # If a cell was selected (clicked), highlight the cell
            selected_cell = game.selected_cell
            if selected_cell:
                # Draw a rectancle on the selected cell
                pygame.draw.rect(
                    window,
                    SELECTED_CELL_COLOR,
                    (
                        selected_cell[1] * CELL_SIZE + BOARD_POS[0],
                        selected_cell[0] * CELL_SIZE + BOARD_POS[1],
                        CELL_SIZE, CELL_SIZE
                    )
                )

            # Exit game button
            exit_btn = draw_btn(
                window,
                (BOARD_POS[0] + 15, (BOARD_POS[1] - 50) / 2),
                (WIDTH / 5, 50),
                BLACK, "Exit game", WHITE,
                regular_font
            )

            # AI move button
            ai_btn = draw_btn(
                window,
                (BOARD_POS[0] + BOARD_SIZE / 3 + 15, (BOARD_POS[1] - 50) / 2),
                (WIDTH / 5, 50),
                GREEN, "AI move", BLACK,
                regular_font
            )

            # New game button
            new_btn = draw_btn(
                window,
                (BOARD_POS[0] + BOARD_SIZE / 1.5 + 15, (BOARD_POS[1] - 50) / 2),
                (WIDTH / 5, 50),
                RED, "New game", WHITE,
                regular_font
            )

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                game.mouse_pos = pygame.mouse.get_pos()

                # Check if exit button was clicked
                if exit_btn.collidepoint(game.mouse_pos):
                    instructions = True
                    time.sleep(.2)
                # Check if the "AI move" button was clicked
                elif ai_btn.collidepoint(game.mouse_pos):
                    # Make sure the game is not already over
                    if not ai.is_win(game.board):
                        # Make a move and store the cell where the number was inserted
                        cell = ai.make_move()
                        # If a move was made
                        if cell:
                            # If the game is not won, mark the cell of the inserted number
                            if not game.is_win():
                                # Select the cell that the AI chose
                                game.selected_cell = cell
                                game.mouse_pos = (
                                    BOARD_POS[0] + cell[1] * CELL_SIZE,
                                    BOARD_POS[1] + cell[0] * CELL_SIZE
                                )
                    time.sleep(.2)
                # Check if the "New game" button was clicked
                elif new_btn.collidepoint(game.mouse_pos):
                    game = Sudoku()
                    ai = SudokuAI(game.board)

                # Check if a cell or the left/right/bottom margin
                # (used for deselecting a cell) was clicked
                notop_rect = pygame.Rect(0, BOARD_POS[1], WIDTH, HEIGHT)
                if notop_rect.collidepoint(game.mouse_pos):
                    game.selected_cell = game.get_cell(board_rect)

            for event in pygame.event.get():
                # Check if game quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Check for key press events
                if event.type == pygame.KEYDOWN:
                    # Insert the key on the board if it's a number
                    game.insert_num(window, board_rect, event.unicode)
                    # Update the AI knowledge
                    ai.update_knowledge()

            # Draw the numbers on the board
            draw_nums(window, game, nums_font)

            # Draw the vertical and horizontal lines of the boards
            draw_vh_lines(window)

            # Pause the music
            pygame.mixer.music.pause()

        # Update the window with everything that was drawn
        pygame.display.update()


def draw_vh_lines(window):
    """
    This functionDraws the vertical and horizontal lines of the sudoku board.
    """

    for x in range(9):
        # Draw vertical lines
        pygame.draw.line(
            window, BLACK,
            (BOARD_POS[0] + (x * CELL_SIZE), BOARD_POS[1]),
            (BOARD_POS[0] + (x * CELL_SIZE), BOARD_POS[1] + BOARD_SIZE),
            # The 3rd, 6th and 9th lines are thicker
            1 if x % 3 != 0 else 2
        )

        # Draw horizontal lines
        pygame.draw.line(
            window, BLACK,
            (BOARD_POS[0], BOARD_POS[1] + (x * CELL_SIZE)),
            (BOARD_POS[0] + BOARD_SIZE, BOARD_POS[1] + (x * CELL_SIZE)),
            # The 3rd, 6th and 9th lines are thicker
            1 if x % 3 != 0 else 2
        )


def draw_btn(window, pos, size, btn_color, text, text_color, font):
    """
    This function draws a button on the `window` and returns the button.
        - `pos` is a tuple in which `pos[0]` is the margin from the left
        and `pos[1]` is the margin from the top.
        - `size` is a tuple in which `size[0]` is the width and `size[1]`
        is the height.
    """

    # Create the button
    btn_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
    # Create styled text, get its rectangle and center it inside `btn_rect`
    styled_text = font.render(text, True, text_color)
    styled_text_rect = styled_text.get_rect()
    styled_text_rect.center = btn_rect.center
    # Draw the button and blit the styled text into `styled_text_rect` 
    pygame.draw.rect(window, btn_color, btn_rect)
    window.blit(styled_text, styled_text_rect)

    return btn_rect


def draw_nums(window, game, font):
    """
    This function draws each number of the current board into the
    `window`. `board` is a 2D list that contains the rows of the board.
    Each row contains numbers from 0 to 9, 0 meaning that the
    corresponding cell is empty.
    """

    # Iterate through the rows
    for i, row in enumerate(game.board):
        # Iterate through each number of the row
        for j, num in enumerate(row):
            curr_num = game.board[i][j]

            if curr_num != 0:
                # The background of the cell
                cell_rect = pygame.Rect(
                    j * CELL_SIZE + BOARD_POS[0],
                    i * CELL_SIZE + BOARD_POS[1],
                    CELL_SIZE, CELL_SIZE
                )

                # Render the font and center the number inside `cell_rect`
                styled_text = font.render(str(curr_num), True, BLACK)
                styled_text_rect = styled_text.get_rect()
                styled_text_rect.center = cell_rect.center

                # Draw the background if the cell is an initial cell
                if game.initial_board[i][j] != 0:
                    pygame.draw.rect(window, INITIAL_CELL_COLOR, cell_rect)

                # Draw the number
                window.blit(styled_text, styled_text_rect)

    # Fixes the overlaping of the initial cells on the board's outline
    pygame.draw.rect(
        window, BLACK,
        (
            BOARD_POS[0], BOARD_POS[1],
            WIDTH - BOARD_POS[0] * 2, HEIGHT - BOARD_POS[0] * 2
        ), 2
    )


if __name__ == "__main__":
    main()
