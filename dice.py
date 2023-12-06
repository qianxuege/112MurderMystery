from cmu_graphics import *
from imageManager import loadImages

# looked through Mike's notes on sprite
# got images of the dice from: 
# 'https://www.alamy.com/set-of-3d-dice-render-white-realistic-dices-casino-and-betting-background-vector-illustration-image443037527.html'

class Dice:
    def __init__(self, boardLeft, boardTop, boardW, boardH, colors):
        self.boardLeft = boardLeft
        self.boardTop = boardTop
        self.boardW = boardW
        self.boardH = boardH
        self.colors = colors
        self.imageDict = loadImages()
        self.diceList = ([self.imageDict["dice1"], self.imageDict["dice2"], self.imageDict["dice3"], 
                          self.imageDict["dice4"], self.imageDict["dice5"], self.imageDict["dice6"]])
        self.diceNum = 6
        self.currFrame = 0
        self.stepsCounter = 0
        
        # properties for draw the dice
        self.mouseX = None
        self.mouseY = None
        self.rollBtnLeft = self.boardLeft + 60 + 100
        self.rollBtnTop = self.boardTop + self.boardH + 20
        self.rollBtnW = 180
        self.rollBtnH = 40
        
    def drawRollDiceBtn(self):
        drawRect(self.rollBtnLeft, self.rollBtnTop, self.rollBtnW, self.rollBtnH, fill=self.colors.dustyBlue)
        drawLabel("Roll Dice", self.boardLeft + 60 + 190, self.boardTop + self.boardH + 40, size=16, fill=self.colors.moonLight)
    
    def checkBtnClick(self):
        if (self.rollBtnLeft <= self.mouseX <= self.rollBtnLeft + self.rollBtnW and 
            self.rollBtnTop <= self.mouseY <= self.rollBtnTop + self.rollBtnH):
            return True
        return False
    
    def drawDice(self):
        drawImage(self.diceList[self.currFrame], 200, 200, align = 'center')
    