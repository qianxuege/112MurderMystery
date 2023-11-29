from cmu_graphics import *
import copy
from handDetection import runCamera


class Colors:
    def __init__(self):
        self.dustyBlue = rgb(116, 136, 168)
        self.mossGreen = rgb(89, 125, 92)

class Board:
    def __init__(self, width, height, rows, cols):
        self.width = width  # 500
        self.height = height  # 500
        self.rows = rows  # 7
        self.cols = cols  # 7
        self.cellBorderWidth = 1
        self.cellSize = self.width / self.cols
        self.boardLeft = 150
        self.boardTop = 100
        self.colors = Colors()
        # inner box properties
        self.innerLeft = self.boardLeft + self.cellSize
        self.innerTop = self.boardTop + self.cellSize
        self.innerSize = self.width - (2 * self.cellSize)
        # instances of cell class
        self.cellDict = dict()
        self.isFirstIteration = True
        # players
        self.player1 = None
        self.AI = None
        self.playerDict = dict()
        # rooms
        self.roomsDict = dict()
        # weapons
        self.weaponsDict = dict() # [charName, weapon, bool for assignedToCell]
        # Alternate turns
        self.currTurn = None
        self.otherPlayer = None

    def drawBoard(self):
        originalCellId = 0
        #only passes in originalCellId when app is first created
        if self.isFirstIteration == True:
            for row in range(self.rows):
                for col in range(self.cols):
                    # leave the middle of the board blank
                    if 0 < row < (self.rows - 1) and 0 < col < (self.cols - 1):
                        continue
                    self.drawCell(row, col, originalCellId)  # pass in an id
                    originalCellId += 1
                
        self.drawBoardBorder()

        # initiating players
        if self.isFirstIteration == True:
            # creates a dictionary of the cells in the correct order after board is drawn
            self.updateCellDict()
            print(self.cellDict)
            for cellNum in self.cellDict:
                self.cellDict[cellNum].drawCell()
            self.createRooms()
        
            # initiates players only after the cellDict is updated
            # -10 is the diff in x position    
            self.player1 = Player(
                "player1",
                self.cellDict,
                self.roomsDict,
                -10,
                (self.innerLeft, self.innerTop, self.innerSize),
                (self.boardLeft, self.boardTop, self.width),
                "yellow",
                self.weaponsDict
            )
            self.AI = Player(
                "AI",
                self.cellDict,
                self.roomsDict,
                20,
                (self.innerLeft, self.innerTop, self.innerSize),
                (self.boardLeft, self.boardTop, self.width),
                "purple",
                self.weaponsDict
            )
            self.playerDict["player1"] = self.player1
            self.playerDict["AI"] = self.AI
            self.currTurn = self.player1
            self.isFirstIteration = False
        else:
            # draw cell using the new cellDict
            for cellNum in self.cellDict:
                self.cellDict[cellNum].drawCell()
                self.cellDict[cellNum].drawCellType()
            # draw Player1
            self.player1.drawPlayer()
            # draw AI
            self.AI.drawPlayer()
            self.drawLowerBtns()

    def createRooms(self): # also add character weapons to the weaponsDict
        # need to change all char secret descriptions according to the linebreaks
        # Kitchen
        kitchenCharSecret = (
            "To most people, Mrs. White seems like an honest \n" + 
            "and optimistic woman who runs Colonel Mustard’s kitchen \n" + 
            "efficiently on a daily basis. Would anyone suspect that \n" + 
            "she has covertly taken money from Mustard and stolen \n" + 
            "valuable antiques to sell on the black market?"
        )
        kitchenRoomSecret = "Mustard was not in the kitchen at 9pm"
        kitchen = Rooms(
            "Kitchen", 0, "Mrs. White", kitchenCharSecret, kitchenRoomSecret
        )
        self.weaponsDict[0] = ['Mrs. White','Candlestick', False]
        self.roomsDict[0] = kitchen

        # Master Bedroom
        bedroomCharSecret = (
            "Everyone knows Colonel Mustard is a decorated war \n" +
            "hero. He is also from a venerated and wealthy family.\n" +
            "Ironically, he wasn’t actually in the battle for which \n" + 
            "he was awarded his most prestigious medal."
        )
        bedroomRoomSecret = "Mustard was not in the bedroom at 9pm"
        bedroom = Rooms(
            "Master Bedroom", 1, "Colonel Mustard", bedroomCharSecret, bedroomRoomSecret
        )
        self.weaponsDict[1] = ['Colonel Mustard','Pistol', False]
        self.roomsDict[1] = bedroom
        # Billiard Room
        billiardCharSecret = (
            "Mr. Green is a businessman who is a closeted homosexual.\n" +
            "He is desperately in love with his partner and wants to \n" + 
            "get married, but Mustard used his influence to make gay \n" +
            "marriage illegal in his state. Green now can’t pursue \n" + 
            "his love –– he wants revenge…"
        )
        billiardRoomSecret = "Mustard was not in the billiard room at 9pm"
        billiard = Rooms(
            "Billiard Room", 2, "Mr. Green", billiardCharSecret, billiardRoomSecret
        )
        self.weaponsDict[2] = ['Mr. Green','Dagger', False]
        self.roomsDict[2] = billiard
        # Study
        studyCharSecret = (
            "Plum is a professor of antiquities. He identifies \n" + 
            "counterfeits and occasionally makes them, including\n" + 
            "his PhD certificate. Beware, Plum knows that \n" +
            "Mustard knows his secret…"
        )
        studyRoomSecret = "Mustard was not in the study room at 9pm"
        study = Rooms("Study", 3, "Professor Plum", studyCharSecret, studyRoomSecret)
        self.weaponsDict[3] = ['Professor Plum','Rope', False]
        self.roomsDict[3] = study
        # Parlor
        parlorCharSecret = (
            "Mrs. Peacock is a lawyer and the mother of a soldier\n" +
            "under Mustard. What an honor you might think! \n" +
            "Well, Mustard killed her son because\n" + 
            "her son attempted to unveil Mustard’s secret."
        )
        parlorRoomSecret = "Mustard was in the Parlor at approximately 9pm"
        parlor = Rooms("Parlor", 4, "Mrs. Peacock", parlorCharSecret, parlorRoomSecret)
        self.weaponsDict[4] = ['Mrs. Peacock','Hammer', False]
        self.roomsDict[4] = parlor
        # Balcony
        balconyCharSecret = (
            "Miss Scarlet is a movie actress whose career is crumbling.\n" +
            "She also lost a lot of money due to gambling.\n" +
            "Hmmm, life must be hard for her right now."
        )
        balconyRoomSecret = "Mustard was not in the Balcony at 9pm."
        balcony = Rooms(
            "Balcony", 5, "Miss Scarlet", balconyCharSecret, balconyRoomSecret
        )
        self.weaponsDict[5] = ['Miss Scarlet','Poison', False]
        self.roomsDict[5] = balcony

    def drawBoardBorder(self):
        drawRect(
            self.boardLeft,
            self.boardTop,
            self.width,
            self.height,
            fill=None,
            border="black",
            borderWidth=2 * self.cellBorderWidth,
        )
        cellSize = self.getCellSize()
        drawRect(
            self.boardLeft + cellSize,
            self.boardTop + cellSize,
            self.width - (2 * cellSize),
            self.height - (2 * cellSize),
            fill=None,
            border="black",
            borderWidth=self.cellBorderWidth,
        )

    def drawCell(self, row, col, originalCellId):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellSize = self.getCellSize()
        # these are the weapon's clue cells
        if originalCellId in {13, 7, 3, 10, 16, 20}:
            cellName = Weapon(originalCellId, "weapon", cellLeft, cellTop, cellSize)
            self.cellDict[originalCellId] = cellName
            # self.originalCellId.append(cellName)
        # these are the cells that would set back the investigation
        elif originalCellId in {15, 0, 4, 12, 22}:
            cellName = Cell(originalCellId, "oops", cellLeft, cellTop, cellSize)
            self.cellDict[originalCellId] = cellName
            # self.originalCellId.append(cellName)
        elif originalCellId == 17:
            cellName = Cell(originalCellId, "Go", cellLeft, cellTop, cellSize)
            self.cellDict[originalCellId] = cellName
            # self.originalCellId.append(cellName)
        else:
            # price for each secret is 100
            cellName = Secret(originalCellId, "secret", cellLeft, cellTop, cellSize, 100)
            self.cellDict[originalCellId] = cellName
            # self.originalCellId.append(cellName)
        cellName.drawCell()
        cellName.drawCellType()

    def updateCellDict(self):
        # rearrange cells in the order that the players will proceed in
        cellDict = dict()
        originalDict = copy.deepcopy(self.cellDict)

        # left column cells (0-5)); range(0, 6). originalCellId: 17-7
        for i in range(0, self.rows - 1):
            bottomLeftID = self.cols + (self.rows - 2) * 2
            cellDict[i] = originalDict[bottomLeftID - (2 * i)]
            cellDict[i].cellDictId = i

        # top row cells (6-11); range(6, 12). originalCellId: 0-5
        # while mobing them into a dict, also changing their cellDictId
        for i in range(self.rows - 1, (self.rows - 1) * 2):
            iterations = i - (self.rows - 1)
            cellDict[i] = originalDict[0 + iterations]
            cellDict[i].cellDictId = i

        # right column cells (12-17); range(12, 18). originalCellId: 6-16
        for i in range((self.rows - 1) * 2, (self.rows - 1) * 3):
            iterations = i - (self.rows - 1) * 2
            cellDict[i] = originalDict[(self.rows - 1) + iterations * 2]
            cellDict[i].cellDictId = i

        # bottom row cells (18-23); range(18, 24). originalCellId: 23-18
        for i in range((self.rows - 1) * 3, (self.rows - 1) * 4):
            iterations = i - (self.rows - 1) * 3
            cellDict[i] = originalDict[(self.rows - 1) * 4 - 1 - iterations]
            cellDict[i].cellDictId = i

        self.cellDict = cellDict
        # print(self.cellDict)

    def getCellLeftTop(self, row, col):
        cellSize = self.getCellSize()
        cellLeft = col * cellSize + self.boardLeft
        cellTop = row * cellSize + self.boardTop
        return cellLeft, cellTop

    def getCellSize(self):
        cellSize = self.width / self.cols
        return cellSize

    # currently not using this
    def drawInnerBoard(self):
        # draw a huge rectangle in the middle of the screen
        drawRect(
            self.innerLeft,
            self.innerTop,
            self.innerSize,
            self.innerSize,
            fill="light green",
        )

    def drawLowerBtns(self):
        # make a guess
        drawRect(self.boardLeft-15, self.boardTop + self.height + 20, 150, 40, fill=self.colors.dustyBlue, border='black')
        drawLabel("Make a guess", self.boardLeft + 60, self.boardTop + self.height + 40, size = 20)

        # switch turns
        drawLabel(f"It is {self.currTurn.name}'s turn.", self.boardLeft + 60+ 180, self.boardTop + self.height + 40, size = 16)
        drawRect(self.boardLeft + 60+ 400 - 100, self.boardTop + self.height + 20, 200, 40, fill=self.colors.dustyBlue, border='black')
        drawLabel('click here to switch turns', self.boardLeft + 60+ 400, self.boardTop + self.height + 40, size = 16)

        # self.boardLeft + self.width - 60, self.boardTop + self.height + 40

class Cell:
    cellDict = dict()

    def __init__(self, originalCellId, cellType, cellLeft, cellTop, cellSize):
        self.cellType = cellType  # secret, oops, weapon
        self.originalCellId = originalCellId
        self.cellDictId = None        # will be changed when updating cellDict
        self.cellLeft = cellLeft
        self.cellTop = cellTop
        self.cellSize = cellSize
        self.cx = cellLeft + cellSize / 2
        self.cy = cellTop + cellSize / 2

    def __repr__(self):
        return f"{self.cellDictId}. {self.cellType}"

    def __eq__(self, other):
        return (
            isinstance(other, Cell)
            and (self.cellType == other.cellType)
            and (self.cellLeft == other.cellLeft)
            and (self.cellTop == other.cellTop)
        )

    def __hash__(self):
        return hash(str(self))

    def drawCell(self):
        if self.cellType == "oops":
            color = rgb(227, 141, 138)  # red
        elif self.cellType == "weapon":
            color = rgb(205, 230, 193)  # green
        elif self.cellType == "Go":
            color = rgb(255, 240, 251)  # pink
        elif self.cellType == "secret" and self.secretOwned == False:
            color = rgb(235, 240, 252)  # blue
        elif self.cellType == "secret" and self.secretOwner != None:
            color = rgb(104, 119, 156)  # darkerBlue
        drawRect(
            self.cellLeft,
            self.cellTop,
            self.cellSize,
            self.cellSize,
            fill=color,
            border="black",
            borderWidth=1,
        )

    def drawCellType(self):
        # print the labels (cellType) on the cell
        drawLabel(
            f"{self.cellType}",
            self.cellLeft + 0.5 * self.cellSize,
            self.cellTop + 0.5 * self.cellSize,
        )

class Weapon(Cell):
    def __init__(self, originalCellId, cellType, cellLeft, cellTop, cellSize):
        super().__init__(originalCellId, cellType, cellLeft, cellTop, cellSize) 
        self.weapon = None
        self.weaponChar = None
        self.cellOccupied = False

# buy and pay rent on Secret cells
class Secret(Cell):
    def __init__(self, originalCellId, cellType, cellLeft, cellTop, cellSize, price):
        super().__init__(originalCellId, cellType, cellLeft, cellTop, cellSize)
        # add a property to Secret. checks if can buy secret or need to pay rent
        self.price = price
        self.secretOwned = False
        self.secretOwner = None
        self.secretRoom = None
        self.secretType = None
        self.secret = None
        self.yesBuy = False
        self.yesRent = False

    def __repr__(self):
        return f"{self.cellDictId}. {self.cellType}, owner is {self.secretOwner}"

    def drawCellType(self):
        # print the labels (cellType) on the cell
        drawLabel(
            f"${self.price} {self.cellType}",
            self.cellLeft + 0.5 * self.cellSize,
            self.cellTop + 0.5 * self.cellSize,
        )


class Rooms:
    def __init__(
        self, name, dictionaryKey, character, characterSecret, roomSecret
    ):  # isRoom is a boolean value
        self.name = name
        self.id = dictionaryKey
        self.accessible = True
        self.character = character
        # the secrets
        self.characterSecret = characterSecret
        self.roomSecret = roomSecret
        # ownserships
        self.characterSecretOwner = None
        self.roomSecretOwner = None

    def __repr__(self):
        return f"{self.name}({self.character}, {self.characterSecretOwner}, {self.roomSecretOwner})"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return isinstance(other, Rooms) and (other.name == self.name)

    def buySecret(self, player):
        #
        pass

    def checkSecret(self):
        if self.characterSecretOwner == None:
            return f"You can buy a character secret"
        elif self.roomSecretOwner == None:
            return f"You can buy a room secret"
        else:
            return f"The secrets in this room have been claimed."


class Player:
    def __init__(
        self, name, cellDict, roomsDict, xPos, innerBoard, outerBoard, playerColor, weaponsDict
    ):
        self.name = name
        self.cellDict = cellDict
        self.roomsDict = roomsDict
        self.weaponsDict = weaponsDict
        self.currCellNum = 0
        self.currCell = cellDict[self.currCellNum]
        self.dX = xPos
        self.cx = self.currCell.cx + self.dX
        self.cy = self.currCell.cy
        self.innerLeft = innerBoard[0]
        self.innerTop = innerBoard[1]
        self.innerSize = innerBoard[2]
        self.boardLeft = outerBoard[0]
        self.boardTop = outerBoard[1]
        self.boardSize = outerBoard[2]
        self.playerColor = playerColor
        self.colors = Colors()
        # upper labels
        self.lives = 3
        self.money = 1500
        # states
        self.buyingSecret = False
        self.removeInnerBoard = False
        self.showRooms = False
        self.roomsDrawn = False
        # renting states
        self.rentingSecret = False
        self.processingRent = False
        self.rentOKRect = None
        # weapon states
        self.showWeaponSecret = False
        self.weaponOKRect = None
        self.processingWeaponSecret = False
        self.shownWeaponSecret = False # resets to False when gets to a new cell
        # rooms and secrets
        self.charSecretOwned = set()
        self.roomSecretOwned = set()
        self.weaponSecretOwned = set()
        self.selectedRoom = None
        self.secretOKRect = None
        # buttons on board
        self.yesBtnLeft = None
        self.yesBtnTop = None
        self.noBtnLeft = None
        self.noBtnTop = None
        self.btnW = 120
        self.btnH = 40
        self.roomBtnCol1Left = None
        self.roomBtnCol2Left = None
        self.roomBtnTop = None
        self.roomBtnH = None
        self.roomBtnW = None

    def __repr__(self):
        return f"Player({self.name}, {self.currCell})"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return isinstance(other, Player) and self.name == other.name

    def updatePlayerCoordinates(self):
        self.cx = self.currCell.cx + self.dX
        self.cy = self.currCell.cy

    def updatePlayerCell(self, steps):  # this should be called when rolled a dice
        # mod by 24 to return to 0 after reached cell 23
        self.currCellNum = (self.currCellNum + steps) % 24
        self.currCell = self.cellDict[self.currCellNum]
        # would reset the state of not drawing inner board (bc player clicked no on the previous cell)
        self.removeInnerBoard = False
        self.shownWeaponSecret = False

    # lives, money
    def drawUpperLabel(self):
        if self.name == "player1":
            drawLabel(
                f"{self.name} lives: {self.lives}",
                self.boardLeft + 35,
                self.boardTop - 70,
                size=20,
            )
            drawLabel(
                f"{self.name} money: ${self.money}",
                self.boardLeft + 35,
                self.boardTop - 40,
                size=20,
            )
        elif self.name == "AI":
            drawLabel(
                f"{self.name} lives: ${self.lives}",
                self.boardLeft + self.boardSize - 35,
                self.boardTop - 70,
                size=20,
            )
            drawLabel(
                f"{self.name} money: ${self.money}",
                self.boardLeft + self.boardSize - 35,
                self.boardTop - 40,
                size=20,
            )
    
    def drawInnerBoard(self):
        color = rgb(247, 246, 228)  # sand
        drawRect(
            self.innerLeft,
            self.innerTop,
            self.innerSize,
            self.innerSize,
            fill=color,
            borderWidth=3,
        )

    def drawWhiteInnerBoard(self):
        color = "white"
        drawRect(
            self.innerLeft,
            self.innerTop,
            self.innerSize,
            self.innerSize,
            fill=color,
            borderWidth=3,
        )

    def buySecretPopup(self):
        yesCX = self.innerLeft + (self.innerSize / 2) - 100
        yesCY = self.innerTop + (self.innerSize / 2) + 50
        noCX = self.innerLeft + (self.innerSize / 2) + 100
        noCY = self.innerTop + (self.innerSize / 2) + 50
        # update btn dimension
        self.yesBtnLeft = yesCX - 60
        self.yesBtnTop = yesCY - 20
        self.noBtnLeft = noCX - 60
        self.noBtnTop = noCY - 20
        drawLabel(
            "Would you like to buy the secret?",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + (self.innerSize / 2) - 100,
            size = 20
        )
        # yes label
        drawRect(self.yesBtnLeft, self.yesBtnTop, self.btnW, self.btnH, fill="yellow")
        drawLabel(f"Yes (Pay ${self.currCell.price})", yesCX, yesCY)
        # no label
        drawRect(self.noBtnLeft, self.noBtnTop, self.btnW, self.btnH, fill="yellow")
        drawLabel(f"No (free of charge)", noCX, noCY)


    def drawRoomSelection(self):
        self.roomBtnCol1Left = self.yesBtnLeft
        self.roomBtnTop = self.innerTop + 60
        self.roomBtnCol2Left = self.noBtnLeft
        # draws a white inner board over the sand inner board
        self.drawWhiteInnerBoard()
        drawLabel(
            "Please select a room to investigate",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + (self.innerSize / 2) - 100,
        )

        dustyBlue = rgb(116, 136, 168)
        for i in range(len(self.roomsDict)):  # len(self.roomsDict)
            if i < 3:
                rectLeft = self.roomBtnCol1Left
                rectTop = self.roomBtnTop + i * (self.btnH + 20) + 50
                cx = rectLeft + 0.5 * self.btnW
                cy = rectTop + 0.5 * self.btnH
                drawRect(rectLeft, rectTop, self.btnW, self.btnH, fill=dustyBlue)
                drawLabel(f"{self.roomsDict[i].id}. {self.roomsDict[i].name}", cx, cy)
            else:
                j = i % 3
                rectLeft = self.roomBtnCol2Left
                rectTop = self.roomBtnTop + j * (self.btnH + 20) + 50
                cx = rectLeft + 0.5 * self.btnW
                cy = rectTop + 0.5 * self.btnH
                drawRect(rectLeft, rectTop, self.btnW, self.btnH, fill=dustyBlue)
                drawLabel(f"{self.roomsDict[i].id}. {self.roomsDict[i].name}", cx, cy)

    def drawSelectedRoom(self):
        self.drawWhiteInnerBoard()
        drawLabel(
            f"You have entered the {self.selectedRoom.name}",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 50,
            size = 20
        )
        if self.selectedRoom.characterSecretOwner == None:
            secretDisplayed = 'characterSecret'
            self.drawSecret('character secret', self.selectedRoom.characterSecret)
            
        # shows the room secret if the character secret is already owned
        elif self.selectedRoom.roomSecretOwner == None:
            secretDisplayed = 'roomSecret'
            self.drawSecret('room secret', self.selectedRoom.roomSecret)
        # draws the OK button in the drawSecret method
        
        # updates ownership if the OK button is clicked
        if self.buyingSecret == False:
            if secretDisplayed == 'characterSecret':
                self.charSecretOwned.add(self.selectedRoom.characterSecret) # updates list of player secrets
                self.selectedRoom.characterSecretOwner = self.name
                self.currCell.secretRoom = self.selectedRoom.name
                self.currCell.secretType = 'characterSecret'
                self.currCell.secret = self.selectedRoom.characterSecret
            elif secretDisplayed == 'roomSecret':
                self.roomSecretOwned.add(self.selectedRoom.roomSecret)
                self.selectedRoom.roomSecretOwner = self.name
                self.currCell.secretType = 'roomSecret'
                self.currCell.secret = self.selectedRoom.roomSecret
            self.yesBuySecret()
            print(self.currCell)

    
    def drawSecret(self, secretType, secretString):
        centerX = self.innerLeft + (self.innerSize / 2)
        drawLabel(f'The {secretType} is:', centerX, self.innerTop + 110)
        currY = self.innerTop + 130
        for line in secretString.splitlines():
            currY += 20
            drawLabel(line, centerX, currY)
        
        # OK button
        dustyBlue = rgb(116, 136, 168)
        drawRect(centerX-50, currY + 50, 100, 40, fill=dustyBlue)
        drawLabel("OK", centerX, currY + 70)
        self.secretOKRect = (centerX-50, currY + 50, 100, 40)
    
    def drawRoomNotAvailable(self):
        drawLabel(f"Sorry, the secrets in {self.selectedRoom.name} have been owned.", 
                  self.innerLeft + (self.innerSize / 2), self.innerTop + 50, size = 16)
        drawLabel(f"Please select a different room.", 
                  self.innerLeft + (self.innerSize / 2), self.innerTop + 75, size = 16)
        
        drawRect(self.innerLeft + (self.innerSize / 2) - 50, self.innerTop + 150, 100, 40, fill=self.colors.dustyBlue)
        drawLabel("OK", self.innerLeft + (self.innerSize / 2), self.innerTop + 170)

    # this should be called at the end of displaying the secret
    def yesBuySecret(self):
        priceOfSecret = self.currCell.price
        self.editMoney(-priceOfSecret)
        self.updateCellOwnership()
        self.selectedRoom = None
    
    def rentSecretPopup(self):
        yesCX = self.innerLeft + (self.innerSize / 2)
        yesCY = self.innerTop + (self.innerSize / 2)
        self.yesBtnLeft = yesCX - 60
        self.yesBtnTop = yesCY - 20
        drawLabel("The secret of this cell has already been owned.", 
                self.innerLeft + (self.innerSize / 2),
                self.innerTop + (self.innerSize / 2) - 130,
                size = 16)
        drawLabel(
            "You'll need to pay a rent.",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + (self.innerSize / 2) - 100,
            size = 16
        )
        # OK label
        drawRect(self.yesBtnLeft, self.yesBtnTop, self.btnW, self.btnH, fill=self.colors.mossGreen)
        drawLabel(f"OK (Pay ${int(self.currCell.price*.75)})", yesCX, yesCY)
        self.rentOKRect = (self.yesBtnLeft, self.yesBtnTop, self.btnW, self.btnH)
    
    def drawRentSecret(self):
        self.drawWhiteInnerBoard()
        drawLabel(
            f"You have entered the {self.currCell.secretRoom}",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 50,
            size = 20
        )
        self.drawSecret(self.currCell.secretType, self.currCell.secret)
        print(f'drawn secret')
        
        if self.rentingSecret == False:
            self.processRentMethod()
        # drawSecret(self, secretType, secretString)

    def processRentMethod(self):
        # the + - money is done in the onclick of APP
        self.processingRent = False
        self.removeInnerBoard = True
        self.rentingSecret = False

    def editMoney(self, money):
        self.money += money
    
    def updateCellOwnership(self):
        self.currCell.secretOwned = True
        self.currCell.secretOwner = self.name
        # change the selectedRoom secret ownership when user closes the popup
        
    # assigns an empty weapon cell a weapon secret
    def checkWeaponCellOwnership(self):
        for i in range(len(self.weaponsDict)):
            if self.weaponsDict[i][2] == False:
                self.currCell.weaponChar = self.weaponsDict[i][0] # update cell char info
                self.currCell.weapon = self.weaponsDict[i][1] # update cell weapon info
                self.weaponsDict[i][2] = True # indicate that this weapon clue has been claimed
                self.showWeaponSecret = True
                self.currCell.cellOccupied = True
                break
        
        
    def drawWeaponSecret(self):
        self.drawInnerBoard()
        centerX = self.innerLeft + (self.innerSize / 2)
        drawLabel(f"{self.currCell.weaponChar}'s weapon is {self.currCell.weapon}.", centerX, self.innerTop + 110, size=20)
        btnX = centerX-50
        btnY = self.innerTop + 110 + 100
        
        # OK button
        drawRect(btnX, btnY, 100, 40, fill=self.colors.dustyBlue)
        drawLabel("OK", centerX, btnY + 20)
        self.weaponOKRect = (btnX, btnY, 100, 40)
    
    def processWeaponSecret(self):
        self.weaponSecretOwned.add(f"{self.currCell.weaponChar}'s weapon is {self.currCell.weapon}.")
        self.processingWeaponSecret = False
        self.showWeaponSecret = False
        self.shownWeaponSecret = True
    

    def checkOnCell(self):
        if isinstance(self.currCell, Secret):
            # checks the secretOwned status of the cell, not the room
            if self.currCell.secretOwned == False:
                if self.removeInnerBoard == False:
                    # change state
                    self.buyingSecret = True  # state
                    self.drawInnerBoard()
                    self.buySecretPopup()
                # draws the room options if clicked on 'yes'
                if self.showRooms == True:
                    print("show rooms")
                    self.drawRoomSelection()
                    self.roomsDrawn = True
                if self.selectedRoom != None:
                    self.showRooms = False  # state
                    self.roomsDrawn = False  # state
                    # check if the room secrets have been owned.
                    if self.selectedRoom.characterSecretOwner == None or self.selectedRoom.roomSecretOwner == None:
                        self.drawSelectedRoom()
                    else:
                        if self.roomsDrawn == False:
                            self.drawRoomNotAvailable()
                            # if click on OK, self.showRooms = True
                        # use mouse press to check if ok is clicked. if clicked, return to drawselectedroom
                        # reset through the yesBuySecret method, called in drawSelectedRoom
            # process rent if cell secret has been owned
            if self.currCell.secretOwned == True:
                if self.currCell.secretOwner != self.name:
                    if self.removeInnerBoard == False:
                        self.drawInnerBoard()
                        self.rentSecretPopup() # would create the rentOKRect
                    if self.rentingSecret == True: # this state is changed when clicked 'ok' on popup
                        print('renting secret: should display secret of the cell')
                        self.drawRentSecret()
                    if self.processingRent == True:
                        self.processRentMethod()

                else:
                    # display you are the owner of the cell, pass
                    pass
        if isinstance(self.currCell, Weapon):
            if self.currCell.cellOccupied == False:
                self.checkWeaponCellOwnership()
            elif self.currCell.cellOccupied == True and self.shownWeaponSecret == False:
                self.showWeaponSecret = True
            if self.showWeaponSecret == True: # this will run if player clicked ok on checkWeaponCellOwnership
                self.drawWeaponSecret()
            if self.processingWeaponSecret == True:
                self.processWeaponSecret()
                print(f"{self.name}'s weapon secrets include {self.weaponSecretOwned}")

    def drawPlayer(self):
        self.updatePlayerCoordinates()
        self.drawUpperLabel()
        # draw innerboard, get cell info
        drawCircle(
            self.cx, self.cy, 10, fill=self.playerColor, border="black", borderWidth=1
        )
        self.checkOnCell()


#### APP MVC


def onAppStart(app):
    app.height = 700
    app.width = 800
    app.paused = True
    app.stepsPerSecond = 1
    app.gameBoard = Board(500, 500, 7, 7)
    app.instructionScreen = False
    app.currPlayer = app.gameBoard.player1
    app.otherPlayer = app.gameBoard.AI
    

def redrawAll(app):
    # drawLabel('112 Murder Mystery', 200, 200)
    # drawLabel(app.paused, 200, 250)

    app.gameBoard.drawBoard()


def onMousePress(app, mouseX, mouseY):
    # change the player name based on whose turn it is --> create a variable
    changePlayerRectLeft = app.gameBoard.boardLeft + 60+ 400 - 100
    changePlayerRectTop = app.gameBoard.boardTop + app.gameBoard.height + 20
    changePlayerRectW = 200
    changePlayerRectH = 40
    # switch curr player in onStep
    if (changePlayerRectLeft <= mouseX <= changePlayerRectLeft + changePlayerRectW and 
        changePlayerRectTop <= mouseY <= changePlayerRectTop + changePlayerRectH):
        if app.gameBoard.currTurn == app.gameBoard.player1:
            app.gameBoard.currTurn = app.gameBoard.AI
            app.gameBoard.otherPlayer = app.gameBoard.player1
        else:
            app.gameBoard.currTurn = app.gameBoard.player1
            app.gameBoard.otherPlayer = app.gameBoard.AI
   
    
    print(app.currPlayer)

    if app.currPlayer != None and app.instructionScreen == False: # this is when the game starts
        # check if clicked on yes or no buttons for buying
        if (app.currPlayer.buyingSecret == True) and (app.currPlayer.showRooms == False):
            # check if mouseX and mouseY is within bounds of Yes or No box
            if (app.currPlayer.yesBtnLeft <= mouseX <= (app.currPlayer.yesBtnLeft + app.currPlayer.btnW) 
                and app.currPlayer.yesBtnTop <= mouseY <= (app.currPlayer.yesBtnTop + app.currPlayer.btnH)
            ):
                print("yes")

                app.currPlayer.showRooms = True  # change this state would trigger draw options for rooms
                app.currPlayer.removeInnerBoard = True # this gets rid of the yes and no btns
                
                # app.gameBoard.player1.yesBuySecret() do this after the player gets the secret
            elif app.currPlayer.noBtnLeft <= mouseX <= (
                app.currPlayer.noBtnLeft + app.currPlayer.btnW
            ) and app.currPlayer.noBtnTop <= mouseY <= (
                app.currPlayer.noBtnTop + app.currPlayer.btnH
            ):
                print("no")
                app.currPlayer.buyingSecret = False
                app.currPlayer.removeInnerBoard = True

        # check which room the player selected
        if app.currPlayer.roomsDrawn == True:  # need to set this state back to False
            for i in range(len(app.currPlayer.roomsDict) // 2):  # 3
                rectTop = (app.currPlayer.roomBtnTop + i * (app.currPlayer.btnH + 20) + 50)
                col1Left = app.currPlayer.roomBtnCol1Left
                col2Left = app.currPlayer.roomBtnCol2Left
                btnW = app.currPlayer.btnW
                btnH = app.currPlayer.btnH
                # column 1
                if col1Left <= mouseX <= col1Left + btnW:
                    if rectTop <= mouseY <= rectTop + btnH:
                        print(f"clicked on {app.currPlayer.roomsDict[i]}")
                        app.currPlayer.selectedRoom = (
                            app.currPlayer.roomsDict[i]
                        )
                        app.currPlayer.showRooms = False
                # column 2
                elif col2Left <= mouseX <= col2Left + btnW:
                    if rectTop <= mouseY <= rectTop + btnH:
                        print(f"clicked on {app.currPlayer.roomsDict[i+3]}")
                        app.currPlayer.selectedRoom = (
                            app.currPlayer.roomsDict[i + 3]
                        )

        # checks if the OK btn is clicked at the buy secret screen. If so, resets.
        if app.currPlayer.secretOKRect != None and app.currPlayer.buyingSecret == True: # secretOKRect is the coordinates for OK btn
            rectLeft = app.currPlayer.secretOKRect[0]
            rectTop = app.currPlayer.secretOKRect[1]
            rectW = app.currPlayer.secretOKRect[2]
            rectH = app.currPlayer.secretOKRect[3]
            if rectLeft <= mouseX <= rectLeft + rectW and rectTop <= mouseY <= rectTop + rectH:
                app.currPlayer.buyingSecret = False
                app.currPlayer.secretOKRect = None
        
        # checks if the OK btn is clicked on the roomsNotAvailable screen
        if app.currPlayer.roomsDrawn == False:
            rectLeft = app.currPlayer.innerLeft + (app.currPlayer.innerSize/2) - 50
            rectTop = app.currPlayer.innerTop + 150
            rectW = 100
            rectH = 40
            if rectLeft <= mouseX <= rectLeft + rectW and rectTop <= mouseY <= rectTop + rectH:
                print('return to showRooms screen')
                app.currPlayer.showRooms = True
                app.currPlayer.selectedRoom = None

         # checks if the OK btn is clicked at the buy secret screen. If so, resets.
        
        ####### Renting
        
        # check if ok btn clicked on rentPopup screen
        if (app.currPlayer.removeInnerBoard == False) and (app.currPlayer.rentOKRect != None):
            # check if mouseX and mouseY is within bounds of OK Btn
            rectLeft = app.currPlayer.rentOKRect[0]
            rectTop = app.currPlayer.rentOKRect[1]
            rectW = app.currPlayer.rentOKRect[2]
            rectH = app.currPlayer.rentOKRect[3]
            
            if rectLeft <= mouseX <= rectLeft + rectW and rectTop <= mouseY <= rectTop + rectH:
                print("mousePressed. ok, display the secret")
                app.currPlayer.rentingSecret = True

        # checks if the OK btn is clicked on the rent secret screen
        if app.currPlayer.secretOKRect != None and app.currPlayer.rentingSecret == True: # secretOKRect is the coordinates for OK btn
            rectLeft = app.currPlayer.secretOKRect[0]
            rectTop = app.currPlayer.secretOKRect[1]
            rectW = app.currPlayer.secretOKRect[2]
            rectH = app.currPlayer.secretOKRect[3]
            if rectLeft <= mouseX <= rectLeft + rectW and rectTop <= mouseY <= rectTop + rectH:
                processRentOfBothPlayers(app)
                app.currPlayer.processingRent = True
                app.currPlayer.secretOKRect = None
                
        # checks if the OK btn is clicked on the weapon screen
        if app.currPlayer.showWeaponSecret == True and app.currPlayer.weaponOKRect != None:
            rectLeft = app.currPlayer.weaponOKRect[0]
            rectTop = app.currPlayer.weaponOKRect[1]
            rectW = app.currPlayer.weaponOKRect[2]
            rectH = app.currPlayer.weaponOKRect[3]
            if rectLeft <= mouseX <= rectLeft + rectW and rectTop <= mouseY <= rectTop + rectH:
                # close the weapon secret screen
                app.currPlayer.showWeaponSecret = False
                print('should remove weapon secret screen')
                app.currPlayer.weaponOKRect = None
                app.currPlayer.processingWeaponSecret = True
                
def processRentOfBothPlayers(app):
    rentMoney = int(app.currPlayer.currCell.price*.75)
    app.currPlayer.editMoney(-rentMoney)
    app.otherPlayer.editMoney(rentMoney)

def onKeyPress(app, key):
    if app.currPlayer != None:
        if key == "c":
            print("running camera")
            # runCamera()
            print("finished running camera")
        if key.isdigit():
            print(key)
            app.currPlayer.updatePlayerCell(int(key))


def onStep(app):
     # declares the player that is making the moves
    if app.gameBoard.currTurn == None:
        app.currPlayer = app.gameBoard.player1
        app.otherPlayer = app.gameBoard.AI
    else:
        app.currPlayer = app.gameBoard.currTurn
        app.otherPlayer = app.gameBoard.otherPlayer


runApp()
