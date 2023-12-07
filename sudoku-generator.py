import random
import pygame
import sys


class SudokuGenerator:
    def __init__(self, removed_cells, row_length=9):  # constructor with parameters removed_cells and row_length
        self.row_length = 9
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.box_length = 3

    def get_board(self):  # returns the board
        return self.board

    def print_board(self):  # prints the board as a string
        for row in self.board:
            print(' '.join(str(num) for num in row))

    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        else:
            return True  # returns True if num is in the 2D list at row

    def valid_in_col(self, col, num):
        for i in range(len(self.board)):
            if num == self.board[i][col]:
                return False
        return True  # returns True if num is in the 2D list at col

    def valid_in_box(self, row_start, col_start, num):
        for i in range(row_start, row_start + self.box_length):
            for j in range(col_start, col_start + self.box_length):
                if num == self.board[i][j]:
                    return False
        return True

    def is_valid(self, row, col, num):
        row_start = 3 * (row // 3)
        col_start = 3 * (col // 3)

        if self.valid_in_row(row, num) and self.valid_in_col(col, num) and self.valid_in_box(row_start, col_start, num):
            return True
        else:
            return False  # returns True if num is valid in the 2D list at row, col

    def fill_box(self, row_start, col_start):
        my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(my_list)  # shuffles numbers 1 - 9

        counter = 0
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                self.board[i][j] = my_list[counter]
                counter += 1

    def fill_diagonal(self):  # fill 3x3 diagonals in the sudoku board starting from top left going to bottom right
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    # given
    def fill_remaining(self, row, col):  # uses back tracking to fill empty spots, which are zeros, in the sudoku grid
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):  # fills out the entire sudoku board with values 1-9
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):  # randomly removes a certain number of cells depending on the difficulty chosen
        cells_to_remove = self.removed_cells
        while cells_to_remove > 0:  # ensures that the number of cells to remove is not greater than the number
            # of cells in the board
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)  # create random row and column values to set to 0
            if self.board[row][col] != 0:  # checks to make sure that the cell is not already 0
                self.board[row][col] = 0   # sets cell to 0
                cells_to_remove -= 1  # set the number of cells to remove to the number of cells to remove minus 1


def generate_sudoku(size, removed):  # function that generates the entire sudoku board with empty cells ready
    # to be played
    sudoku = SudokuGenerator(removed, size)
    sudoku.fill_values()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board


def check_winner(boardd):  # checks to see if the board is full and if all the numbers are correct
    for i in range(9):
        for j in range(9):
            temp = boardd.board[i][j]
            boardd.board[i][j] = 0
            if boardd.is_valid(i, j, temp):
                boardd.board[i][j] = temp
                continue
            else:
                return False
    return True


def draw_game_won(screen):  # dispays the new screen for at the end if the user successfully completes the sudoku board
    title_font = pygame.font.Font(None, 65)
    button_font = pygame.font.Font(None, 70)

    screen.fill((0, 33, 165))  # set background color

    title_surface = title_font.render("You won!", 0, (250, 70, 22))
    title_rectangle = title_surface.get_rect(
        center=(450 // 2, 500 // 2 - 150))
    screen.blit(title_surface, title_rectangle)

    exit_text = button_font.render("Exit", 0, (0, 33, 165))

    exit_surface = pygame.Surface((exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
    exit_surface.fill((250, 70, 22))
    exit_surface.blit(exit_text, (10, 10))

    exit_rectangle = exit_surface.get_rect(
        center=(450 // 2, 500 // 2 + 0))

    screen.blit(exit_surface, exit_rectangle)

    while True:
        for event in pygame.event.get():  # uses pygame functions to check which event is occurring
            if event.type == pygame.QUIT:  # checks if close window is attempted
                sys.exit()  # exits program
            if event.type == pygame.MOUSEBUTTONDOWN:  # check if mouse button is clicked
                if exit_rectangle.collidepoint(event.pos):
                    sys.exit()  # exits program
        pygame.display.update()

def draw_game_lost(screen):  # displays new screen for at the end if the user unseccuessfully complete the sudoku board
    title_font = pygame.font.Font(None, 65)
    button_font = pygame.font.Font(None, 70)

    screen.fill((0, 33, 165))  # sets background color

    title_surface = title_font.render("You lost!", 0, (250, 70, 22))
    title_rectangle = title_surface.get_rect(
        center=(450 // 2, 500 // 2 - 150))
    screen.blit(title_surface, title_rectangle)

    restart_text = button_font.render("Restart", 0, (0, 33, 165))

    restart_surface = pygame.Surface((restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
    restart_surface.fill((250, 70, 22))
    restart_surface.blit(restart_text, (10, 10))

    restart_rectangle = restart_surface.get_rect(
        center=(450 // 2, 500 // 2))

    screen.blit(restart_surface, restart_rectangle)

    while True:
        for event in pygame.event.get():  # uses pygame functions to check which event is occurring
            if event.type == pygame.QUIT:  # checks if close window is attempted
                sys.exit()  # exits program
            if event.type == pygame.MOUSEBUTTONDOWN:  # check if mouse button is clicked
                if restart_rectangle.collidepoint(event.pos):
                    difficulty = draw_game_start(screen)  # sends user back to the home screen
                    if difficulty:
                        draw_grid(screen, difficulty)
        pygame.display.update()


def draw_game_start(screen):  # displays screen for the home screen at the beginning of the sudoku game
    start_title_font = pygame.font.Font(None, 65)
    button_font = pygame.font.Font(None, 70)

    screen.fill((0, 33, 165)) # color background

    # Initialize and draw title
    title_surface = start_title_font.render("Welcome to Sudoku", 0, (250, 70, 22))
    title_rectangle = title_surface.get_rect(
        center=(450 // 2, 500 // 2 - 150))
    screen.blit(title_surface, title_rectangle)

    # initialize buttons and text

    easy_text = button_font.render("Easy", 0, (0, 33, 165))
    medium_text = button_font.render("Medium", 0, (0, 33, 165))
    hard_text = button_font.render("Hard", 0, (0, 33, 165))

    easy_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    easy_surface.fill((250, 70, 22))
    easy_surface.blit(easy_text, (10, 10))
    medium_surface = pygame.Surface((medium_text.get_size()[0] + 20, medium_text.get_size()[1] + 20))
    medium_surface.fill((250, 70, 22))
    medium_surface.blit(medium_text, (10, 10))
    hard_surface = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
    hard_surface.fill((250, 70, 22))
    hard_surface.blit(hard_text, (10, 10))

    easy_rectangle = easy_surface.get_rect(
        center=(450 // 2, 500 // 2 + 0))
    medium_rectangle = medium_surface.get_rect(
        center=(450 // 2, 500 // 2 + 90))
    hard_rectangle = hard_surface.get_rect(
        center=(450 // 2, 500 // 2 + 180))

    screen.blit(easy_surface, easy_rectangle)
    screen.blit(medium_surface, medium_rectangle)
    screen.blit(hard_surface, hard_rectangle)


    while True:
        for event in pygame.event.get():  # uses pygame fucntions to check which event is occuring
            if event.type == pygame.QUIT:   # checks if close window is attempted
                sys.exit()  # exits program
            if event.type == pygame.MOUSEBUTTONDOWN:  # check if mouse button is clicked
                if easy_rectangle.collidepoint(event.pos):
                    return generate_sudoku(9, 30)
                # change to 30 when GUI done
                if medium_rectangle.collidepoint(event.pos):
                    return generate_sudoku(9, 40)
                if hard_rectangle.collidepoint(event.pos):
                    return generate_sudoku(9, 50)


        pygame.display.update()


def draw_grid(screen, starting_board):  # displays screen for after a difficulty level is chose and game is ready to play

    start_board = [row[:] for row in starting_board]

    sudoku_board = starting_board
    # print(start_board)


    sketch_board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    pygame.display.set_mode((450, 500))
    number_font = pygame.font.Font(None, 36)
    sketch_font = pygame.font.Font(None, 25)
    button_font = pygame.font.Font(None, 20)

    current_row, current_col = 0, 0


    while True:
        for event in pygame.event.get():  # uses pygame fucntions to check which event is occuring
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # checks which keys on keyboard are being pressed
                if event.key == pygame.K_UP:  # checks up arrow key
                    current_row = max(0, current_row - 1)  # Move up (limit at 0)
                elif event.key == pygame.K_DOWN:  # checks for down arrow key
                    current_row = min(8, current_row + 1)  # Move down (limit at 8)
                elif event.key == pygame.K_LEFT:  # checks for left arrow key
                    current_col = max(0, current_col - 1)  # Move left (limit at 0)
                elif event.key == pygame.K_RIGHT:  # checks for right arrow key
                    current_col = min(8, current_col + 1)
                elif event.key == pygame.K_BACKSPACE:  # check for backspace key and remove cell
                    sudoku_board[current_col][current_row] = 0
                # check which number from 1-9 is being pressed
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                                   pygame.K_8, pygame.K_9]:
                    entered_number = int(pygame.key.name(event.key))
                    if sudoku_board[current_col][current_row] == 0:
                        sketch_board[current_col][current_row] = entered_number
                elif event.key == pygame.K_RETURN:  # check for ENTER key on keyboard
                    if sketch_board[current_col][current_row] != 0:
                        sudoku_board[current_col][current_row] = sketch_board[current_col][current_row]
                        sketch_board[current_col][current_row] = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:  # check for mouse being clicked to be able to choose cells on
                # the board using mouse
                mouse = pygame.mouse.get_pos()
                if mouse[1] < 450:
                    current_col = mouse[0] // 50
                    current_row = mouse[1] // 50
                else:
                    continue
                # print("Clicked on row:", row_clicked, "column:", column_clicked)  # Print clicked cell position

        screen.fill((0, 0, 0))

        # draws the lines to set up grid for sudoku board
        for i in range(1, 10):
            if i % 3 == 0:
                pygame.draw.line(
                    screen,
                    (250, 70, 22),
                    (0, i * 50),
                    (500, i * 50),
                )
            else:
                pygame.draw.line(
                    screen,
                    (0, 33, 165),
                    (0, i * 50),
                    (500, i * 50)
                )
        for i in range(1, 10):
            if i % 3 == 0:
                pygame.draw.line(
                    screen,
                    (250, 70, 22),
                    (i * 50, 0),
                    (i * 50, 450),
                )
            else:

                pygame.draw.line(
                    screen,
                    (0, 33, 165),
                    (i * 50, 0),
                    (i * 50, 450),
                )

        # draws the sketched numbers onto the cells
        for row in range(9):
            for col in range(9):
                if int(sketch_board[row][col]) != 0:
                    number_text = sketch_font.render(str(sketch_board[row][col]), 0, (150, 150, 150))
                    col_pos = col * 50 + 5
                    row_pos = row * 50 + 5
                    screen.blit(number_text, (row_pos, col_pos))

        # draws the numbers regularly into the cells
        for row in range(9):
            for col in range(9):
                if int(sudoku_board[row][col]) != 0:
                    number_text = number_font.render(str(sudoku_board[row][col]), 0, (255, 255, 255))
                    col_pos = col * 50 + 14
                    row_pos = row * 50 + 20
                    screen.blit(number_text, (row_pos, col_pos))

        # makes the 3 buttons at the bottom of the sudoku game (reset, restart, exit)
        reset_text = button_font.render("reset", 0, (0, 33, 165))
        restart_text = button_font.render("restart", 0, (0, 33, 165))
        exit_text = button_font.render("exit", 0, (0, 33, 165))

        reset_surface = pygame.Surface((reset_text.get_size()[0] + 20, reset_text.get_size()[1] + 20))
        reset_surface.fill((250, 70, 22))
        reset_surface.blit(reset_text, (10, 10))
        restart_surface = pygame.Surface((restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
        restart_surface.fill((250, 70, 22))
        restart_surface.blit(restart_text, (10, 10))
        exit_surface = pygame.Surface((exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
        exit_surface.fill((250, 70, 22))
        exit_surface.blit(exit_text, (10, 10))

        reset_rectangle = reset_surface.get_rect(
            center=(150, 475))
        restart_rectangle = restart_surface.get_rect(
            center=(225, 475))
        exit_rectangle = exit_surface.get_rect(
            center=(300, 475))

        screen.blit(reset_surface, reset_rectangle)
        screen.blit(restart_surface, restart_rectangle)
        screen.blit(exit_surface, exit_rectangle)

        for event in pygame.event.get():  # uses pygame fucntions to check which event is occuring
            if event.type == pygame.QUIT:  # checks if close window is attempted
                sys.exit()  # exits program
            if event.type == pygame.MOUSEBUTTONDOWN:  # checks for mouse button being clicked
                if reset_rectangle.collidepoint(event.pos):
                    draw_grid(screen, start_board)  # set sudoku grid back to original states

                if restart_rectangle.collidepoint(event.pos):
                    difficulty = draw_game_start(screen)  # sends user back to home screen
                    if difficulty:
                        draw_grid(screen, difficulty)

                if exit_rectangle.collidepoint(event.pos):
                    sys.exit()  # exits program

        # highlights the cell in which the user is currently on
        pygame.draw.rect(screen, (255, 0, 0), (current_col * 50, current_row * 50, 50, 50), 3)

        full_list = []
        for i in range(9):
            for j in range(9):
                full_list.append(sudoku_board[i][j])
        if 0 not in full_list:  # checks if the board is full
            winner = SudokuGenerator(1)
            winner.board = sudoku_board
            if check_winner(winner):
                draw_game_won(screen)
            else:
                draw_game_lost(screen)

        pygame.display.update()




if __name__ == "__main__":

    pygame.init()  # initialized pygame
    screen = pygame.display.set_mode((450, 500))  # sets the dimensions of the screen
    pygame.display.set_caption("Sudoku")  # sets the name of the window to Sudoku at the top
    difficulty = draw_game_start(screen)
    if difficulty:
        draw_grid(screen, difficulty)
