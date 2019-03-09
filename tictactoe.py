import numpy as np
import matplotlib.pyplot as plt

import random
from datetime import datetime

class Agent(object):
    
    def __init__(self, eta, gamma, epsilon):
        self.qmatrix = np.zeros((3**9, 9))
        self.eta = eta
        self.gamma = gamma
        self.epsilon = epsilon
        self.player = 'X'
        self.prev_state = None
        self.prev_action = None


    def update_epsilon(self, delta):
        if self.epsilon + delta > 1.0:
            self.epsilon = 1.0
        else:
            self.epsilon += delta

    
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

                unique_vals = np.unique(self.qmatrix[state, :])
                if random.random() < (1 - self.epsilon):
                    action = random.choice(indices)
                elif len(unique_vals) == 1 and unique_vals[0] == 0.0:
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


    def play_game(self, game):
        action = None
        done = False
        self.prev_state = None
        self.prev_action = None

        state = game.translate_board_state_to_index()

        if game.has_opponent_won() == True or game.is_it_a_draw() == True:
            done = True
        else:
            actions = game.get_possible_next_moves()

            if len(actions) > 0:
                indices = self.translate_actions_to_indices(actions)

                unique_vals = np.unique(self.qmatrix[state, :])
                if (len(unique_vals) == 1 and unique_vals[0] == 0.0):
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

                if game.has_agent_won() == True or game.is_it_a_draw() == True:
                    done = True

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


def opponent_moves(game):
    actions = game.get_possible_next_moves()
    if len(actions) > 0:
        action = random.choice(actions)
        game.make_move(position=action, player='O')


def train_agent(starting_player, agent, game):
    result = "in progress"

    if starting_player == 'X':
        done = agent.qlearning(game)
        if not done:
            opponent_moves(game)
        else:
            result = "done"
            game.reset_board()
    else:
        opponent_moves(game)
        done = agent.qlearning(game)
        if done:
            result = "done"  
            game.reset_board()

    return result


def play_game(starting_player, agent, game):
    result = "in progress"

    if starting_player == 'X':
        done = agent.play_game(game)
        if not done:
            opponent_moves(game)
        else:
            if game.has_agent_won() == True:
                result = "agent"
            elif game.has_opponent_won() == True:
                result = "opponent"
            elif game.is_it_a_draw() == True:
                result = "draw"
                
            game.reset_board()
    else:
        opponent_moves(game)
        done = agent.play_game(game)
        if done:
            if game.has_agent_won() == True:
                result = "agent"
            elif game.has_opponent_won() == True:
                result = "opponent"
            elif game.is_it_a_draw() == True:
                result = "draw"
                
            game.reset_board()

    return result


def assess_agent(starting_player, agent, game, y_axis, epoch=-1):
    num_games = 0
    agent_wins = 0 
    while num_games < 10:
        result = play_game(starting_player, agent, game)
            
        if result == "agent":
            agent_wins += 1
            num_games += 1
        elif result != "in progress":
            num_games += 1

        if starting_player == 'X':
            starting_player = 'O'
        else:
            starting_player = 'X'

    if epoch > -1:
        print("After {} epoch(s), agent has won {} out of {} games.".format(epoch + 1, agent_wins, num_games))
    else:
        print("Without training, agent won {} of {} games.".format(agent_wins, num_games))
    y_axis.append(agent_wins)
    
    return starting_player, y_axis


def plot_progress(x_axis, y_axis):
    plt.style.use('seaborn-whitegrid')
    plt.plot(np.array(x_axis), np.array(y_axis))
    plt.title("Agent Progress Over Time")
    plt.xlabel("Epoch")
    plt.ylabel("Number of Winning Games out of 10")

    fname = "agent_wins_" + str(datetime.now())
    fparts = fname.split(' ')
    time = fparts[1].split('.')
    fparts = [fparts[0], time[0]]
    fname = "_".join(fparts)
    plt.savefig(fname)
    plt.close()


def get_user_input(game):
    result = "in progress"

    input_done = False
    while not input_done:
        print("Please select the grid element you want by typing in the following format: row,col")
        print("Remember that the grid is 0-based; e.g., row 1, column 1 would be '0,0'")
        user_input = input()
        user_input = user_input.strip()

        if len(user_input) != 3:
            print("Sorry, your answer is in the wrong format. Please try again.")
        else:
            user_input = user_input.split(',')
            
            try:
                user_input = [int(user_input[0]), int(user_input[1])]
                
                if (user_input[0] < 0 or user_input[0] > 2) or (user_input[1] < 0 or user_input[1] > 2):
                    print("The input you have entered is out of range. Please try again.")
                else:
                    position = (user_input[0], user_input[1])
                    result = game.make_move(position, 'O')

                    if result == True:
                        game.print_board()
                        input_done = True

                        if game.has_opponent_won() == True:
                            print("You won!")
                            result = "user"
                        elif game.is_it_a_draw() == True:
                            print("It's a draw.")
                            result = "draw"
                    else:
                        print("Sorry, the move you requested is not a valid move. Please try again.")
            except:
                print("You have entered something that is not a number. Please try again.")

    return result

def play_against_user(agent, game):
    player = 'X'

    print("Time to try your hand against the agent. Play 10 games against it and see how you do.")
    print("Agent is 'X', you are 'O'.")

    game.reset_board()
    game.print_board()

    num_games = 0
    agent_wins = 0
    user_wins = 0
    num_draws = 0
    while num_games < 10:
        if player == 'X':
            print("Agent's turn.")
            done = agent.play_game(game)
            game.print_board()

            if done:
                if game.has_agent_won() == True:
                    print("Agent has won!")
                    agent_wins += 1
                elif game.has_opponent_won() == True:
                    print("You won!")
                    user_wins += 1
                elif game.is_it_a_draw() == True:
                    print("It's a draw.")
                    num_draws += 1

                num_games += 1
                game.reset_board()
        else:
            print("Your turn.\n")
            result = get_user_input(game)
            game.print_board()

            if result == "user":
                user_wins += 1
                num_games += 1
                game.reset_board()
            elif result == "draw":
                num_draws += 1
                num_games += 1
                game.reset_board()

        if player == 'X':
            player = 'O'
        else:
            player = 'X'

    print("Agent won {} games.".format(agent_wins))
    print("You won {} games.".format(user_wins))
    print("{} games were a draw.".format(num_draws))
                



def main():
    game = Game()
    agent = Agent(eta=0.5, gamma=0.9, epsilon=0.1)

    num_epochs = 10
    stop = 10000
    epsilon_increase = 0.05
    m = 5000

    # Used for plotting
    x_axis = [i for i in range(num_epochs + 1)]
    y_axis = []
       
    starting_player = 'X'
    starting_player, y_axis = assess_agent(starting_player, agent, game, y_axis)
    for epoch in range(num_epochs):
        game.reset_board()
        num_training_games = 0
        while num_training_games < stop:
            if num_training_games == m:
                agent.update_epsilon(epsilon_increase)

            result = train_agent(starting_player, agent, game)
            if result == "done":
                num_training_games += 1

            if starting_player == 'X':
                starting_player = 'O'
            else:
                starting_player = 'X'

        game.reset_board()
        starting_player, y_axis = assess_agent(starting_player, agent, game, y_axis, epoch)
    
    plot_progress(x_axis, y_axis)
    play_against_user(agent, game)
        
    

if __name__ == '__main__':
    main()
