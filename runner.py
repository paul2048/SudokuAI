import pygame
import sys
import time

from sudoku import Sudoku
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


    while True:
        for event in pygame.event.get():
            # Check if game quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.mouse_pos = pygame.mouse.get_pos()

        window.fill(WHITE)

        if instructions:
            # Unpause the music
            pygame.mixer.music.unpause()

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
                if play_btn.collidepoint(game.mouse_pos):
                    instructions = False
                    time.sleep(.3)

        # If the "Play Game" button was clicked
        else:
            # Pause the music
            pygame.mixer.music.pause()

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

            # New level button
            new_btn = draw_btn(
                window,
                (BOARD_POS[0] + BOARD_SIZE / 1.5 + 15, (BOARD_POS[1] - 50) / 2),
                (WIDTH / 5, 50),
                RED, "New level", WHITE,
                regular_font
            )

            # Draw the outline of the board
            board_rect = pygame.draw.rect(
                window, BLACK,
                (
                    BOARD_POS[0], BOARD_POS[1],
                    WIDTH - BOARD_POS[0] * 2, HEIGHT - BOARD_POS[0] * 2
                ), 2
            )

            # Draw the board
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
            
            # Check for mouse click events
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                # Check if exit button was clicked
                if exit_btn.collidepoint(game.mouse_pos):
                    instructions = True
                    time.sleep(.3)

                # Check if a cell or the left/right/bottom margin
                # (used for deselecting a cell) was clicked
                notop_rect = pygame.Rect(0, BOARD_POS[1], WIDTH, HEIGHT)
                if notop_rect.collidepoint(game.mouse_pos):
                    game.selected_cell = game.get_cell(board_rect)

            # If a cell was selected (clicked), highlight the cell
            selected_cell = game.selected_cell
            if selected_cell:
                # Draw a rectancle on the selected cell
                pygame.draw.rect(
                    window,
                    selected_cell_color,
                    (
                        selected_cell[0] * CELL_SIZE + BOARD_POS[0] + 1,
                        selected_cell[1] * CELL_SIZE + BOARD_POS[1] + 1,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1
                    )
                )

            # Draw the numbers on the board
            game.draw_nums(window, nums_font)

        # Update the window with everything that was drawn
        pygame.display.update()


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


if __name__ == "__main__":
    main()
