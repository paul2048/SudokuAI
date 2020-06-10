import pygame
import sys
import time

from sudoku import Sudoku
from settings import *


if __name__ == "__main__":

    # Initialize pygame and create the window
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Fonts
    BMJAPAN = "assets/fonts/BMjapan.ttf"
    lg_bmjapan_font = pygame.font.Font(BMJAPAN, 42)
    md_bmjapan_font = pygame.font.Font(BMJAPAN, 32)
    rules_font = pygame.font.SysFont("Arial", 24)

    # Set window title and window icon
    pygame.display.set_caption("SudokuAI")
    icon = pygame.image.load("assets/images/sudoku.png")
    pygame.display.set_icon(icon)

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
                    rule_seg = rules_font.render(rule_seg, True, BLACK)
                    rule_rect = rule_seg.get_rect()
                    rule_rect.center = (WIDTH / 2, 125 + (i * 60) + (j * 25))
                    window.blit(rule_seg, rule_rect)
            
            # Play game button
            btn_rect = pygame.Rect((WIDTH / 4), (3 / 4) * HEIGHT, WIDTH / 2, 50)
            btn_text = md_bmjapan_font.render("Play Game", True, WHITE)
            btn_text_rect = btn_text.get_rect()
            btn_text_rect.center = btn_rect.center
            pygame.draw.rect(window, BLACK, btn_rect)
            window.blit(btn_text, btn_text_rect)

            # Check if play button clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                if btn_rect.collidepoint(game.mouse_pos):
                    instructions = False
                    time.sleep(3)

        # If the "Play Game" button was clicked
        else:
            # Draw the outline of the board
            board_rect = pygame.draw.rect(window, BLACK, (BOARD_POS[0], BOARD_POS[1], WIDTH - 150, HEIGHT - 150), 2)


            # Draw the board
            for x in range(9):
                # Draw vertical lines
                pygame.draw.line(
                    window,
                    BLACK,
                    (BOARD_POS[0] + (x * CELL_SIZE), BOARD_POS[1]),
                    (BOARD_POS[0] + (x * CELL_SIZE), BOARD_POS[1] + BOARD_SIZE),
                    # The 3rd, 6th and 9th lines are thicker
                    1 if x % 3 != 0 else 2
                )

                # Draw horizontal lines
                pygame.draw.line(
                    window,
                    BLACK,
                    (BOARD_POS[0], BOARD_POS[1] + (x * CELL_SIZE)),
                    (BOARD_POS[0] + BOARD_SIZE, BOARD_POS[1] + (x * CELL_SIZE)),
                    # The 3rd, 6th and 9th lines are thicker
                    1 if x % 3 != 0 else 2
                )

            # Check for mouse clicks on the cells
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.mouse_pos = pygame.mouse.get_pos()
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

        # Update in the window everything that was drawn
        pygame.display.update()
