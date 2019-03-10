import numpy as np
import random

from game import Game

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