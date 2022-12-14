# bingo
My wife posed me the following question:  In a game of bingo with n cards in play, what is the average length of a game?  I attempted to answer this question in two ways.

1. Build a bingo simulator which takes as input the number of cards in play, the number of trials to run, and how often to print results, 
generates random bingo boards and runs random bingo games, and prints out the average length of game from that data.

2. Assume every board is in play and write a program to compute the average length of game in this scenario.

According to the law of large numbers, these two methods should agree in the limit as the number of boards increases.

# Bingo Simulator:

bingo_simulator.py takes three input parameters.  The first represents the number of bingo boards to be randomly generated.  The second represents the number of trials to run.  And the third says how many trials to run before printing a running average length so far.  For each trial, it randomly generates the inputted number of boards, simulates a game of bingo using these boards, and records the length of the game for the average.  This can be used to approximate the average length of game given the inputted number of boards by the law of large numbers.

# Bingo Calculator One:

This assumes that there is one bingo board in play and computes the average length of game in a manner similar to bingo calculator all, but including balls that are not on the board.

# Bingo Calculator All:

This assumes that all bingo boards are in play.  The program takes no input parameters.  If all boards are in play, the probability of a bingo for a given sequence of balls only depends on the number of each letter appearing in the sequence (by symmetry).  Thus, my program goes through all possible combinations of draws.  It labels them either as NO_BINGO, ROW_BINGO, COLUMN_BINGO, or MULTIPLE_BINGO (note that in this scenario diagonal bingos are equivalent to column bingos).  It does not score no bingo for obvious reasons.  It does not score multiple bingo because the game would have ended before this scenario arose.  For row bingo and column bingos, it computes the probability of this distribution of ball counts occurring.  It tallies these weights and computes the expected value using them.  An explanation of my computation and some sample calculations appear at the end of the output.
