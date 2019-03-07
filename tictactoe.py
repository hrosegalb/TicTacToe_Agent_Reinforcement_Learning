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

    def print_qmatrix(self):
        print(self.qmatrix)
        print(np.amax(self.qmatrix))
        print(np.histogram(self.qmatrix))
    
    def update_epsilon(self, delta):
        if self.epsilon - delta < 0.0:
            self.epsilon = 0.0
        else:
            self.epsilon -= delta

    
    def qlearning(self, game):
        action = None
        reward = 0
        done = False

        state = game.translate_board_state_to_index()

        if game.has_opponent_won() == True:
            self.qmatrix[self.prev_state, self.prev_action] = self.qmatrix[self.prev_state, self.prev_action] + self.eta * (reward + self.gamma * np.max(self.qmatrix[state, :]) - self.qmatrix[self.prev_state, self.prev_action])
            self.prev_state = None
            self.prev_action = None
            done = True
        elif game.is_it_a_draw() == True:
            reward = 0.5
            self.qmatrix[self.prev_state, self.prev_action] = self.qmatrix[self.prev_state, self.prev_action] + self.eta * (reward + self.gamma * np.max(self.qmatrix[state, :]) - self.qmatrix[self.prev_state, self.prev_action])
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
                    max_val = float('-inf')
                    top_index = None
                    for index in indices:
                        if self.qmatrix[state][index] > max_val:
                            max_val = self.qmatrix[state][index]
                            top_index = index
                    action = top_index
        
                action_idx = indices.index(action)
                game.make_move(actions[action_idx], self.player)
                new_state = game.translate_board_state_to_index()

                if game.has_agent_won() == True:
                    reward = 1
                    self.prev_state = None
                    self.prev_action = None
                    done = True
                elif game.is_it_a_draw() == True:
                    reward = 0.5
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

def opponent_moves(game):
    actions = game.get_possible_next_moves()
    if len(actions) > 0:
        action = random.choice(actions)
        game.make_move(position=action, player='O')
    

def main():
    game = Game()
    agent = Agent(eta=0.8, gamma=0.9, epsilon=1.0)

    stop = 100000
    epsilon_decay = 0.05
    m = 1000
    starting_player = 'X'
    agent_wins = 0
    for i in range(stop):
        if i == m:
            agent.update_epsilon(epsilon_decay)
            m += 100

        if starting_player == 'X':
            done = agent.qlearning(game)
            if not done:
                opponent_moves(game)
            else:
                if game.has_agent_won() == True:
                    print("Agent has won!")
                    agent_wins += 1
                elif game.has_opponent_won() == True:
                    print("Opponent has won!")
                elif game.is_it_a_draw() == True:
                    print("It's a draw!")
                
                game.reset_board()
                starting_player = 'O'
        else:
            opponent_moves(game)
            done = agent.qlearning(game)
            if done:
                if game.has_agent_won() == True:
                    print("Agent has won!")
                    agent_wins += 1
                elif game.has_opponent_won() == True:
                    print("Opponent has won!")
                elif game.is_it_a_draw() == True:
                    print("It's a draw!")
                
                game.reset_board()
                starting_player = 'X'

    agent.print_qmatrix()
    print("Number of agent wins: {}/{}\nWin Percentage: {}".format(agent_wins, stop, (agent_wins/stop)))
    

if __name__ == '__main__':
    main()
