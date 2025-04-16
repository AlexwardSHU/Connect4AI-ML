import random
import heapq
import numpy as np

class Connect4:
    def __init__(self):
        self.board = np.full((6,7), ' ')
        self.currentPlayer = 'R'

    def Print_Board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-"*25)

    def Reset_Board(self):
        for row in range(6):
            for col in range(7):
                self.board[row, col] = ' '

    def Find_Legal_Moves(self):
        legal_moves = []
        for col in range(7):
            if self.board[0, col] == ' ':
                legal_moves.append(col)
        return legal_moves

    def Make_Move(self, col, player):
        for row in range(5, -1, -1):
            if self.board[row, col] == ' ':
                self.board[row, col] = player
                return True
        return False

    def Check_for_Win(self, player):
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

    def Draw(self):
        return ' ' not in self.board

class Random_Agent:
    def __init__(self, game, AI_Player, Human_Player):
        self.game = game
        self.AI_Player = AI_Player
        self.Human_Player = Human_Player

    def Random_Move(self):
        return random.choice(self.game.Find_Legal_Moves())

class Rule_Based_Agent:
    def __init__(self, game, AI_Player, Human_Player):
        self.game = game
        self.AI_Player = AI_Player
        self.Human_Player = Human_Player

    def Make_Move(self, Board):
        for col in self.game.Find_Legal_Moves():
            for row in range(5, -1, -1):
                if Board[row, col] == ' ':
                    Board[row, col] = self.AI_Player
                    if self.game.Check_for_Win(self.AI_Player):
                        Board[row, col] = ' '
                        return col
                    Board[row, col] = ' '

        for col in self.game.Find_Legal_Moves():
            for row in range(5, -1, -1):
                if Board[row, col] == ' ':
                    Board[row, col] = self.Human_Player
                    if self.game.Check_for_Win(self.Human_Player):
                        Board[row, col] = ' '
                        return col
                    Board[row, col] = ' '

        return random.choice(self.game.Find_Legal_Moves())


class MiniMax_Agent:
    def __init__(self, game, AI_Player, Human_Player):
        self.game = game
        self.AI_Player = AI_Player
        self.Human_Player = Human_Player
        self.max_depth = 5

    def Score_Position(self, player):
        score = 0
        board = self.game.board
        center_array = [board[row][3] for row in range(6)]
        score += center_array.count(player) * 3
        return score

    def Minimax(self, depth, alpha, beta, is_maximising):
        if self.game.Check_for_Win(self.AI_Player):
            return 10 - depth
        elif self.game.Check_for_Win(self.Human_Player):
            return depth - 10
        if self.game.Draw():
            return 0
        if depth >= self.max_depth:
            return self.Score_Position(self.AI_Player) - self.Score_Position(self.Human_Player)

        if is_maximising:
            max_eval = -np.inf
            for col in self.game.Find_Legal_Moves():
                row = self.Next_Open_Row(col)
                if row is not None:
                    self.game.board[row, col] = self.AI_Player
                    eval = self.Minimax(depth + 1, alpha, beta, False)
                    self.game.board[row, col] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = np.inf
            for col in self.game.Find_Legal_Moves():
                row = self.Next_Open_Row(col)
                if row is not None:
                    self.game.board[row, col] = self.Human_Player
                    eval = self.Minimax(depth + 1, alpha, beta, True)
                    self.game.board[row, col] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def Best_Move(self):
        best_val = -np.inf
        move = None
        for col in self.game.Find_Legal_Moves():
            row = self.Next_Open_Row(col)
            if row is not None:
                self.game.board[row, col] = self.AI_Player
                move_val = self.Minimax(0, -np.inf, np.inf, False)
                self.game.board[row, col] = ' '
                if move_val > best_val:
                    best_val = move_val
                    move = col
        return move

    def Next_Open_Row(self, col):
        for row in range(5, -1, -1):
            if self.game.board[row, col] == ' ':
                return row
        return None


def simulate_game(bots):
    game = Connect4()
    agent1 = None
    agent2 = None
    valid1 = False
    valid2 = False
    valid_num = False
    num_of_games = 0
    agent1_wins = 0
    agent2_wins = 0
    draws = 0
    while not valid_num:
        try:
            num_of_games = int(input("How many games should be played: "))
            valid_num = True
        except ValueError:
            print("Invalid input, try again")
    match bots:
        case 1:
            agent1 = Random_Agent(game, "R", "Y")
            agent2 = Rule_Based_Agent(game, "Y", "R")
        case 2:
            agent1 = Rule_Based_Agent(game, "R", "Y")
            agent2 = MiniMax_Agent(game, "Y", "R")
    for x in range(num_of_games):
        while True:
            if bots == 1:
                while not valid1:
                    col = agent1.Random_Move()
                    if col in game.Find_Legal_Moves():
                        if game.Make_Move(col, agent1.AI_Player):
                            valid1 = True

            if bots == 2:
                while not valid1:
                    col = agent1.Make_Move(game.board)
                    if col in game.Find_Legal_Moves():
                        if game.Make_Move(col, agent1.AI_Player):
                            valid1 = True

            if game.Check_for_Win(agent1.AI_Player):
                print(agent1.AI_Player + " wins")
                agent1_wins+=1
                game.Reset_Board()
                break

            if bots == 1:
                while not valid2:
                    col = agent2.Make_Move(game.board)
                    if col in game.Find_Legal_Moves():
                        if game.Make_Move(col, agent2.AI_Player):
                            valid2 = True

            if bots == 2:
                while not valid2:
                    col = agent2.Best_Move()
                    if col in game.Find_Legal_Moves():
                        if game.Make_Move(col, agent2.AI_Player):
                            valid2 = True

            if game.Check_for_Win(agent2.AI_Player):
                print(agent2.AI_Player + " wins")
                agent2_wins += 1
                game.Reset_Board()
                break

            if game.Draw():
                print("Draw")
                draws+=1
                game.Reset_Board()
                break

            valid1 = False
            valid2 = False

    print("Agent 1 wins " + agent1.AI_Player + ": " + str(agent1_wins) + "\nAgent 2 wins " + agent2.AI_Player + ": " + str(agent2_wins) + "\nDraws:" + str(draws))


def play(opponent):
    game = Connect4()
    agent = None
    match opponent:
        case 1: agent = Random_Agent(game, "Y", "R")
        case 2: agent = Rule_Based_Agent(game, "Y", "R")
        case 3: agent = MiniMax_Agent(game, "Y", "R")
    valid = False
    AIvalid = False
    print("Red vs Yellow")
    while True:
        game.Print_Board()
        print(game.currentPlayer + "'s turn")
        if game.currentPlayer == "R" or opponent == 5:
            while not valid:
                try:
                    col = int(input("Pick a column(0-6): "))
                    if col in game.Find_Legal_Moves():
                        if game.Make_Move(col, game.currentPlayer):
                            valid = True
                        else:
                            print("Column Full")
                    else:
                        print("Invalid input, try again")
                except ValueError:
                    print("Invalid input, try again")

        if game.Check_for_Win(game.currentPlayer):
            game.Print_Board()
            print(game.currentPlayer + " wins")
            break

        if opponent == 1:
            while not AIvalid:
                col = agent.Random_Move()
                if col in game.Find_Legal_Moves():
                    if game.Make_Move(col, agent.AI_Player):
                        AIvalid = True

        elif opponent == 2:
            while not AIvalid:
                col = agent.Make_Move(game.board)
                if col in game.Find_Legal_Moves():
                    if game.Make_Move(col, agent.AI_Player):
                        AIvalid = True

        elif opponent == 3:
            while not AIvalid:
                col = agent.Best_Move()
                if col in game.Find_Legal_Moves():
                    if game.Make_Move(col, agent.AI_Player):
                        AIvalid = True

        if game.Check_for_Win(agent.AI_Player):
            game.Print_Board()
            print(agent.AI_Player + " wins")
            break

        if game.Draw():
            game.Print_Board()
            print("Draw")
            break

        if opponent == 5:
            if game.currentPlayer == 'R':
                game.currentPlayer = 'Y'
            else:
                game.currentPlayer = 'R'
        valid = False
        AIvalid = False

def choose_bots():
    valid = False
    choice = 0
    print("Choose Bot Game")
    print("1) Random Agent vs Rule Based Agent \n2) Rule Based Agent vs Minimax Agent \n3) Minimax Agent vs ML Agent")
    while not valid:
        try:
            choice = int(input("Please choose a Match: "))
            if 4 > choice > 0:
                valid = True
            else:
                print("Invalid input, try again")
        except ValueError:
            print("Invalid input, try again")
    return choice

def main_menu():
    valid = False
    choice = 0
    print("Connect 4")
    print("1) Random Agent \n2) Rule Based Agent \n3) Minimax Agent \n4) ML Agent \n5) P1 VS P2 \n6) Bot vs Bot")
    while not valid:
        try:
            choice = int(input("Please choose a Game Mode: "))
            if 7 > choice > 0:
                valid = True
            else:
                print("Invalid input, try again")
        except ValueError:
            print("Invalid input, try again")
    return choice


player = main_menu()
if player < 6:
    play(player)
else:
    bots = choose_bots()
    simulate_game(bots)
