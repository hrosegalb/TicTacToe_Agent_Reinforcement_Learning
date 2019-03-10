import numpy as np
import matplotlib.pyplot as plt

import random
from datetime import datetime

from agent import Agent
from game import Game


# Hannah Galbraith
# CS546
# 3/10/19
# Program 2

########################
# Auxiliary functions  #
# for tic-tac-toe game #
########################


def opponent_moves(game):
    """ :param game: Game object
       
        Picks action at random for opponent from a list of possible actions. """

    actions = game.get_possible_next_moves()
    if len(actions) > 0:
        action = random.choice(actions)
        game.make_move(position=action, player='O')


def train_agent(player, agent, game):
    """ :param player: 'X' or 'O'
        :param agent: Agent object
        :param game: Game object
        
        Functioned invoked during training of the agent. Plays one round of tic-tac-toe. If agent.qlearning 
        returns True, then game is done and method returns 'done' to the calling routine. Otherwise, it returns
        'in progress'. """

    result = "in progress"

    if player == 'X':
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


def play_game(player, agent, game):
        """ :param player: 'X' or 'O'
        :param agent: Agent object
        :param game: Game object
        
        Functioned invoked during assessment of the agent. Plays one round of tic-tac-toe. If agent.play_game 
        returns True, then game is done. Function will determine whether agent has won,
        opponent has won, or whether it's a draw. Depending on the outcome, it will set result to 'agent', 
        'opponent', or 'draw' and return that to the calling routine. Otherwise, it returns
        'in progress'. """

    result = "in progress"

    if player == 'X':
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


def assess_agent(player, agent, game, y_axis):
    """ :param player: 'X' or 'O'
        :param agent: Agent object
        :param game: Game object
        :param y_axis: list of integers 
        
        Function assesses agent's performance after a given training epoch. Plays 10 games against random agent
        and records the number of times the agent won. Appends result to 'y_axis' list and returns the 
        current player and y_axis to the calling routine. """

    num_games = 0
    agent_wins = 0 
    while num_games < 10:
        result = play_game(player, agent, game)
            
        if result == "agent":
            agent_wins += 1
            num_games += 1
        elif result != "in progress":
            num_games += 1

        if player == 'X':
            player = 'O'
        else:
            player = 'X'

    y_axis.append(agent_wins)

    return player, y_axis


def plot_progress(x_axis, y_axis):
    """ :param x_axis: list of integers
        :param y_axis: list of integers
        
        Creates a line graph of agent's progress during training. Saves the plot to a png file. """
    plt.style.use('seaborn-whitegrid')
    plt.plot(np.array(x_axis), np.array(y_axis))
    plt.title("Agent Progress Over Time")
    plt.xlabel("Epoch")
    plt.ylabel("Number of Winning Games out of 10")

    # This is just a bit of logic to get the filename in the format I want
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
        game.print_board()
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

    print("\nTime to try your hand against the agent. Play 10 games against it and see how you do.")
    print("Agent is 'X', you are 'O'.")
    print("\nGame #1:\n")

    game.reset_board()
    game.print_board()

    num_games = 0
    prev_game_num = 0
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
                if num_games < 10:
                    print("\nGame #{0}\n".format(num_games + 1))

                game.reset_board()

        else:
            print("Your turn.\n")   
            result = get_user_input(game)

            if result == "user":
                user_wins += 1
                num_games += 1
                if num_games < 10:
                    print("\nGame #{0}\n".format(num_games + 1))

                game.reset_board()
            elif result == "draw":
                num_draws += 1
                num_games += 1
                if num_games < 10:
                    print("\nGame #{0}\n".format(num_games + 1))

                game.reset_board()

        if player == 'X':
            player = 'O'
        else:
            player = 'X'

    print("Agent won {} game(s).".format(agent_wins))
    print("You won {} game(s).".format(user_wins))
    print("{} game(s) were a draw.".format(num_draws))
                

def main():
    game = Game()
    agent = Agent(eta=0.5, gamma=0.9, epsilon=0.1)

    num_epochs = 10
    stop = 10000
    epsilon_increase = 0.05
    m = 5000

    # Used for plotting agent's progress
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
