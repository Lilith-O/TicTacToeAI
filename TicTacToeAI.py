import sys
import pygame
import copy
import random
import numpy as np
from constants import *


#PYGAME
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
my_font = pygame.font.SysFont("Times New Roman", 15)
screen.fill(BG_COLOUR)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLUMNS))
        self.empty_squares = self.squares
        self.marked_squares = 0
    
    def final_state(self, show):
        #Horizontal Win
        for row in range(ROWS):
            if(self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0):
                if (show):
                    color = CIRC_COLOR if self.squares[row][0] == 2 else X_COLOR
                    initPos = (OFFSET, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    finalPos = (WIDTH - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    
                    pygame.draw.line(screen, color, initPos, finalPos, LINE_WIDTH)
                return self.squares[row][0]
        #Vertical Win
        for col in range(COLUMNS):
            if(self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0):
                if (show):
                    color = CIRC_COLOR if self.squares[0][col] == 2 else X_COLOR
                    initPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, OFFSET)
                    finalPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - OFFSET)
                    pygame.draw.line(screen, color, initPos, finalPos, LINE_WIDTH)
                return self.squares[0][col]
        #Desc Diagonal Win
        if (self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0):
            if (show):
                color = CIRC_COLOR if self.squares[1][1] == 2 else X_COLOR
                initPos = (OFFSET, OFFSET)
                finalPos = (WIDTH -OFFSET, HEIGHT - OFFSET)
                pygame.draw.line(screen, color, initPos, finalPos, LINE_WIDTH)
            return self.squares[1][1]
        #Asc Diagonal Win
        if(self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0):
            if (show):
                color = CIRC_COLOR if self.squares[1][1] == 2 else X_COLOR
                initPos = (OFFSET, HEIGHT - OFFSET)
                finalPos = (WIDTH - OFFSET, OFFSET)
                pygame.draw.line(screen, color, initPos, finalPos, LINE_WIDTH)
            return self.squares[1][1]
        #No Win
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def empty_square(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))
        return empty_squares
    
    def isFull(self):
        return self.marked_squares == 9
    
    def isEmpty(self):
        return self.marked_squares == 0
    
class AI:
    def __init__(self, level=2, player = 2):
        self.level = level
        self.player = player

    def random(self, board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))

        return empty_squares[index] # (row, col)

    def minimax(self, board, maximizing):
        #terminal case
        case = board.final_state(False)

        #player 1 win
        if case == 1:
            return 1, None #evaluation, move
        #player 2 win
        if case == 2:
            return -1, None #evaluation, move
        #draw
        elif board.isFull():
            return 0, None #evaluation, move
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:

                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:

                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move

        


    def eval(self, main_board):
        if self.level == 1:
            eval = 'random'
            move = self.random(main_board)
        elif self.level == 2:
            
            eval, move = self.minimax(main_board, False)
        
        print(f'AI has chose to mark the square in pos  {move} with an evaluation of: {eval}')
        return move


class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # 1- cross, 2- circle
        self.gamemode = 'AI' # pvp or AI
        self.running = True
        self.show_lines()
    
    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
       
        screen.fill(BG_COLOUR)
        #vertical lines
        pygame.draw.line(screen, BOARD_COLOUR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, BOARD_COLOUR, (WIDTH- SQUARE_SIZE, 0), (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)

        #horizontal lines
        pygame.draw.line(screen, BOARD_COLOUR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BOARD_COLOUR, (0, HEIGHT- SQUARE_SIZE, ), (WIDTH, HEIGHT-SQUARE_SIZE), LINE_WIDTH)
        text_surface = my_font.render("PRESS G change gamemode(PVP or AI), R- Restart game, 0 for random AI and 1 for Hard AI",True, TEXT_COLOR)
        screen.blit(text_surface, (0, 0))

    def next_turn(self):
        self.player = self.player % 2 + 1

    def draw_fig(self, row, col):
        if self.player == 1:

            #descending line
            start_desc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, X_COLOR, start_desc, end_desc, X_WIDTH)

            #ascending line
            start_asc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, X_COLOR, end_asc, start_asc, X_WIDTH)

        elif self.player == 2:
            center = (col * SQUARE_SIZE + SQUARE_SIZE //2, row *SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, SHAPESWIDTH)

    def change_gamemode(self):
        self.gamemode = 'AI' if self.gamemode == 'pvp' else 'pvp'
    
    def isOver(self):
        return self.board.final_state(True) != 0 or self.board.isFull()

    def reset(self, gamemode):
        self.__init__()
        self.gamemode = gamemode



def main():

    #objects
    game = Game()
    board = game.board
    ai = game.ai

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                #g gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                #restart game
                if event.key == pygame.K_r:
                    game.reset(game.gamemode)
                    board = game.board
                    ai = game.ai
                # 0 random AI
                if event.key == pygame.K_0:
                    ai.level = 1
                # 1 minimax AI
                if event.key == pygame.K_1:
                    ai.level = 2

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)
                    if game.isOver():
                        game.running = False

        if(game.gamemode == 'AI' and game.player == ai.player and game.running):
            pygame.display.update()

            row, col = ai.eval(board)
            game.make_move(row,col)
            if game.isOver():
                game.running = False
        
        pygame.display.update()


main()