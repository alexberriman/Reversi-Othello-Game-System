import re
import math
import sys
import Reversi

# Constants for white/black (for when we reference the tuple)
(WHITE, BLACK, EMPTY) = (1,2,0)

# Board size (a x a)
BOARD_SIZE = 8

# ASCII char codes for the letter A and H
(LETTER_A, LETTER_H) = (97, 97 + BOARD_SIZE - 1)
    
    
class Gameboard():
    
    def __init__(self, gameboard=""):
        """ Object initialiser - let's set everything up """
        self.gameboard = self.createGameboard()
        self.players = self.players()
        
        # If we've passed through a gameboard to copy from, let's do it
        if gameboard != "":
            for piece in self.getPieces(gameboard):
                self.setPiece([piece[0], piece[1]], piece[2])
                
        # Otherwise, load the default pieces
        else:
            self.initGameboard()
        
    def createGameboard(self):
        """ Initialise the tuple which contains the gameboard data """
        return [[0 for col in range(self.size())] for row in range(self.size())]
        
    def players(self):
        """ Let's just store some basic information about the two players """
        return {
            WHITE: ["White", "w"],
            BLACK: ["Black", "b"],
        }
        
    def initGameboard(self):
        """
        Let's assign the starting discs to the board (we put them right in the middle of the board)
        nb: code redundancy, clean up
        """
        self.setPiece(self.coordsToString(int(self.size() / 2 - 1), int(self.size() / 2 - 1)), WHITE)
        self.setPiece(self.coordsToString(int(self.size() / 2 - 1), int(self.size() / 2)), BLACK)
        self.setPiece(self.coordsToString(int(self.size() / 2), int(self.size() / 2 - 1)), BLACK)
        self.setPiece(self.coordsToString(int(self.size() / 2), int(self.size() / 2)), WHITE)
    
    def getPos(self, pos):
        """ Converts a board position from a string (i.e. A5) to a set of coordinates """
        y = ord(pos[0:1].lower()) - LETTER_A
        x = int(pos[1:].lower()) - 1
        return [x,y]
        
    def coordsToString(self, y, x):
        """ Opposite of getPos: converts a set of coordinates to a board position as a string """
        letter = chr(LETTER_A + x)
        ord = y + 1
        
        return letter + str(ord)

    def setPiece(self, pos, piece):
        """ 
        Assign a piece to the board (if we pass through a string in the format '[A-Za-z]{1}[1-8]{1}'
        we convert to ordinals 
        """
        if (isinstance(pos, str)):
            pos = self.getPos(pos)
        
        self.gameboard[pos[0]][pos[1]] = piece
        
    def getPiece(self, pos):
        """ Returns the piece currently occupying a board position """
        if (isinstance(pos, str)):
            pos = self.getPos(pos)

        # Without the exception this errors when gameboard size is 6 (look in to)
        try:
            return self.gameboard[pos[0]][pos[1]]
        except:
            return
        
    def opponent(self, player):
        """ Given a player, it returns the opponent (i.e. if white is passed through will return black) """
        if player not in [WHITE, BLACK]:
            return
            
        return WHITE if player == BLACK else BLACK
        
    def gameboardPos(self, x, y, representation=1):
        """ Outputs the gameboard (different representation/formats are to display different sets of information) """
        pos = str(self.gameboard[x][y])
        
        if representation == 1:
            return "." if self.gameboard[x][y] == 0 else self.players[self.gameboard[x][y]][1]
        elif representation == 2:
            return str(chr(LETTER_A + y)) + str(x + 1)
            
    def outputGameboard(self, representation):
        """ Outputs the gameboard """
        boardString = " " * 3
        
        # Output the letters at the top
        for x in range(0, len(self.gameboard)):
            boardString += chr(LETTER_A + x) + " "
        boardString += "\n"
                
        # Output the game positions
        for x in range(0, len(self.gameboard)):
            boardString += str(x + 1) + " " * (3 - len(str(x + 1)))
            for y in range(0, len(self.gameboard[x])):
                boardString += self.gameboardPos(x,y, representation if representation not in [3] else 1) + " "
                
            if (representation == 3):
                boardString += "\t"
                for y in range(0, len(self.gameboard[x])):
                    boardString += self.gameboardPos(x, y, 2) + " "
            
            boardString += "\n"
        
        boardString += "\nScore: \n\tWhite: " + str(self.score(WHITE)) + "\n\tBlack: " + str(self.score(BLACK)) + "\n"
                
        return boardString
        
    def score(self, player):
        """ Returns the score (amount of pieces on the board for a given player) """
        score = 0
        for y in range(0, self.size()):
            for x in range(0, self.size()):
                if self.getPiece([x, y]) == player:
                    score += 1
                    
        return score
        
    def getPieces(self, gameboard):
        """ Retrieves all of the pieces of the gameboard """
        pieces = []
        for y in range(0, gameboard.size()):
            for x in range(0, gameboard.size()):
                piece = gameboard.getPiece([x, y])
                if piece != 0:
                    pieces.append([x,y, piece])
                    
        return pieces
        
    def emptyPieces(self):
        """ Returns the amount of empty squares currently on the board """
        return (self.size() * self.size()) - len(self.getPieces(self))
        
    def size(self):
        """ Returns the size of the board (AxA) """
        return LETTER_H - LETTER_A + 1
    
    def __str__(self):
        """ toString() method just outputs the gameboard """
        return self.outputGameboard(1)