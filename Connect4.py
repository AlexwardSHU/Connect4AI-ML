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

class Random_Agent:
    def __init__(self, game):
        self.game = game
        self.AI_Player = "Y"
        self.Human_Player = "R"

    def Random_Move(self):
        return random.randint(0, 6)

class Rule_Based_Agent:
    def __init__(self, game):
        self.game = game
        self.AI_Player = "Y"
        self.Human_Player = "R"

def play(opponent):
    game = Connect4()
    agent = Random_Agent(game)
    match opponent:
        case 1: agent = Random_Agent(game)
    valid = False
    AIvalid = False
    print("Red vs Yellow")
    while True:
        game.print_board()
        print(game.currentPlayer + "'s turn")
        if game.currentPlayer == "R" or opponent == 5:
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

        if opponent == 1:
            while not AIvalid:
                col = agent.Random_Move()
                print(col)
                if col in game.find_legal_moves():
                    if game.make_move(col, agent.AI_Player):
                        AIvalid = True

        if game.check_for_win(agent.AI_Player):
            game.print_board()
            print(agent.AI_Player + " wins")
            break

        if game.draw():
            game.print_board()
            print("Draw")
            break

        if opponent == 5:
            if game.currentPlayer == 'R':
                game.currentPlayer = 'Y'
            else:
                game.currentPlayer = 'R'
        valid = False
        AIvalid = False

def main_menu():
    valid = False
    choice = 0
    print("Connect 4")
    print("1) Random Agent \n 2) Rule Based Agent \n 3) Minimax Agent \n 4) ML Agent \n 5) P1 VS P2")
    while not valid:
        try:
            choice = int(input("Please choose a Game Mode: "))
            if 6 > choice > 0:
                valid = True
            else:
                print("Invalid input, try again")
        except ValueError:
            print("Invalid input, try again")
    return choice

player = main_menu()
play(player)
