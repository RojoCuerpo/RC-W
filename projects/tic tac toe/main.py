import random  # <--- for pc to make its move
import time  # <--- to chill a little
import os  # <--- to clear the screen between each turn


class Game:
    def __init__(self):
        # possible moves, one for each of the 9 spaces on the board. pc and player will remove one option per turn until
        # someone wins or a draw happens
        self.possible_moves = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        # this one is to create a visual system of coordinates that the user can see to guide their shots
        self.places = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

        # The board comes from this dictionary. I opted for a dict to compare the user's input directly to each key,
        # and replace the correct value with an "X"
        self.board = [{"1": ".", "2": ".", "3": "."}, {"4": ".", "5": ".", "6": "."},
                      {"7": ".", "8": ".", "9": "."}]

        # to cancel any place already chosen in the coordinates grid
        self.blank = "."

        # to replace the dots of the empty board with the player's shot
        self.shoot = "X"

        # same deal, for the pc
        self.pc_shoot = "0"

        # there are 3 ways to finish the game. First we stop the game and then check which case applies:
        # 0:
        self.stop = False
        # 1:
        self.win = False
        # 2:
        self.defeat = False
        # draw
        self.draw = False

    # this one prints only the grid of coordinates
    def print_places(self):
        print(f"Available Places: \n")
        for i in self.places:
            for x in i:
                print(" " + x, end=" ")
            print()

    # this one prints only the board. Note that we print only the value for each key on each dict.
    # it will be useful later
    def print_board(self):
        print("\nBoard: ")
        for dic in self.board:
            for x in dic:
                print(" " + dic[x], end=" ")
            print()

    # controls player's and pc's input. It is done on 5 stages for both players:
    def moves(self):
        # 1- Takes the input, eg: "6"
        # NOTE: if the input is not a valid coordinate, "17" or "S"; we'll have a ValueError,
        # we deal with this later on, check "play" method
        move = input("\nYour move: ")

        # 2- remove the coordinate from the possible_moves list, so none can take it again.
        self.possible_moves.remove(move)

        # 3- this checks the grid and replaces the coordinate with a blank: this place is no longer open
        for row in self.places:
            if move in row:
                row[row.index(move)] = self.blank

        # 4- same deal, but using the X mark on the board.
        for dic in self.board:
            if move in dic:
                dic[move] = self.shoot
        
        # check if player has won:
        # create list of the board's 3 rows, with its marks. Each row is a list. This is easier to check and iterate 
        # through than the dictionary
        x_and_dots = []
        for i in range(len(self.board)):
            x_and_dots.append(list(self.board[i].values()))

        # check for rows: (if shoot is in a row, and all indices of this row are equal to shoot, then player wins)
        for i in x_and_dots:
            if self.shoot in i:
                check_rows = all(x == self.shoot for x in i)
                if check_rows:
                    self.win = True
                    self.stop = True

        # check_columns: (if shoot is in all rows with the same index, a vertical line has been formed. player wins)
        for a, b in enumerate(x_and_dots[0]):
            if x_and_dots[0][a] == x_and_dots[1][a] == x_and_dots[2][a] and b == self.shoot:
                self.win = True
                self.stop = True

        # check diagonal: (if the center square is an X, check if the corners are as well. if so,
        # a diagonal has been formed, player wins)
        if x_and_dots[1][1] == self.shoot:
            if x_and_dots[0][0] == self.shoot:
                if x_and_dots[2][2] == self.shoot:
                    self.win = True
                    self.stop = True
            elif x_and_dots[0][2] == self.shoot:
                if x_and_dots[2][0] == self.shoot:
                    self.win = True
                    self.stop = True

        # if possible_moves is empty, and player didn't win tih the last shot, it means we have a draw
        if len(self.possible_moves) == 0:
            self.draw = True
            self.stop = True

        time.sleep(3)

        # -----------------------------------------------------------------------------------------------------
        # PC'S MOVE:
        # 1- random choice from the possible_moves list, from which we have already removed every previous shot:
        pc_move = random.choice(self.possible_moves)

        # 2-
        self.possible_moves.remove(pc_move)

        # 3-
        for row in self.places:
            if pc_move in row:
                row[row.index(pc_move)] = self.blank

        # 4-
        for dic in self.board:
            if pc_move in dic:
                dic[pc_move] = self.pc_shoot

        # 5- Check if pc has won: we'll take the same algorithms, and just change them to compare the elements on the 
        # rows to the pc_shoot var
        x_and_dots = []
        for i in range(len(self.board)):
            x_and_dots.append(list(self.board[i].values()))

        # rows:
        for i in x_and_dots:
            if self.pc_shoot in i:
                check_rows = all(x == self.pc_shoot for x in i)
                if check_rows:
                    self.defeat = True
                    self.stop = True

        # check_columns:
        for a, b in enumerate(x_and_dots[0]):
            if x_and_dots[0][a] == x_and_dots[1][a] == x_and_dots[2][a] and b == self.pc_shoot:
                self.defeat = True
                self.stop = True

        # check diagonal:
        if x_and_dots[1][1] == self.pc_shoot:
            if x_and_dots[0][0] == self.pc_shoot:
                if x_and_dots[2][2] == self.pc_shoot:
                    self.defeat = True
                    self.stop = True
            elif x_and_dots[0][2] == self.pc_shoot:
                if x_and_dots[2][0] == self.pc_shoot:
                    self.defeat = True
                    self.stop = True

        # finally-clear the screen before printing the updated coordinates grid/board:
        os.system('cls')

    # create methods for each case after the game ends:
    def is_win(self):
        print("\nYou win!")
        self.print_board()
        quit()

    def is_defeat(self):
        print("\nPc wins this one!")
        self.print_board()
        quit()

    def is_draw(self):
        print("\nWe have a draw!")
        self.print_board()
        quit()

    def play(self):
        while not self.stop:
            try:
                self.print_places()
                self.print_board()
                self.moves()
            except ValueError:
                # if player choose an option that doesn't exist on the possible_moves, we catch the error and handle it,
                # this way ensuring we can continue the game
                os.system('cls')
                print("\nInvalid option, try again\n")
            except IndexError:
                if not self.win:
                    self.is_draw()
                else:
                    self.is_win()
        if self.stop:
            if self.win:
                self.is_win()
            if self.defeat:
                self.is_defeat()
            if self.draw:
                self.is_draw()


tictactoe = Game()
tictactoe.play()
