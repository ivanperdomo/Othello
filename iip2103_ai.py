#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to
complete and submit.

@author: Ivan Perdomo, iip2103
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cached = {} #STATE : UTILITY

def compute_utility(board, color):
    """
    Return the utility of the given board state
    (represented as a tuple of tuples) from the perspective
    of the player "color" (1 for dark, 2 for light)
    """

    scores = get_score(board)

    if color== 1:
        return scores[0]-scores[1]
    else:
        return scores[1]-scores[0]

############ MINIMAX ###############################
#MAX = 1
#MIN = 2
def minimax_min_node(board, color): #returns lowest attainable utility
    if color == 1 : opponent = 2
    else : opponent = 1
    if board in cached:
        return cached[board]
    if not get_possible_moves(board,color):
        return compute_utility(board,color)
    v = float("Inf")
    for move in get_possible_moves(board,color):
        #new_move = play_move(board,color,move[0],move[1])
        v = min(v,minimax_max_node(play_move(board,color,move[0],move[1]),opponent))
    return v
def minimax_max_node(board, color): #returns highest possible utility
    if color == 1 : opponent = 2
    else: opponent = 1
    if board in cached:
        return cached[board]
    if not get_possible_moves(board,color):
        return compute_utility(board,color)
    v = float("-Inf")
    for move in get_possible_moves(board,color):
        #new_move = play_move(board,color,move[0],move[1])
        v = max(v,minimax_min_node(play_move(board,color,move[0],move[1]),opponent))
    return v

def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    moves = []
    for option in get_possible_moves(board,color): #get all minimizer moves
        new_move = play_move(board,color,option[0],option[1])
        utility = minimax_max_node(new_move,color)
        if new_move not in cached:
            cached[new_move] = utility
        moves.append([(option[0], option[1]), utility])
    sorted_options = sorted(moves, key = lambda x: x[1])
    return sorted_options[0][0]

############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit):
    if color == 1 : opponent = 2
    else: opponent = 1
    level += 1
    if board in cached:
        return cached[board]
    if not get_possible_moves(board,color) or level == limit:
        return compute_utility(board,color)

    #elif board in cached:
    #    return cached[board]

    v = float("Inf")
    for move in get_possible_moves(board,color):
        new_move = play_move(board, color, move[0], move[1])
        v = min(v,alphabeta_max_node(new_move,opponent,alpha,beta,level,limit))
        if v <= alpha : return v
        beta = min(beta,v)
    return v


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    if color == 1 : opponent = 2
    else: opponent = 1
    level += 1
    if board in cached:
        return cached[board]

    if not get_possible_moves(board,color) or level == limit:
        return compute_utility(board,color)

    v = float("-Inf")
    for move in get_possible_moves(board, color) :
        new_move = play_move(board, color, move[0], move[1])
        v = max(v, alphabeta_min_node(new_move, opponent, alpha, beta, level, limit))
        if v >= beta : return v
        alpha = max(alpha, v)
    return v


def select_move_alphabeta(board, color):
    moves = []
    node_ordering = []
    alpha = float("-Inf")
    beta = float("Inf")

    for option in get_possible_moves(board,color):
        node_ordering.append([(option[0],option[1]),compute_utility(play_move(board,color,option[0],option[1]),color)])
    node_ordering = sorted(node_ordering, key = lambda x : x[1], reverse = True)
    for option in node_ordering:
    #for option in get_possible_moves(board, color) :  # get all minimizer moves
        new_move = play_move(board, color, option[0][0], option[0][1])
        utility = alphabeta_max_node(new_move, color,alpha,beta, 0, 4)
        if new_move not in cached:
            cached[new_move] = utility
        moves.append([(option[0][0], option[0][1]), utility])
    sorted_options = sorted(moves, key = lambda x : x[1])

    return sorted_options[0][0]


####################################################

def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Minimax AI") # First line is the name of this AI
    color = int(input()) # Then we read the color: 1 for dark (goes first),
                         # 2 for light.

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager

            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()