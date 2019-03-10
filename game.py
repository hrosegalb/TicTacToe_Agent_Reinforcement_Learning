import numpy as np

# Hannah Galbraith
# CS546
# 3/10/19
# Program 2

#######################
# Game class for      #
# tic-tac-toe game    #
######################


class Game(object):
    
    def __init__(self):
        self.board = np.zeros((3,3))


    def make_move(self, position, player):
        """ :param position: tuple of integers
            :param player: 'X' or 'O'
        
            Method takes a position and player as arguments. If the board is 
            empty in the position given (i.e. if there is a '0' in that grid element),
            then method puts a '1' in that position if the player is 'X' and '2' if 
            player is '0' and returns True. Otherwise, if the spot is occupied, it returns False. """

        move_made = False

        if self.board[position[0]][position[1]] == 0:
            if player == 'X':
                self.board[position[0]][position[1]] = 1
            else:
                self.board[position[0]][position[1]] = 2
            move_made = True

        return move_made

    
    def get_possible_next_moves(self):
        """ Method creates a list of all positions on the board that are empty, i.e. 
            all matrix indices that have a '0' in them. Returns a list of tuples. """

        actions = []

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] == 0:
                    actions.append((i,j))
        
        return actions

    
    def translate_board_state_to_index(self):
        """ Method translates the current board state into an integer that can be used to index into the Agent's QMatrix.
            Returns a sum of (c0 * 3^0 + c1 * 3^1 + ... + c8 * 3^8), where each 'c' is determined by the value currently 
            in the corresponding position on the board. Returns the final sum. """

        index = (self.board[0][0] * 3**0) + (self.board[0][1] * 3**1) + (self.board[0][2] * 3**2) + (self.board[1][0] * 3**3) + (self.board[1][1] * 3**4) + (self.board[1][2] * 3**5) + (self.board[2][0] * 3**6) + (self.board[2][1] * 3**7) + (self.board[2][2] * 3**8)
        return int(index)


    def has_agent_won(self):
        """ Evaluates whether the agent has won by checking if there are three adjacent '1's in the matrix either
            diagonally, horizontally, or vertically. If so, it returns True. Otherwise, it returns False. """

        # Evaluate diagonals
        if self.board[0][0] == 1 and self.board[1][1] == 1 and self.board[2][2] == 1:
            return True
        
        if self.board[2][0] == 1 and self.board[1][1] == 1 and self.board[0][2] == 1:
            return True

        # Evaluate horizontally
        for i in range(self.board.shape[0]):
            if self.board[i][0] == 1 and self.board[i][1] == 1 and self.board[i][2] == 1:
                return True
        
        # Evaluate vertically
        for i in range(self.board.shape[1]):
            if self.board[0][i] == 1 and self.board[1][i] == 1 and self.board[2][i] == 1:
                return True

        return False


    def has_opponent_won(self):
        """ Evaluates whether the opponent has won by checking if there are three adjacent '2's in the matrix either
            diagonally, horizontally, or vertically. If so, it returns True. Otherwise, it returns False. """

        # Evaluate diagonals
        if self.board[0][0] == 2 and self.board[1][1] == 2 and self.board[2][2] == 2:
            return True
        
        if self.board[2][0] == 2 and self.board[1][1] == 2 and self.board[0][2] == 2:
            return True

        # Evaluate horizontally
        for i in range(self.board.shape[0]):
            if self.board[i][0] == 2 and self.board[i][1] == 2 and self.board[i][2] == 2:
                return True
        
        # Evaluate vertically
        for i in range(self.board.shape[1]):
            if self.board[0][i] == 2 and self.board[1][i] == 2 and self.board[2][i] == 2:
                return True

        return False


    def is_it_a_draw(self):
        """ Evaluates whether the game is a draw by iterating through the board to see if there are any '0's
            left. If so, it returns False. Otherwise, if no '0's are found, it returns True.
            NOTE: This method will only work as intended if has_agent_won() and has_opponent_won() have been
            executed first and both returned False. This method does not check whether either player has won.
            Therefore, it is possible that the method would return True despite there being a winning game. """

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] == 0:
                    return False
        
        return True

    
    def reset_board(self):
        """ This method should be invoked after a game has been played. It resets the board by creating a new
            3x3 matrix of zeros. """

        self.board = np.zeros((3,3))


    def print_board(self):
        """ Method prints the current board state by translating zeros into ' ', ones into 'X', and twos into 'O'. """

        state = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] == 0:
                    state.append(' ')
                elif self.board[i][j] == 1:
                    state.append('X')
                else:
                    state.append('O')

        print("{}|{}|{}".format(state[0], state[1], state[2]))
        print("------")
        print("{}|{}|{}".format(state[3], state[4], state[5]))
        print("------")
        print("{}|{}|{}".format(state[6], state[7], state[8]))
        print("\n")