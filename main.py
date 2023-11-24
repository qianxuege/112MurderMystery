from cmu_graphics import *
from handDetection import runCamera

class Board:
    def __init__(self, width, height, rows, cols):
        self.width = width #500
        self.height = height #500
        self.rows = rows #7
        self.cols = cols #7
        self.cellBorderWidth = 1
        self.boardLeft = 100
        self.boardTop = 100
    
    def drawBoard(self):
        # width, height = self.width, self.height
        # rows, cols = self.rows, self.cols
        for row in range(self.rows):
            for col in range(self.cols):
                if 0 < row < (self.rows-1)  and 0 < col < (self.cols-1):
                    continue
                self.drawCell(row, col)
        self.drawBoardBorder()
    
    def drawBoardBorder(self):
        drawRect(self.boardLeft, self.boardTop, self.width, self.height, 
                 fill=None, border = 'black', 
                 borderWidth = 2*self.cellBorderWidth)
        cellSize = self.getCellSize()
        drawRect(self.boardLeft + cellSize, self.boardTop + cellSize, self.width - (2*cellSize), self.height - (2*cellSize),
                 fill=None, border = 'black',
                 borderWidth = self.cellBorderWidth)
    
    def drawCell(self, row, col):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellWidth = cellHeight = self.getCellSize()
        drawRect(cellLeft, cellTop, cellWidth, cellHeight, 
                 fill=None, border='black', 
                 borderWidth=self.cellBorderWidth)
    
    def getCellLeftTop(self, row, col):
        cellSize = self.getCellSize()
        cellLeft = col*cellSize + self.boardLeft
        cellTop = row*cellSize + self.boardTop
        return cellLeft, cellTop
    
    def getCellSize(self):
        cellSize = self.width/self.cols
        return cellSize
        
class Cell:
    def __init__(self, secretType, cellLeft, cellTop, cellSize):
        self.secretType = secretType
        self.cellLeft = cellLeft
        self.cellTop = cellTop
        self.cellSize = cellSize
    def __repr__(self):
        return f'{self.secretType}'       
        
    def __eq__(self, other):
        return (isinstance(other, Cell) and (self.secretType==other.secretType)
                and (self.cellLeft == other.cellLeft) and (self.cellTop == other.cellTop))
        
    def __hash__(self):
        return hash(str(self))
    
    def drawCellType(self):
        drawLabel(self.secretType, self.cellLeft + .5*self.cellSize, self.cellTop + .5*self.cellSize)
    ## print the labels (secretType)on the cell

class Secret(Cell):
    def __init__(self):
        self.secrets = []

class Rooms:
    def __init__(self, name, character, characterSecret, isRoom): # isRoom is a boolean value
        self.name = name
        self.accessible = True
        self.character = character
        # the secrets
        self.characterSecret = characterSecret
        self.isRoom = isRoom
        # ownserships
        self.characterSecretOwner = None
        self.isRoomOwner = None
        
    def __repr__(self):
        return f'{self.name}({self.character}, {self.characterSecretOwner}, {self.isRoomOwner})'
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other):
        return isinstance(other, Rooms) and (other.name == self.name)
    
    def buySecret(self, player):
        #
        pass
    
    def checkSecret(self):
        if self.characterSecretOwner == None:
            return f'You can buy a character secret'
        elif self.isRoomOwner == None:
            return f'You can buy a room secret'
        else:
            return None
    


        
    

def onAppStart(app):
    app.height = 700
    app.width = 800
    app.paused = True
    app.stepsPerSecond = 5
    

def redrawAll(app):
    # drawLabel('112 Murder Mystery', 200, 200)
    # drawLabel(app.paused, 200, 250)
    gameBoard = Board(500, 500, 7, 7)
    gameBoard.drawBoard()

def onKeyPress(app, key):
    if key == 's':
        print('running camera')
        # runCamera()
        print('finished running camera')
        
def onStep(app):
    app.paused = not app.paused

runApp()