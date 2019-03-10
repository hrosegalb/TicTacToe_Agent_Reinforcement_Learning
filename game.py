import numpy as np

class Game(object):
    
    def __init__(self):
        self.board = np.zeros((3,3))


    def make_move(self, position, player):
        move_made = False

        if self.board[position[0]][position[1]] == 0:
            if player == 'X':
                self.board[position[0]][position[1]] = 1
            else:
                self.board[position[0]][position[1]] = 2
            move_made = True

        return move_made

    
    def get_possible_next_moves(self):
        actions = []

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] == 0:
                    actions.append((i,j))
        
        return actions

    
    def translate_board_state_to_index(self):
        index = (self.board[0][0] * 3**0) + (self.board[0][1] * 3**1) + (self.board[0][2] * 3**2) + (self.board[1][0] * 3**3) + (self.board[1][1] * 3**4) + (self.board[1][2] * 3**5) + (self.board[2][0] * 3**6) + (self.board[2][1] * 3**7) + (self.board[2][2] * 3**8)
        return int(index)


    def has_agent_won(self):
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
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] == 0:
                    return False
        
        return True

    
    def reset_board(self):
        self.board = np.zeros((3,3))


    def print_board(self):
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