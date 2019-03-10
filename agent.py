import numpy as np
import random

from game import Game

# Hannah Galbraith
# CS546
# 3/10/19
# Program 2

#######################
# Agent class for     #
# tic-tac-toe game    #
######################


class Agent(object):
    
    def __init__(self, eta, gamma, epsilon):
        """ :param eta: float between [0.0, 1.0]
            :param gamma: float between (0.0, 1.0] 
            :param epsilon: float between (0.0, 1.0] 
            
            Initializes QMatrix and sets eta, gamma, epsilon, and player. 
            Initializes prev_state and prev_action to None. """

        self.qmatrix = np.zeros((3**9, 9))
        self.eta = eta
        self.gamma = gamma
        self.epsilon = epsilon
        self.player = 'X'
        self.prev_state = None
        self.prev_action = None


    def update_epsilon(self, delta):
        """ :param delta: float between [0.0, 1.0] 
            
            Increases epsilon by amount 'delta' provided that 
            epsilon + delta is not greater than 1.0. If so, it
            sets epsilon to 1.0. """
            
        if self.epsilon + delta > 1.0:
            self.epsilon = 1.0
        else:
            self.epsilon += delta

    
    def qlearning(self, game):
        """ :param game: Game object 
        
            Performs Qlearning algorithm. If it discovers that it has won, or if the opponent has won, or if there
            is a draw, it updates the QMatrix accordingly, sets 'done' to True, and returns 'done'. Otherwise,
            it keeps 'done' set to False and returns that. """

        action = None   # Column index for the QMatrix
        reward = 0      # Amount of reward it will receive for its next action
        done = False    # Keeps track of whether or not the game is finished

        # Gets the current state of the game
        # 'state' is an integer used as a row index for the QMatrix
        state = game.translate_board_state_to_index()

        # Check to see if current state is a winning state for the opponent or a draw.
        # If so, update QMatrix, set 'prev_state' and 'prev_action' to None, and set 'done' to True.
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
            # Get a list of possible next actions to take
            # Actions will be a list of tuples of integers representing positions on the board
            actions = game.get_possible_next_moves()

            if len(actions) > 0:
                # Translate the positions received into a list of column indices (0-8) for the QMatrix
                indices = self.translate_actions_to_indices(actions)

                # Choose an action either randomly or greedily
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
        
                # Make move and get new state
                action_idx = indices.index(action)
                game.make_move(actions[action_idx], self.player)
                new_state = game.translate_board_state_to_index()

                # Check to see whether agent has won or whether game is a draw.
                # If so, update reward, update QMatrix at position [state][action],
                # set 'prev_state' and 'prev_action' to None, and set 'done' to True
                if game.has_agent_won() == True:
                    reward = 1
                    self.qmatrix[state, action] = self.qmatrix[state, action] + self.eta * (reward + self.gamma * np.max(self.qmatrix[new_state, :]) - self.qmatrix[state, action])
                    self.prev_state = None
                    self.prev_action = None
                    done = True
                elif game.is_it_a_draw() == True:
                    reward = 0.5
                    self.qmatrix[state, action] = self.qmatrix[state, action] + self.eta * (reward + self.gamma * np.max(self.qmatrix[new_state, :]) - self.qmatrix[state, action])
                    self.prev_state = None
                    self.prev_action = None
                    done = True
                else:
                    # Otherwise, if game is still in progress, update QMatrix at position [state][action], and
                    # set 'prev_state' and 'prev_action' to 'state' and 'action' 
                    self.qmatrix[state, action] = self.qmatrix[state, action] + self.eta * (reward + self.gamma * np.max(self.qmatrix[new_state, :]) - self.qmatrix[state, action])
                    self.prev_state = state
                    self.prev_action = action

        return done


    def play_game(self, game):
        """ :param game: Game object
        
        This method is nearly identical to the Qlearning method except that no updates to the QMatrix are made.
        Method is invoked during assessment of agent and when agent is playing against a user. """

        action = None
        done = False

        state = game.translate_board_state_to_index()

        if game.has_opponent_won() == True or game.is_it_a_draw() == True:
            done = True
        else:
            actions = game.get_possible_next_moves()

            if len(actions) > 0:
                indices = self.translate_actions_to_indices(actions)

                # Choose next action greedily unless all values in the current row are
                # 0.0. In this case, choose randomly from the list of available actions.
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
        """ :param actions: list of integer tuples
        
            Method translates each position given in the 'actions' list into its corresponding column index in 
            the QMatrix. Returns a list of the indices. """

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