import random
import heapq
import numpy as np

class Connect4:
    def __init__(self):
        self.board = np.full((6,7), ' ')
        self.currentPlayer = 'R'

    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-"*25)

    def find_legal_moves(self):
        legal_moves = []
        for row in range(6):
            for col in range(7):
                if self.board[row, col] == ' ':
                    legal_moves.append(col)
        print(legal_moves)
        return legal_moves

    def make_move(self, col, player):
        for row in range(5, -1, -1):
            if self.board[row, col] == ' ':
                self.board[row, col] = player
                return True
        return False

    def check_for_win(self, player):
        # Horizontal
        for col in range(4):
            for row in range(6):
                if self.board[row, col] == player and self.board[row, col+1] == player and self.board[row, col+2] == player and self.board[row, col+3] == player:
                    return True
        # Vertical
        for col in range(7):
            for row in range(3):
                if self.board[row, col] == player and self.board[row+1, col] == player and self.board[row+2, col] == player and self.board[row+3, col] == player:
                    return True
        # Diagonal1
        for col in range(4):
            for row in range(3):
                if self.board[row, col] == player and self.board[row+1, col+1] == player and self.board[row+2, col+2] == player and self.board[row+3, col+3] == player:
                    return True
        # Diagonal2
        for col in range(4):
            for row in range(3, 6):
                if self.board[row, col] == player and self.board[row-1, col+1] == player and self.board[row-2, col+2] == player and self.board[row-3, col+3] == player:
                    return True

    def draw(self):
        return ' ' not in self.board

def play():
    game = Connect4()
    valid = False
    print("Red vs Yellow")
    while True:
        game.print_board()
        print(game.currentPlayer + "'s turn")
        while not valid:
            try:
                col = int(input("Pick a column(0-6): "))
                if col in game.find_legal_moves():
                    if game.make_move(col, game.currentPlayer):
                        valid = True
                    else:
                        print("Column Full")
                else:
                    print("Invalid input, try again")
            except ValueError:
                print("Invalid input, try again")

        if game.check_for_win(game.currentPlayer):
            game.print_board()
            print(game.currentPlayer + " wins")
            break

        if game.draw():
            game.print_board()
            print("Draw")
            break

        if game.currentPlayer == 'R':
            game.currentPlayer = 'Y'
        else:
            game.currentPlayer = 'R'
        valid = False

play()

