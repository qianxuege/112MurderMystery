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
        self.cellList = []
        self.cellDict = dict()
        self.isFirstIteration = True
        self.player1 = None
    
    def drawBoard(self):
        cellId = 0
        for row in range(self.rows):
            for col in range(self.cols):
                # leave the middle of the board blank
                if 0 < row < (self.rows-1)  and 0 < col < (self.cols-1):
                    continue
                self.drawCell(row, col, cellId) # pass in an id
                cellId += 1
        self.drawBoardBorder()
        
        # creates a dictionary of the cells in the correct order after board is drawn
        if self.isFirstIteration==True:
            self.updateCellList()
            # initiates player1 after the cellDict is updated
            self.player1 = Player('player1', self.cellDict, -10) # -10 is the diff in x position
            self.isFirstIteration = False
        else:
            # draw Player1
            self.player1.drawPlayer()
        
        
    
    def drawBoardBorder(self):
        drawRect(self.boardLeft, self.boardTop, self.width, self.height, 
                 fill=None, border = 'black', 
                 borderWidth = 2*self.cellBorderWidth)
        cellSize = self.getCellSize()
        drawRect(self.boardLeft + cellSize, self.boardTop + cellSize, self.width - (2*cellSize), self.height - (2*cellSize),
                 fill=None, border = 'black',
                 borderWidth = self.cellBorderWidth)
    
    def drawCell(self, row, col, cellId):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellSize = self.getCellSize()
        # these are the weapon's clue cells
        if cellId in {13, 7, 3, 10, 16, 20}:
            cellName = Cell(cellId, 'weapon', cellLeft, cellTop, cellSize)
            self.cellList.append(cellName)
        # these are the cells that would set back the investigation
        elif cellId in {15, 0, 4, 12, 22}:
            cellName = Cell(cellId, 'oops', cellLeft, cellTop, cellSize)
            self.cellList.append(cellName)
        elif cellId == 17:
            cellName = Cell(cellId, 'Go', cellLeft, cellTop, cellSize)
            self.cellList.append(cellName)
        else:
            cellName = Cell(cellId, 'secret', cellLeft, cellTop, cellSize)
            self.cellList.append(cellName)
        cellName.drawCell()
        cellName.drawCellType()
    
    def updateCellList(self): 
        # rearrange cells in the order that the players will proceed in
        cellDict = dict()
        
        # left column cells (0-5)); range(0, 6). orinal cellID: 17-7
        for i in range(0, self.rows-1):
            bottomLeftID = self.cols + (self.rows-2)*2
            cellDict[i] = self.cellList[bottomLeftID-(2*i)]
        
        # top row cells (6-11); range(6, 12). orinal cellID: 0-5
        for i in range(self.rows-1, (self.rows-1)*2):
            iterations = i - (self.rows-1)
            cellDict[i] = self.cellList[0+iterations]
        
        # right column cells (12-17); range(12, 18). orinal cellID: 6-16
        for i in range((self.rows-1)*2, (self.rows-1)*3):
            iterations = i - (self.rows-1)*2
            cellDict[i] = self.cellList[(self.rows-1)+iterations*2]
            
        # bottom row cells (18-23); range(18, 24). orinal cellID: 23-18
        for i in range((self.rows-1)*3, (self.rows-1)*4):
            iterations = i - (self.rows-1)*3
            cellDict[i] = self.cellList[(self.rows-1)*4-1-iterations]
        
        self.cellDict = cellDict
        print(self.cellDict)
            
    def getCellLeftTop(self, row, col):
        cellSize = self.getCellSize()
        cellLeft = col*cellSize + self.boardLeft
        cellTop = row*cellSize + self.boardTop
        return cellLeft, cellTop
    
    def getCellSize(self):
        cellSize = self.width/self.cols
        return cellSize
        
class Cell:
    cellList = []
    def __init__(self, cellId, secretType, cellLeft, cellTop, cellSize):
        self.secretType = secretType # secret, oops, weapon
        self.cellId = cellId
        self.cellLeft = cellLeft
        self.cellTop = cellTop
        self.cellSize = cellSize
        self.cx = cellLeft + cellSize/2
        self.cy = cellTop + cellSize/2
    def __repr__(self):
        return f'{self.cellId}. {self.secretType}'      
        
    def __eq__(self, other):
        return (isinstance(other, Cell) and (self.secretType==other.secretType)
                and (self.cellLeft == other.cellLeft) and (self.cellTop == other.cellTop))
        
    def __hash__(self):
        return hash(str(self))
    
    def drawCell(self):
        if self.secretType=='oops':
            color = 'red'
        elif self.secretType == 'weapon':
            color= 'green'
        elif self.secretType == 'Go':
            color = 'pink'
        else:
            color = 'blue'
        drawRect(self.cellLeft, self.cellTop, self.cellSize, self.cellSize, 
                 fill=color, border='black', 
                 borderWidth=1)
    
    def drawCellType(self):
        drawLabel(f'{self.cellId}. {self.secretType}', self.cellLeft + .5*self.cellSize, self.cellTop + .5*self.cellSize)
    ## print the labels (secretType)on the cell

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
    
class Player:
    def __init__(self, name, cellDict, xPos):
        self.name = name
        self.cellDict = cellDict
        self.currCellNum = 0
        self.currCell = cellDict[self.currCellNum]
        self.dX = xPos
        self.cx = self.currCell.cx + self.dX
        self.cy = self.currCell.cy
        
    def __repr__(self):
        return f'Player({self.name}, {self.currCell})'
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return isinstance(other, Player) and self.name==other.name
    
    def updatePlayerCoordinates(self):
        self.cx = self.currCell.cx + self.dX
        self.cy = self.currCell.cy
    
    def updatePlayerCell(self, steps): # this should be called when rolled a dice
        # mod by 24 to return to 0 after reached cell 23
        self.currCellNum  = (self.currCellNum + steps) % 24 
        self.currCell = self.cellDict[self.currCellNum]
    
    def drawPlayer(self):
        self.updatePlayerCoordinates()
        drawCircle(self.cx, self.cy, 10, fill='yellow')

        
    
#### APP

def onAppStart(app):
    app.height = 700
    app.width = 800
    app.paused = True
    app.stepsPerSecond = 1
    app.gameBoard = Board(500, 500, 7, 7)
    

def redrawAll(app):
    # drawLabel('112 Murder Mystery', 200, 200)
    # drawLabel(app.paused, 200, 250)

    app.gameBoard.drawBoard()

def onMousePress(app, mouseX, mouseY):
    pass

def onKeyPress(app, key):
    if key == 'c':
        print('running camera')
        # runCamera()
        print('finished running camera')
    if key.isdigit():
        print(key)
        app.gameBoard.player1.updatePlayerCell(int(key))
        
def onStep(app):
    app.paused = not app.paused

runApp()