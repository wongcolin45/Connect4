#Connect4 
#   1   2   3   4   5   6   7
# ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╗
# ║   ║   ║   ║   ║   ║   ║   ║
# ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣
# ║   ║   ║   ║   ║   ║   ║   ║
# ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣
# ║   ║   ║   ║ O ║   ║   ║   ║
# ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣
# ║   ║   ║   ║ x ║   ║   ║   ║
# ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣
# ║   ║   ║   ║ x ║   ║   ║   ║
# ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣
# ║   ║   ║   ║ x ║   ║   ║   ║
# ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╝

import time
import os
import math
infinity = math.inf


# Example Scoring Heuristics
# Win: Assign a very high positive score (e.g., +1000).
# Block Opponent Win: Assign a very high negative score (e.g., -1000).
# Three in a Row: Assign a high positive score (e.g., +10).
# Block Opponent Three in a Row: Assign a high negative score (e.g., -10).
# Two in a Row: Assign a moderate positive score (e.g., +5).
# Block Opponent Two in a Row: Assign a moderate negative score (e.g., -5).
# Center Control: Assign additional scores for pieces in the center columns.

class Board:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.grid = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.pause = 0.1;
        
    def display(self):
        os.system('clear')
        #showEvalution(self)
        #self.showInRows()
        print("  1   2   3   4   5   6   7")
        print("╔═══╦═══╦═══╦═══╦═══╦═══╦═══╗")
        for r in range(6):
            for c in range(7):
                print(f"║ {self.grid[r][c]} ",end = "")
            print("║",end="")
            print()
            if r != 5: 
                print("╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣")
            else:
                print("╚═══╩═══╩═══╩═══╩═══╩═══╩═══╝")
   
    def move(self, col, icon):
        j = 0
        while j < 5 and self.grid[j + 1][col] == ' ':
            self.grid[j][col] = icon
            self.grid[j][col] = ' '
            j += 1
        self.grid[j][col] = icon
        

    def possibleMoves(self):
        moves = [0,1,2,3,4,5,6]
        for c in range(self.cols):
            if self.grid[0][c] != ' ':
                moves.remove(c)
        return moves
            

    def inBounds(self, r, c):
        return 0 <= r and r < self.rows and 0 <= c and c < self.cols

    def checkCenter(self):
        score = 0
        for r in range(self.rows):
            if self.grid[r][3] == 'X':
                score += 1
            elif self.grid[r][3] == 'O':
                score -= 1
        return score

   
    def checkDirection(self, icon, r, c, x, y, streak):
        count = 0
        i = r + x
        j = c + y
        
        while self.inBounds(i,j) and self.grid[i][j] == icon and count < streak:
            i += x
            j += y
            count += 1
        return count == streak

    def showInRows(self):
        for i in range (1, 3):
            print(f"{i}s in a row is {self.checkInRow(i)}")  

    def isBlocked(self, opp, r, c, i, j, streak):
        #Check next point
        x = r + streak * i
        y = c + streak * j
        m = 2
        if not self.inBounds(x, y) or self.grid[x][y] == opp:
            m -= 1
        #check backwards point
        x += -1 * i
        y += -1 * j
        if not self.inBounds(x, y) or self.grid[x][y] == opp:
            m -= 1
        return m


    def checkInRow(self, streak):
        total = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] != ' ':
                    icon = self.grid[r][c]
                    #check all directions for point
                    for i in range(-1,2):
                        for j in range(-1,2):
                            if i == 0 and j == 0:
                                break
                            if self.checkDirection(icon, r, c, i, j, streak):
                                #reverse direction
                                i *= -1
                                j *= 1          
                                if icon == 'X':
                                    total += 1 * self.isBlocked('O', r, c, i, j, streak)                
                                else:
                                    total -= 1 * self.isBlocked('X', r, c, i, j, streak)                                                                  
        total = total / 2
        if (total < -1 or total > 1) and streak == 2:
            total *= 9
        
        return total

    def setGrid(self, grid):
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = grid[r][c]

    def getClone(self):
        clone = Board()
        clone.setGrid(self.grid)
        return clone           

def getOppositeTurn(icon):
    if icon == 'X':
        return 'O'
    return 'X'


def evaluate(position):
    score = 0
    #Winner
    score += 1000 * position.checkInRow(3)
    #3 in a row
    score += 100 * position.checkInRow(2)
    #2 in a row
    score += 10 * position.checkInRow(1)
    #center control
    score += 4 * position.checkCenter()
    return score


def getIcon(maximizingPlayer):
    if maximizingPlayer:
        return 'X'
    else:
        return 'O'


def minimax(position, depth, maximizingPlayer):
    if depth == 0 or position.checkInRow(3) != 0:
        return evaluate(position)
    elif maximizingPlayer:
        maxEval = -infinity
        for move in position.possibleMoves():
            child = position.getClone()
            child.move(move, getIcon(maximizingPlayer))
            eval_value = minimax(child, depth - 1, False)

            if eval_value > maxEval:
                maxEval = eval_value

            
        return maxEval
    else:
        minEval = infinity
        for move in position.possibleMoves():
            child = position.getClone()
            child.move(move, getIcon(maximizingPlayer))
            eval_value = minimax(child, depth - 1, True)
            
            if eval_value < minEval:
                minEval = eval_value

        return minEval   
    
    
def getBestMove(board, depth, maximizingPlayer):
    bestScore = -infinity if maximizingPlayer else infinity
    bestMove = None
    for move in board.possibleMoves():
        tempBoard = board.getClone()

        icon = getIcon(maximizingPlayer)

        tempBoard.move(move, icon)
        score = minimax(tempBoard, depth, not maximizingPlayer)
        if maximizingPlayer:
            if score > bestScore:
                bestScore = score
                bestMove = move
        else:
            if score < bestScore:
                bestScore = score
                bestMove = move
    return bestMove




                    
def showEvalution(board):
    print(f"evlaution is  {evaluate(board)}")

                        


class Connect4Game:  
    def __init__(self):
        self.board = Board()
        self.turn = 'X'
        
    
    def getMove(self):
        self.board.display()
        move = input("select a column:")
        return int(move) - 1
    
    def play(self):
        while self.board.checkInRow(3) == 0:
            
            self.board.display()
            
            if self.turn == 'X':
                move = getBestMove(self.board, 4 , True)
            else:
                move = self.getMove()

            self.board.move(move, self.turn)
            self.turn = 'X' if self.turn == 'O' else 'O'

            self.board.display()
            

            
        self.board.display()
        print("there is a winner!!!!!")
                





game = Connect4Game()
game.play()
