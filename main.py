from cmu_graphics import *
from handDetection import runCamera

class Board:
    def __init__(self, width, height, rows, cols):
        self.width = width #350
        self.height = height #350
        self.rows = rows #7
        self.cols = cols #7
        self.cellBorderWidth = 1
        self.boardLeft = 50
        self.boardTop = 150
    
    def drawBoard(self):
        # width, height = self.width, self.height
        # rows, cols = self.rows, self.cols
        for row in range(self.rows):
            for col in range(self.cols):
                self.drawCell(row, col)
        self.drawBoardBorder()
    
    def drawBoardBorder(self):
        drawRect(self.boardLeft, self.boardTop, self.width, self.height, 
                 fill=None, border = 'black', 
                 borderWidth = 2*self.cellBorderWidth)
    
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
        # print(cellSize)
        return cellSize
        

def onAppStart(app):
    app.height = 600
    app.width = 600
    app.paused = True
    app.stepsPerSecond = 5
    

def redrawAll(app):
    drawLabel('112 Murder Mystery', 200, 200)
    # drawLabel(app.paused, 200, 250)
    gameBoard = Board(400, 400, 7, 7)
    gameBoard.drawBoard()

def onKeyPress(app, key):
    if key == 's':
        print('running camera')
        # runCamera()
        print('finished running camera')
        
def onStep(app):
    app.paused = not app.paused

runApp()