import random
import tkinter as tk
from tkinter import messagebox

class BattleshipGame:
    def __init__(self):
        self.grid_size = 10
        self.ships = {
            "Carrier": 5,
            "Battleship": 4,
            "Cruiser": 3,
            "Submarine": 3,
            "Destroyer": 2
        }
        self.player1_board = [["-" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.player2_board = [["-" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.player1_moves = set()
        self.player2_moves = set()

    def place_ships_randomly(self, board):
        for ship, size in self.ships.items():
            placed = False
            while not placed:
                orientation = random.choice(["H", "V"])

                # horizontal
                if orientation == "H":
                    row = random.randint(0, self.grid_size - 1)
                    col = random.randint(0, self.grid_size - size)
                    if all(board[row][col + i] == "~" for i in range(size)):
                        for i in range(size):
                            board[row][col + i] = ship[0]
                        placed = True

                # vertical
                else:
                    row = random.randint(0, self.grid_size - size)
                    col = random.randint(0, self.grid_size - 1)
                    if all(board[row + i][col] == "-" for i in range(size)):
                        for i in range(size):
                            board[row + i][col] = ship[0]
                        placed = True

    # TODO: static?
    def validate_move(self, move, moves_made):
        if move in moves_made:
            return False
        row, col = move
        return 0 <= row < self.grid_size and 0 <= col < self.grid_size

    def make_move(self, board, move):
        row, col = move
        if board[row][col] != "-":
            hit_ship = board[row][col]
            board[row][col] = "X"
            return f"Hit {hit_ship}!"
        else:
            board[row][col] = "O"
            return "Miss!"

    def all_ships_sunk(self, board):
        return all(all(cell in ["-", "O", "X"] for cell in row) for row in board)




####
class Player: #TODO, used for creating types of players (Human and Computer)
    def __init__(self, name):
        self.name = name

class HumanPlayer(Player):  #TODO
    def __init__(self, name):
        super().__init__(name)

class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.last_hit = None

    def make_move(self, game, board, moves_made):

        # if there was a previous hit, play more intelligently (rather than random)
        if self.last_hit:
            row, col = self.last_hit
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                move = (new_row, new_col)

                # TODO: use validate_moves
                if game.validate_move(move, moves_made):

                    moves_made.add(move)
                    result = game.make_move(board, move)

                    # TODO: modify this to have memory of previous hit in case adjacent not hit, but other adjacents available
                    if "Hit" in result:
                        self.last_hit = move

                    return move, result

            # if all adjacent moves exhausted
            self.last_hit = None
            # TODO: recursive, maybe make it non-recursive?
            self.make_move(game, board, moves_made)




        # choose a random coordinate for move
        else:
            move = (random.randint(0, game.grid_size - 1), random.randint(0, game.grid_size - 1))
            if game.validate_move(move, moves_made):
                moves_made.add(move)
                result = game.make_move(board, move)
                if "Hit" in result:
                    self.last_hit = move
                else:
                    self.last_hit = None
                return move, result

            # TODO: recursive, maybe make it non-recursive?
            else:
                self.make_move(game, board, moves_made)


class BattleshipUI:
    def __init__(self, master):
        self.master = master                        # tkinter root
        self.master.title("Battleship")
        self.game = BattleshipGame()
        self.player1 = HumanPlayer("Player 1")
        self.player2 = None
        self.current_player = self.player1
        self.game_mode = None                       # currently: (multiplayer, computer)

        self.create_main_menu()

    def create_main_menu(self):
        self.main_frame = tk.Frame(self.master)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20)

        tk.Label(self.main_frame, text="Welcome to Battleship!", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        tk.Button(self.main_frame, text="Multiplayer", command=self.start_multiplayer).grid(row=1, column=0, pady=5)
        tk.Button(self.main_frame, text="Play against Computer", command=self.start_computer_game).grid(row=2, column=0, pady=5)

    # TODO
    def start_multiplayer(self):
        self.game_mode = "multiplayer"
        self.player2 = HumanPlayer("Player 2")
        self.setup_game()

    def start_computer_game(self):
        self.game_mode = "computer"
        self.player2 = ComputerPlayer("Computer")
        self.setup_game()

    def setup_game(self):
        self.main_frame.destroy()
        self.game.place_ships_randomly(self.game.player1_board)
        self.game.place_ships_randomly(self.game.player2_board)

        self.game_frame = tk.Frame(self.master)
        self.game_frame.grid(row=0, column=0, padx=20, pady=20)

        self.player_label = tk.Label(self.game_frame, text=f"{self.player1.name}'s turn", font=("Arial", 14))
        self.player_label.grid(row=0, column=0, columnspan=self.game.grid_size*2+3, pady=10)

        # Player 1 board
        self.player1_buttons = self.create_board(1, 1, 0)
        tk.Label(self.game_frame, text=f"{self.player1.name}'s Board", font=("Arial", 12)).grid(row=1, column=0, columnspan=self.game.grid_size+1, pady=5)

        # Gap column
        self.game_frame.grid_columnconfigure(self.game.grid_size + 1, minsize=50)

        # Separator
        tk.Frame(self.game_frame, width=2, bg="black").grid(row=1, column=self.game.grid_size+1, rowspan=self.game.grid_size+1, sticky="ns", padx=10)

        # Player 2 board
        self.player2_buttons = self.create_board(1, 1, self.game.grid_size+2)
        tk.Label(self.game_frame, text=f"{self.player2.name}'s Board", font=("Arial", 12)).grid(row=1, column=self.game.grid_size+2, columnspan=self.game.grid_size, pady=5)

    def create_board(self, start_row, start_col, offset):
        buttons = []
        for i in range(self.game.grid_size):
            row = []
            for j in range(self.game.grid_size):
                btn = tk.Button(self.game_frame, text="~", width=2, height=1,
                                command=lambda r=i, c=j: self.make_move(r, c))
                btn.grid(row=start_row+i+1, column=start_col+j+offset, padx=1, pady=1)
                row.append(btn)
            buttons.append(row)
        return buttons

    # TODO: logic for multiplayer
    def make_move(self, row, col):
        if self.game_mode == "multiplayer" or (self.game_mode == "computer" and self.current_player == self.player1):
            move = (row, col)
            board = self.game.player2_board if self.current_player == self.player1 else self.game.player1_board
            moves = self.game.player1_moves if self.current_player == self.player1 else self.game.player2_moves
            buttons = self.player2_buttons if self.current_player == self.player1 else self.player1_buttons

            if self.game.validate_move(move, moves):
                result = self.game.make_move(board, move)
                moves.add(move)
                self.update_button(buttons, row, col, result)

                if self.game.all_ships_sunk(board):
                    self.end_game(f"{self.current_player.name} wins!")
                else:
                    self.switch_player()

                # if self.game_mode == "computer" and self.current_player == self.player2:
                #     self.computer_move()

        elif self.game_mode == "computer" and self.current_player == self.player2:

            # TODO: TypeError: cannot unpack non-iterable NoneType object. problem with move not being assigned (assigned to None)
            move, result = self.player2.make_move(self.game, self.game.player1_board, self.game.player2_moves)

            row, col = move
            self.update_button(self.player1_buttons, row, col, result)

            if self.game.all_ships_sunk(self.game.player1_board):
                self.end_game(f"{self.player2.name} wins!")
            else:
                self.switch_player()

    # def computer_move(self):
    #     while True:
    #         move = (random.randint(0, self.game.grid_size - 1), random.randint(0, self.game.grid_size - 1))
    #         if self.game.validate_move(move, self.game.player2_moves):
    #             result = self.game.make_move(self.game.player1_board, move)
    #             self.game.player2_moves.add(move)
    #             row, col = move
    #             self.update_button(self.player1_buttons, row, col, result)
    #
    #             if self.game.all_ships_sunk(self.game.player1_board):
    #                 self.end_game("Computer wins!")
    #             else:
    #                 self.switch_player()
    #             break

    def update_button(self, buttons, row, col, result):
        if "Hit" in result:
            buttons[row][col].config(text="X", bg="red")
        else:
            buttons[row][col].config(text="O", bg="gray")

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        self.player_label.config(text=f"{self.current_player.name}'s turn")

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.master.quit()

    def start(self):
        self.current_player = self.player1
        self.player_label.config(text=f"{self.current_player.name}'s turn")

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleshipUI(root)
    root.mainloop()


