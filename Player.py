import random
import numpy
from copy import deepcopy

class Player:
    def __init__(self, team):
        ## team = 1 or -1, 1 for white, -1 for black
        self.team = team
        self.opponent_team = team * -1
        self.moves = []
        

    def add_move(self, board): # use the board function to find all possible moves for the current player
        self.moves = board.legal_moves(self.team)
    
    def next_move(self, board):
        # by default the play class makes random moves
        self.add_move(board)
        #print("player moves", self.moves)
        result = random.choice(self.moves) 
        self.clear_moves() # clears the move so future moves are not disrupted
        return result
    
    def clear_moves(self):
        # modifier method for clearing moves
        self.moves = []

    def check_turn(self, board):
        # helper function for checking if it is the player's turn
        if (board.turn != self.team):
            print("Not this player's turn Error!")
            return False
        else:
            return True


class Minimax_Player(Player): 
    def eval_board(self, board):
        # Heuristic function for minimax
        # Don't question, we just made this up
        score = 0
        pieces = board.allpieces()
        #print("pieces = ", pieces)
        for p in pieces:
            tempscore += p[0].value[p[0].type-1]
            score += tempscore
        #print("score = ", score)
        return score

    def min_maxN(self, board, n):
        # requires that self.moves contains legal moves available for the current player
        scores = []   ## scoring for each move, positive is good for white, negative is good for black        
        best_move = 0
    
        
        for move in self.moves:
            
            # make copy of the board position so we are not changing the actual board when trying moves
            tempboard = deepcopy(board)
            tempboard.push(move)
            
            if n > 0:  # look ahead n moves opponent player plays
                temp_best_move = self.min_maxN(tempboard,n-1)
                tempboard.push(temp_best_move)

            scores.append(self.eval_board(tempboard))   # score corresponse to the move indices
            

        if self.team == 1:
            best_move = self.moves[scores.index(max(scores))] # max() finds the highest positive score
        else: # that is self.team == -1
            best_move = self.moves[scores.index(min(scores))] # min() finds the lowest positive score

        return best_move
    
    def next_move(self, board):
        self.add_move(board)
        #print("available moves", self.moves)
        bestmove = self.min_maxN(board, 2)
        self.clear_moves()
        return bestmove
        

class MinimaxAlphaBeta_Player(Player): 
    def __init__(self, team, depth):
        super().__init__(team)
        self.MAX = numpy.Inf  #initialize to be positive infinity
        self.MIN = numpy.NINF #initialize to be negative infinity
        self.depth = depth # number of moves we look ahead
        # flip the position values for black because black is on the other side of the board
        self.whitePawnEval = [
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-3.0], [0,0,-4.0], [0,0,-4.0], [0,0,-5.0], [0,0,-6.0], [0,0,-5.0], [0,0,-4.0], [0,0,-4.0], [0,0,-3.0]],
[[0,0,-2.0], [0,0,-3.0], [0,0,-3.0], [0,0,-4.0], [0,0,-5.0], [0,0,-4.0], [0,0,-3.0], [0,0,-3.0], [0,0,2.0]],
[[0,0,-1.0], [0,0,-2.0], [0,0,-2.0], [0,0,-3.0], [0,0,-4.0], [0,0,-3.0], [0,0,-2.0], [0,0,-2.0], [0,0,-1.0]],
[[0,0,2.0],  [0,0,1.0], [0,0, 1.0], [0,0, 0], [0,0, 0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0]],
[[0,0,3.0],  [0,0,2.0],  [0,0,1.0], [0,0, 1.0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0],  [0,0,3.0]]]
        self.blackPawnval = list(reversed(self.whitePawnEval)) 
        self.whiteKingEval = [
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-3.0], [0,0,-4.0], [0,0,-4.0], [0,0,-5.0], [0,0,-6.0], [0,0,-5.0], [0,0,-4.0], [0,0,-4.0], [0,0,-3.0]],
[[0,0,-2.0], [0,0,-3.0], [0,0,-3.0], [0,0,-4.0], [0,0,-5.0], [0,0,-4.0], [0,0,-3.0], [0,0,-3.0], [0,0,2.0]],
[[0,0,-1.0], [0,0,-2.0], [0,0,-2.0], [0,0,-3.0], [0,0,-4.0], [0,0,-3.0], [0,0,-2.0], [0,0,-2.0], [0,0,-1.0]],
[[0,0,2.0],  [0,0,1.0], [0,0, 1.0], [0,0, 0], [0,0, 0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0]],
[[0,0,3.0],  [0,0,2.0],  [0,0,1.0], [0,0, 1.0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0],  [0,0,3.0]]]
        self.blackKingEval = list(reversed(self.whiteKingEval))
        self.whiteFortressEval = [
[[0,0,-4], [0,0,-5], [0,0,-5], [0,0,-6], [0,0,-7], [0,0,-6], [0,0,-5], [0,0,-5], [0,0,-4]],
[[0,0,-4], [0,0,-5], [0,0,-5], [0,0,-6], [0,0,-7], [0,0,-6], [0,0,-5], [0,0,-5], [0,0,-4]],
[[0,0,-4], [0,0,-5], [0,0,-5], [0,0,-6], [0,0,-7], [0,0,-6], [0,0,-5], [0,0,-5], [0,0,-4]],
[[0,0,-5], [0,0,-2], [0,0,-3], [0,0,-3], [0,0,-3], [0,0,-3], [0,0,-3], [0,0,-2], [0,0,-5]],
[[0,0,-3], [0,0,-4], [0,0,-4], [0,0,-2], [0,0, 0], [0,0,-2], [0,0,-4], [0,0,-4], [0,0,-3]],
[[0,0,-2], [0,0, 0], [0,0, 3], [0,0, 3], [0,0, 4], [0,0, 3], [0,0, 3], [0,0, 0], [0,0,-2]],
[[0,0,-1], [0,0, 2], [0,0, 2], [0,0, 2], [0,0, 5], [0,0, 2], [0,0, 2], [0,0, 2], [0,0,-1]],
[[0,0, 1], [0,0, 2], [0,0, 2], [0,0, 3], [0,0, 6], [0,0, 3], [0,0, 2], [0,0, 2], [0,0, 1]],
[[0,0, 3], [0,0, 4], [0,0, 4], [0,0, 4], [0,0, 5], [0,0, 4], [0,0, 4], [0,0, 4], [0,0, 3]]]
        self.blackFortressEval = list(reversed(self.whiteFortressEval))
        self.whiteArcherEval = [
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-3.0], [0,0,-4.0], [0,0,-4.0], [0,0,-5.0], [0,0,-6.0], [0,0,-5.0], [0,0,-4.0], [0,0,-4.0], [0,0,-3.0]],
[[0,0,-2.0], [0,0,-3.0], [0,0,-3.0], [0,0,-4.0], [0,0,-5.0], [0,0,-4.0], [0,0,-3.0], [0,0,-3.0], [0,0,2.0]],
[[0,0,-1.0], [0,0,-2.0], [0,0,-2.0], [0,0,-3.0], [0,0,-4.0], [0,0,-3.0], [0,0,-2.0], [0,0,-2.0], [0,0,-1.0]],
[[0,0,2.0],  [0,0,1.0], [0,0, 1.0], [0,0, 0], [0,0, 0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0]],
[[0,0,3.0],  [0,0,2.0],  [0,0,1.0], [0,0, 1.0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0],  [0,0,3.0]]]
        self.blackArcherEval = list(reversed(self.whiteArcherEval))
        self.whiteLieutenantEval = [
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-3.0], [0,0,-4.0], [0,0,-4.0], [0,0,-5.0], [0,0,-6.0], [0,0,-5.0], [0,0,-4.0], [0,0,-4.0], [0,0,-3.0]],
[[0,0,-2.0], [0,0,-3.0], [0,0,-3.0], [0,0,-4.0], [0,0,-5.0], [0,0,-4.0], [0,0,-3.0], [0,0,-3.0], [0,0,2.0]],
[[0,0,-1.0], [0,0,-2.0], [0,0,-2.0], [0,0,-3.0], [0,0,-4.0], [0,0,-3.0], [0,0,-2.0], [0,0,-2.0], [0,0,-1.0]],
[[0,0,2.0],  [0,0,1.0], [0,0, 1.0], [0,0, 0], [0,0, 0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0]],
[[0,0,3.0],  [0,0,2.0],  [0,0,1.0], [0,0, 1.0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0],  [0,0,3.0]]]
        self.blackLieutenantEval = list(reversed(self.whiteLieutenantEval))
        self.whiteGeneralEval = [
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-3.0], [0,0,-4.0], [0,0,-4.0], [0,0,-5.0], [0,0,-6.0], [0,0,-5.0], [0,0,-4.0], [0,0,-4.0], [0,0,-3.0]],
[[0,0,-2.0], [0,0,-3.0], [0,0,-3.0], [0,0,-4.0], [0,0,-5.0], [0,0,-4.0], [0,0,-3.0], [0,0,-3.0], [0,0,2.0]],
[[0,0,-1.0], [0,0,-2.0], [0,0,-2.0], [0,0,-3.0], [0,0,-4.0], [0,0,-3.0], [0,0,-2.0], [0,0,-2.0], [0,0,-1.0]],
[[0,0,2.0],  [0,0,1.0], [0,0, 1.0], [0,0, 0], [0,0, 0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0]],
[[0,0,3.0],  [0,0,2.0],  [0,0,1.0], [0,0, 1.0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0],  [0,0,3.0]]]
        self.blackGeneralEval = list(reversed(self.whiteGeneralEval))
        self.whiteCaptainEval = [
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-3.0], [0,0,-4.0], [0,0,-4.0], [0,0,-5.0], [0,0,-6.0], [0,0,-5.0], [0,0,-4.0], [0,0,-4.0], [0,0,-3.0]],
[[0,0,-2.0], [0,0,-3.0], [0,0,-3.0], [0,0,-4.0], [0,0,-5.0], [0,0,-4.0], [0,0,-3.0], [0,0,-3.0], [0,0,2.0]],
[[0,0,-1.0], [0,0,-2.0], [0,0,-2.0], [0,0,-3.0], [0,0,-4.0], [0,0,-3.0], [0,0,-2.0], [0,0,-2.0], [0,0,-1.0]],
[[0,0,2.0],  [0,0,1.0], [0,0, 1.0], [0,0, 0], [0,0, 0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0]],
[[0,0,3.0],  [0,0,2.0],  [0,0,1.0], [0,0, 1.0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0],  [0,0,3.0]]]
        self.blackCaptainEval = list(reversed(self.whiteCaptainEval))
        self.whiteCannonEval = [
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-3.0], [0,0,-4.0], [0,0,-4.0], [0,0,-5.0], [0,0,-6.0], [0,0,-5.0], [0,0,-4.0], [0,0,-4.0], [0,0,-3.0]],
[[0,0,-2.0], [0,0,-3.0], [0,0,-3.0], [0,0,-4.0], [0,0,-5.0], [0,0,-4.0], [0,0,-3.0], [0,0,-3.0], [0,0,2.0]],
[[0,0,-1.0], [0,0,-2.0], [0,0,-2.0], [0,0,-3.0], [0,0,-4.0], [0,0,-3.0], [0,0,-2.0], [0,0,-2.0], [0,0,-1.0]],
[[0,0,2.0],  [0,0,1.0], [0,0, 1.0], [0,0, 0], [0,0, 0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0]],
[[0,0,3.0],  [0,0,2.0],  [0,0,1.0], [0,0, 1.0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0],  [0,0,3.0]]]
        self.blackCannonEval = list(reversed(self.whiteCannonEval))
        self.whiteMusketeerEval = [
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-3.0], [0,0,-4.0], [0,0,-4.0], [0,0,-5.0], [0,0,-6.0], [0,0,-5.0], [0,0,-4.0], [0,0,-4.0], [0,0,-3.0]],
[[0,0,-2.0], [0,0,-3.0], [0,0,-3.0], [0,0,-4.0], [0,0,-5.0], [0,0,-4.0], [0,0,-3.0], [0,0,-3.0], [0,0,2.0]],
[[0,0,-1.0], [0,0,-2.0], [0,0,-2.0], [0,0,-3.0], [0,0,-4.0], [0,0,-3.0], [0,0,-2.0], [0,0,-2.0], [0,0,-1.0]],
[[0,0,2.0],  [0,0,1.0], [0,0, 1.0], [0,0, 0], [0,0, 0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0]],
[[0,0,3.0],  [0,0,2.0],  [0,0,1.0], [0,0, 1.0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0],  [0,0,3.0]]]
        self.blackMusketeerEval = list(reversed(self.whiteMusketeerEval))
        """ Backup Position Values
            [-4.0, -5.0, -5.0, -6.0, -7.0, -6.0, -5.0, -5.0, -4.0],
            [-4.0, -5.0, -5.0, -6.0, -7.0, -6.0, -5.0, -5.0, -4.0],
            [-4.0, -5.0, -5.0, -6.0, -7.0, -6.0, -5.0, -5.0, -4.0],
            [-4.0, -5.0, -5.0, -6.0, -7.0, -6.0, -5.0, -5.0, -4.0],
            [-3.0, -4.0, -4.0, -5.0, -6.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -5.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -3.0, -4.0, -3.0, -2.0, -2.0, -1.0],
            [ 2.0,  1.0,  1.0,  0,  0,  0,  1.0,  1.0,  2.0],
            [ 3.0,  2.0,  1.0,  1.0,  0,  1.0,  1.0,  2.0,  3.0]]
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-4.0], [0,0,-5.0], [0,0,-5.0], [0,0,-6.0], [0,0,-7.0], [0,0,-6.0], [0,0,-5.0], [0,0,-5.0], [0,0,-4.0]],
[[0,0,-3.0], [0,0,-4.0], [0,0,-4.0], [0,0,-5.0], [0,0,-6.0], [0,0,-5.0], [0,0,-4.0], [0,0,-4.0], [0,0,-3.0]],
[[0,0,-2.0], [0,0,-3.0], [0,0,-3.0], [0,0,-4.0], [0,0,-5.0], [0,0,-4.0], [0,0,-3.0], [0,0,-3.0], [0,0,2.0]],
[[0,0,-1.0], [0,0,-2.0], [0,0,-2.0], [0,0,-3.0], [0,0,-4.0], [0,0,-3.0], [0,0,-2.0], [0,0,-2.0], [0,0,-1.0]],
[[0,0,2.0],  [0,0,1.0], [0,0, 1.0], [0,0, 0], [0,0, 0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0]],
[[0,0,3.0],  [0,0,2.0],  [0,0,1.0], [0,0, 1.0],  [0,0,0],  [0,0,1.0],  [0,0,1.0],  [0,0,2.0],  [0,0,3.0]]]
        """
        # Put the position values in dictionary for easy access
        self.WhitePiecePositionValue = {1:self.whitePawnEval,
                                        2:self.whiteKingEval,
                                        3:self.whiteFortressEval,
                                        4:self.whiteArcherEval,
                                        5:self.whiteLieutenantEval,
                                        6:self.whiteGeneralEval,
                                        7:self.whiteCaptainEval,
                                        8:self.whiteCannonEval,
                                        9:self.whiteMusketeerEval}
        self.BlackPiecePositionValue = {1:self.blackPawnEval,
                                        2:self.blackKingEval,
                                        3:self.blackFortressEval,
                                        4:self.blackArcherEval,
                                        5:self.blackLieutenantEval,
                                        6:self.blackGeneralEval,
                                        7:self.blackCaptainEval,
                                        8:self.blackCannonEval,
                                        9:self.blackMusketeerEval}
        self.PiecePositionValue = {1:self.WhitePiecePositionValue, 
                                  -1:self.BlackPiecePositionValue}

    def eval_board_backup(self, board):
        # Backup code for eval_board before re-designing the function
        # Just in case program crashes
        score = 0
        pieces = board.allpieces()
        #print("pieces = ", pieces)
        for p in pieces:
            #print(p)
            score += p[0].value[p[0].type-1]
        return score

    def eval_board(self, board):
        # Heuristic function for minimax
        # representing how favorable the current board position is
        # positive means good for white, negative means good for black
        # return a float number 
        totalscore = 0
        pieces = board.allpieces()
        #print("pieces = ", pieces)
        for p in pieces: # p[0] is a piece object, p[1] is [y,x,z] position of the piece object on board
            totalscore += p[0].team * (p[0].value[p[0].type-1] + \
            self.PiecePositionValue[p[0].team][p[0].type][p[1][0]][p[1][1]][p[1][2]])
        return totalscore

    def MinimaxAlphaBeta(self, depth, board, alpha, beta, maximizingplayer):
        # requires that self.moves contains legal moves available for the current player
        # depth is number of moves look ahead 
        # maximizingplayer is a boolean 
        if (depth == 0):
            return -self.eval_board(board)
        if maximizingplayer: #initialize to min for maximizing
            bestmove_score = self.MIN 
            for move in self.moves:
                # make copy of the board position so we are not changing the actual board when trying moves
                tempboard = deepcopy(board)
                tempboard.push(move)
                tempmove_score = self.MinimaxAlphaBeta(depth - 1, tempboard, alpha, beta, False)
                #temp.push(temp_best_move)
                bestmove_score = max(bestmove_score, tempmove_score)
                alpha = max(alpha, tempmove_score) # update alpha
                if beta <= alpha: # the check condition for pruning the move or not
                    return bestmove_score # prune, stop checking more moves in the for loop  
        else: 
            bestmove_score = self.MAX # which is the minimizingplayer, initialize to max for minimizing
            for move in self.moves:
                # make copy of the board position so we are not changing the actual board when trying moves
                tempboard = deepcopy(board)
                tempboard.push(move)
                tempmove_score = self.MinimaxAlphaBeta(depth - 1, tempboard, alpha, beta, True)
                #temp.push(temp_best_move)
                bestmove_score = min(bestmove_score, tempmove_score)
                alpha = min(alpha, tempmove_score) # update alpha
                if beta <= alpha: # the check condition for pruning the move or not
                    return bestmove_score # prune, stop checking more moves in the for loop
    
    def MinimaxAlphaBetaDriver(self, depth, board):
        # driver function for calling the recursive Minimax Alphabeta
        # depth is how many moves we look ahead in the future
        bestmove = self.moves[0]
        bestmove_score = self.MIN #initialize worse score to optimize
        for move in self.moves:
            # make copy of the board position so we are not changing the actual board when trying moves
            tempboard = deepcopy(board)
            tempboard.push(move)
            tempmove_score = self.MinimaxAlphaBeta(depth - 1, tempboard, self.MAX, self.MIN, False)
            if (tempmove_score > bestmove_score): 
                # if the current checked move has better score than the best move on record
                bestmove_score = tempmove_score # update best score 
                bestmove = move # update bestmove
        return bestmove

    def next_move(self, board):
        self.add_move(board)
        bestmove = self.MinimaxAlphaBetaDriver(self.depth, board)
        self.clear_moves()
        return bestmove


## GUI class for human player
class HumanPlayer():
    def __init__(self, team):
        super().__init__(team)
    
    def GetHumanInput(self):
        pass

    def next_move(self, board):
        pass
