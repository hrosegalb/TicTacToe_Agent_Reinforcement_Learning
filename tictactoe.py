import numpy as np
import random

class Agent(object):
    
    def __init__(self, eta, gamma, epsilon):
        self.qmatrix = np.zeros((3**9, 9))
        self.eta = eta
        self.gamma = gamma
        self.epsilon = epsilon
        self.player = 'X'
        self.prev_state = None
        self.prev_action = None

    
    def update_epsilon(self, new_epsilon):
        self.epsilon = new_epsilon

    
    def qlearning(self, game):
        action = None
        reward = 0
        done = False

        state = game.translate_board_state_to_index()

        if game.has_opponent_won() == True:
            reward = -1
            self.qmatrix[self.prev_state, self.prev_action] = qmatrix[self.prev_state, self.prev_action] + self.eta * (reward + self.gamma * np.max(self.qmatrix[state, :]) - self.qmatrix[self.prev_state, self.prev_action])
            self.prev_state = None
            self.prev_action = None
            done = True
        elif game.is_it_a_draw() == True:
            self.qmatrix[self.prev_state, self.prev_action] = qmatrix[self.prev_state, self.prev_action] + self.eta * (reward + self.gamma * np.max(self.qmatrix[state, :]) - self.qmatrix[self.prev_state, self.prev_action])
            self.prev_state = None
            self.prev_action = None
            done = True
        else:
            actions = game.get_possible_next_moves()

            if len(actions) > 0:
                indices = self.translate_actions_to_indices(actions)

                if random.random() < self.epsilon:
                    action = random.choice(indices)
                else:
                    action = np.argmax(self.qmatrix[state,:])
        
                action_idx = indices.index(action)
                game.make_move(actions[action_idx], self.player)
                new_state = game.translate_board_state_to_index()

                if game.has_agent_won() == True:
                    reward = 1
                    self.prev_state = None
                    self.prev_action = None
                    done = True

                self.qmatrix[state, action] = self.qmatrix[state, action] + self.eta * (reward + self.gamma * np.max(self.qmatrix[new_state, :]) - self.qmatrix[state, action])
                self.prev_state = state
                self.prev_action = action

        return done


    def translate_actions_to_indices(self, actions):
        indices = []
        for a in actions:
            if a == (0,0):
                indices.append(0)
            elif a == (0,1):
                indices.append(1)
            elif a == (0,2):
                indices.append(2)
            elif a == (1,0):
                indices.append(3)
            elif a == (1,1):
                indices.append(4)
            elif a == (1,2):
                indices.append(5)
            elif a == (2,0):
                indices.append(6)
            elif a == (2,1):
                indices.append(7)
            elif a == (2,2):
                indices.append(8)
        return indices


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


    def is_next_move_winning_move(self, position, player):
        result = False
        if player == 'X':
            self.board[position[0]][position[1]] = 1
            result = has_agent_won()
            self.board[position[0]][position[1]] = 0
        elif player == 'O':
            self.board[position[0]][position[1]] = 2
            result = has_opponent_won()
            self.board[position[0]][position[1]] = 0

        return result


    def has_agent_won(self):
        # Evaluate diagonals
        if self.board[0][0] == 1 and self.board[1][1] == 1 and self.board[2][2] == 1:
            return True
        elif self.board[2][0] == 1 and self.board[1][1] == 1 and self.board[0][2] == 1:
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
        elif self.board[2][0] == 2 and self.board[1][1] == 2 and self.board[0][2] == 2:
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

def opponent_moves(game):
    actions = game.get_possible_next_moves()
    action = random.choice(actions)
    game.make_move(position=action, player='O')

def main():
    game = Game()
    agent = Agent(eta=0.9, gamma=0.9, epsilon=1.0)

    iter = 0
    game.print_board()
    while game.has_agent_won() == False and game.has_opponent_won() == False and game.is_it_a_draw() == False and iter < 10:
        done = agent.qlearning(game)
        game.print_board()
        if not done:
            opponent_moves(game)
            game.print_board()
        iter += 1
    
    if game.has_agent_won() == True:
        print("Agent has won!")
    elif game.has_opponent_won() == True:
        print("Opponent has won!")
    elif game.is_it_a_draw() == True:
        print("It's a draw!")
    
    #index = game.translate_board_state_to_index()
    #actions = game.get_possible_next_moves()
    #print("Index: {}\nList of actions: {}".format(index, actions))

    #game.make_move(position=(1,1), player='O')
    #game.print_board()
    #index = game.translate_board_state_to_index()
    #actions = game.get_possible_next_moves()
    #print("Index: {}\nList of actions: {}".format(index, actions))

    #game.make_move(position=(0,0), player='X')
    #game.print_board()
    #index = game.translate_board_state_to_index()
    #actions = game.get_possible_next_moves()
    #print("Index: {}\nList of actions: {}".format(index, actions))

    #game.make_move(position=(0,1), player='O')
    #game.print_board()
    #index = game.translate_board_state_to_index()
    #actions = game.get_possible_next_moves()
    #print("Index: {}\nList of actions: {}".format(index, actions))

    #game.make_move(position=(1,0), player='X')
    #game.print_board()
    #index = game.translate_board_state_to_index()
    #actions = game.get_possible_next_moves()
    #print("Index: {}\nList of actions: {}".format(index, actions))
    #game.make_move(position=(2,1), player='O')
    #game.print_board()

    #print("Has opponent won? {}".format(game.has_opponent_won()))
    


if __name__ == '__main__':
    main()