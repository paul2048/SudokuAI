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
    sm_bmjapan_font = pygame.font.Font(BMJAPAN, 24)
    md_regular_font = pygame.font.SysFont("Arial", 24)
    sm_regular_font = pygame.font.SysFont("Arial", 19)
    nums_font = pygame.font.SysFont("Arial", 24)

    # Set window title and window icon
    pygame.display.set_caption("SudokuAI")
    icon = pygame.image.load("assets/images/sudoku.png")
    pygame.display.set_icon(icon)

    # Buttons used for dark and light modes
    SUN = pygame.image.load("assets/images/sun.png")
    MOON = pygame.image.load("assets/images/moon.png")
    MODE_BTN_POS = (32, 32)

    # Play the music
    if SONG:
        pygame.mixer.init()
        pygame.mixer.music.load(SONG)
        pygame.mixer.music.play(-1, 0.0)

    # Show instructions initially
    instructions = True

    game = Sudoku()
    ai = SudokuAI(game.board)


    while True:
        window.fill(THEME_COLOR_1)

        if instructions:
            for event in pygame.event.get():
                # Check if game quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Play game button
            play_btn = draw_btn(
                window,
                (WIDTH / 4, HEIGHT - 75),
                (WIDTH / 2, 50),
                THEME_COLOR_2, "Play Game", THEME_COLOR_1,
                md_bmjapan_font
            )

            # The horizontal center of the medium mode button
            medium_btn_center = play_btn.center[0] - (WIDTH / 5) / 2

            easy_mode_btn = draw_btn(
                window,
                (medium_btn_center - 150, HEIGHT - 150),
                (WIDTH / 5, 50),
                DARK_SLATE_GRAY if game.difficulty == 1 else THEME_COLOR_2,
                "Easy", THEME_COLOR_1, sm_bmjapan_font
            )

            medium_mode_btn = draw_btn(
                window,
                (medium_btn_center, HEIGHT - 150),
                (WIDTH / 5, 50),
                DARK_SLATE_GRAY if game.difficulty == 2 else THEME_COLOR_2,
                "Medium", THEME_COLOR_1, sm_bmjapan_font
            )

            hard_mode_btn = draw_btn(
                window,
                (medium_btn_center + 150, HEIGHT - 150),
                (WIDTH / 5, 50),
                DARK_SLATE_GRAY if game.difficulty == 3 else THEME_COLOR_2,
                "Hard", THEME_COLOR_1, sm_bmjapan_font
            )

            # Changing difficulty warning
            warn_msg = "Warning! Changing the difficulty will delete your progress."
            warn = sm_regular_font.render(warn_msg, True, RED)
            warn_rect = warn.get_rect()
            warn_rect.center = (WIDTH / 2, HEIGHT - 175)
            window.blit(warn, warn_rect)


            # Render the title
            title = lg_bmjapan_font.render("SudokuAI", True, THEME_COLOR_2)
            title_rect = title.get_rect()
            title_rect.center = (WIDTH / 2, 50)
            window.blit(title, title_rect)

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
                    rule_seg = md_regular_font.render(rule_seg, True, THEME_COLOR_2)
                    rule_rect = rule_seg.get_rect()
                    rule_rect.center = (WIDTH / 2, 125 + (i * 60) + (j * 25))
                    window.blit(rule_seg, rule_rect)

            # Disply the moon/sun image (turn on/off the dark mode)
            if DARK_MODE:
                dark_mode_btn = window.blit(SUN, MODE_BTN_POS)
            else:
                dark_mode_btn = window.blit(MOON, MODE_BTN_POS)

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                game.mouse_pos = pygame.mouse.get_pos()
                # Check if play button was clicked
                if play_btn.collidepoint(game.mouse_pos):
                    instructions = False
                    time.sleep(.3)

                # If one of difficulty buttons was clicked. Make sure to
                # not create a a new game if the difficulty wasn't changed.
                elif easy_mode_btn.collidepoint(game.mouse_pos):
                    if game.difficulty != 1:
                        game = Sudoku(difficulty=1)
                        ai = SudokuAI(game.board)
                elif medium_mode_btn.collidepoint(game.mouse_pos):
                    if game.difficulty != 2:
                        game = Sudoku(difficulty=2)
                        ai = SudokuAI(game.board)
                elif hard_mode_btn.collidepoint(game.mouse_pos):
                    if game.difficulty != 3:
                        game = Sudoku(difficulty=3)
                        ai = SudokuAI(game.board)

                # If the moon/sun was clicked
                elif dark_mode_btn.collidepoint(game.mouse_pos):
                    toggle_theme()
                    time.sleep(.2)

            # Unpause the music
            pygame.mixer.music.unpause()

        # If the "Play Game" button was clicked
        else:
            # Draw the outline of the board
            board_rect = pygame.draw.rect(
                window, THEME_COLOR_2,
                (
                    BOARD_POS[0], BOARD_POS[1],
                    WIDTH - BOARD_POS[0] * 2, HEIGHT - BOARD_POS[0] * 2
                ), 2
            )

            # If the AI found no solutions
            if ai.no_solutions:
                # Highlight all the mutable cells as wrong
                draw_wrong(window, game)

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
                THEME_COLOR_2, "Exit game", THEME_COLOR_1,
                md_regular_font
            )

            # AI move button
            ai_btn = draw_btn(
                window,
                (BOARD_POS[0] + BOARD_SIZE / 3 + 15, (BOARD_POS[1] - 50) / 2),
                (WIDTH / 5, 50),
                GREEN, "AI move", BLACK,
                md_regular_font
            )

            # New game button
            new_btn = draw_btn(
                window,
                (BOARD_POS[0] + BOARD_SIZE / 1.5 + 15, (BOARD_POS[1] - 50) / 2),
                (WIDTH / 5, 50),
                RED, "New game", THEME_COLOR_1,
                md_regular_font
            )

            # Click events for the buttons
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
                    if not ai.is_win():
                        # Try to make a safe move
                        cell = ai.make_move()
                        # If a safe move exists
                        if cell:
                            if not game.is_win():
                                # Mark the cell of the inserted number
                                game.selected_cell = cell
                                game.mouse_pos = (
                                    BOARD_POS[0] + cell[1] * CELL_SIZE,
                                    BOARD_POS[1] + cell[0] * CELL_SIZE
                                )
                        # If the board doesn't have any solutions or the user
                        # inserted a wrong value into a cell
                        else:
                            # Put the board in a "no solutions" state
                            ai.no_solutions = True
                            game.selected_cell = None

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
                    # Make sure a cell is selected before inserting
                    if board_rect.collidepoint(game.mouse_pos):
                        # Get the board out of the "no solutions" state
                        ai.no_solutions = False
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
    This function draws the vertical and horizontal lines of the sudoku board.
    """

    for x in range(9):
        # Draw vertical lines
        pygame.draw.line(
            window, THEME_COLOR_2,
            (BOARD_POS[0] + (x * CELL_SIZE), BOARD_POS[1]),
            (BOARD_POS[0] + (x * CELL_SIZE), BOARD_POS[1] + BOARD_SIZE),
            # The 3rd, 6th and 9th lines are thicker
            1 if x % 3 != 0 else 3
        )

        # Draw horizontal lines
        pygame.draw.line(
            window, THEME_COLOR_2,
            (BOARD_POS[0], BOARD_POS[1] + (x * CELL_SIZE)),
            (BOARD_POS[0] + BOARD_SIZE, BOARD_POS[1] + (x * CELL_SIZE)),
            # The 3rd, 6th and 9th lines are thicker
            1 if x % 3 != 0 else 3
        )

def draw_wrong(window, game):
    """
    This function highlights all the mutable cells as wrong.
    It's called when:
        1) The user made a wrong move on the board, and then the user
        uses the AI button and the AI finds out that there is no solution.
        2) The board had no solutions from the beginning.
    """

    # Iterate through each row of the board
    for i, row in enumerate(game.initial_board):
        # Iterate through each number of the row
        for j, num in enumerate(row):
            if num == 0:
                # Draw a red background for the current cell
                pygame.draw.rect(
                    window, RED,
                    (
                        BOARD_POS[0] + CELL_SIZE * j,
                        BOARD_POS[1] + CELL_SIZE * i,
                        CELL_SIZE, CELL_SIZE
                    )
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
            if num != 0:
                # The background of the cell
                cell_rect = pygame.Rect(
                    j * CELL_SIZE + BOARD_POS[0],
                    i * CELL_SIZE + BOARD_POS[1],
                    CELL_SIZE, CELL_SIZE
                )

                # Render the font and center the number inside `cell_rect`
                styled_text = font.render(str(num), True, THEME_COLOR_2)
                styled_text_rect = styled_text.get_rect()
                styled_text_rect.center = cell_rect.center

                # Draw the background if the cell is an initial cell
                if game.initial_board[i][j] != 0:
                    pygame.draw.rect(window, INITIAL_CELL_COLOR, cell_rect)

                # Draw the number
                window.blit(styled_text, styled_text_rect)

    # Fixes the overlaping of the initial cells on the board's outline
    pygame.draw.rect(
        window, THEME_COLOR_2,
        (
            BOARD_POS[0], BOARD_POS[1],
            WIDTH - BOARD_POS[0] * 2, HEIGHT - BOARD_POS[0] * 2
        ), 2
    )


def toggle_theme():
    """
    This function updates the theme to:
        1) the dark mode if the moon image was clicked
        2) the light mode if the sun image was clicked 
    """

    # Use the global variables from `settings.py`
    global DARK_MODE, THEME_COLOR_1, THEME_COLOR_2
    global SELECTED_CELL_COLOR, INITIAL_CELL_COLOR

    DARK_MODE = not DARK_MODE

    if DARK_MODE:
        THEME_COLOR_1 = BLACK
        THEME_COLOR_2 = WHITE
        SELECTED_CELL_COLOR = DARK_GRAY
        INITIAL_CELL_COLOR = DARK_SLATE_GRAY
    else:
        THEME_COLOR_1 = WHITE
        THEME_COLOR_2 = BLACK
        SELECTED_CELL_COLOR = ANTIQUE_WHITE
        INITIAL_CELL_COLOR = LIGHT_GRAY


if __name__ == "__main__":
    main()
