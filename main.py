from cmu_graphics import *
from handDetection import runCamera


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
        # inner box properties
        self.innerLeft = self.boardLeft + self.cellSize
        self.innerTop = self.boardTop + self.cellSize
        self.innerSize = self.width - (2 * self.cellSize)
        # instances of cell class
        self.cellList = []
        self.cellDict = dict()
        self.isFirstIteration = True
        self.player1 = None
        self.AI = None
        # rooms
        self.roomsDict = dict()

    def drawBoard(self):
        cellId = 0
        for row in range(self.rows):
            for col in range(self.cols):
                # leave the middle of the board blank
                if 0 < row < (self.rows - 1) and 0 < col < (self.cols - 1):
                    continue
                self.drawCell(row, col, cellId)  # pass in an id
                cellId += 1
        self.drawBoardBorder()

        # initiating players
        if self.isFirstIteration == True:
            # creates a dictionary of the cells in the correct order after board is drawn
            self.updateCellList()
            self.createRooms()
            # initiates players only after the cellDict is updated
            # -10 is the diff in x position
            self.isFirstIteration = False
            self.player1 = Player(
                "player1",
                self.cellDict,
                self.roomsDict,
                -10,
                (self.innerLeft, self.innerTop, self.innerSize),
                (self.boardLeft, self.boardTop, self.width),
                "yellow",
            )
            self.AI = Player(
                "AI",
                self.cellDict,
                self.roomsDict,
                20,
                (self.innerLeft, self.innerTop, self.innerSize),
                (self.boardLeft, self.boardTop, self.width),
                "purple",
            )
        else:
            # draw Player1
            self.player1.drawPlayer()
            # draw AI
            self.AI.drawPlayer()

    def createRooms(self):
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

    def drawCell(self, row, col, cellId):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellSize = self.getCellSize()
        # these are the weapon's clue cells
        if cellId in {13, 7, 3, 10, 16, 20}:
            cellName = Cell(cellId, "weapon", cellLeft, cellTop, cellSize)
            self.cellList.append(cellName)
        # these are the cells that would set back the investigation
        elif cellId in {15, 0, 4, 12, 22}:
            cellName = Cell(cellId, "oops", cellLeft, cellTop, cellSize)
            self.cellList.append(cellName)
        elif cellId == 17:
            cellName = Cell(cellId, "Go", cellLeft, cellTop, cellSize)
            self.cellList.append(cellName)
        else:
            # price for each secret is 100
            cellName = Secret(cellId, "secret", cellLeft, cellTop, cellSize, 100)
            self.cellList.append(cellName)
        cellName.drawCell()
        cellName.drawCellType()

    def updateCellList(self):
        # rearrange cells in the order that the players will proceed in
        cellDict = dict()

        # left column cells (0-5)); range(0, 6). orinal cellID: 17-7
        for i in range(0, self.rows - 1):
            bottomLeftID = self.cols + (self.rows - 2) * 2
            self.cellList[bottomLeftID - (2 * i)].cellId = i
            cellDict[i] = self.cellList[bottomLeftID - (2 * i)]

        # top row cells (6-11); range(6, 12). orinal cellID: 0-5
        # while mobing them into a dict, also changing their cellID
        for i in range(self.rows - 1, (self.rows - 1) * 2):
            iterations = i - (self.rows - 1)
            self.cellList[0 + iterations].cellId = i
            cellDict[i] = self.cellList[0 + iterations]

        # right column cells (12-17); range(12, 18). orinal cellID: 6-16
        for i in range((self.rows - 1) * 2, (self.rows - 1) * 3):
            iterations = i - (self.rows - 1) * 2
            self.cellList[(self.rows - 1) + iterations * 2].cellId = i
            cellDict[i] = self.cellList[(self.rows - 1) + iterations * 2]

        # bottom row cells (18-23); range(18, 24). orinal cellID: 23-18
        for i in range((self.rows - 1) * 3, (self.rows - 1) * 4):
            iterations = i - (self.rows - 1) * 3
            self.cellList[(self.rows - 1) * 4 - 1 - iterations].cellId = i
            cellDict[i] = self.cellList[(self.rows - 1) * 4 - 1 - iterations]

        self.cellDict = cellDict
        print(self.cellDict)

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


class Cell:
    cellList = []

    def __init__(self, cellId, secretType, cellLeft, cellTop, cellSize):
        self.secretType = secretType  # secret, oops, weapon
        self.cellId = cellId
        self.cellLeft = cellLeft
        self.cellTop = cellTop
        self.cellSize = cellSize
        self.cx = cellLeft + cellSize / 2
        self.cy = cellTop + cellSize / 2

    def __repr__(self):
        return f"{self.cellId}. {self.secretType}"

    def __eq__(self, other):
        return (
            isinstance(other, Cell)
            and (self.secretType == other.secretType)
            and (self.cellLeft == other.cellLeft)
            and (self.cellTop == other.cellTop)
        )

    def __hash__(self):
        return hash(str(self))

    def drawCell(self):
        if self.secretType == "oops":
            color = rgb(227, 141, 138)  # red
        elif self.secretType == "weapon":
            color = rgb(205, 230, 193)  # green
        elif self.secretType == "Go":
            color = rgb(255, 240, 251)  # pink
        else:
            color = rgb(235, 240, 252)  # blue
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
        # print the labels (secretType) on the cell
        drawLabel(
            f"{self.secretType}",
            self.cellLeft + 0.5 * self.cellSize,
            self.cellTop + 0.5 * self.cellSize,
        )


# buy and pay rent on Secret cells
class Secret(Cell):
    def __init__(self, cellId, secretType, cellLeft, cellTop, cellSize, price):
        super().__init__(cellId, secretType, cellLeft, cellTop, cellSize)
        # add a property to Secret. checks if can buy secret or need to pay rent
        self.price = price
        self.secretOwned = False
        self.secretOwner = None
        self.yesBuy = False
        self.yesRent = False

    def __repr__(self):
        return f"{self.cellId}. {self.secretType}, owner is {self.secretOwner}"

    def drawCellType(self):
        # print the labels (secretType) on the cell
        drawLabel(
            f"${self.price} {self.secretType}",
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
        self, name, cellDict, roomsDict, xPos, innerBoard, outerBoard, playerColor
    ):
        self.name = name
        self.cellDict = cellDict
        self.roomsDict = roomsDict
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
        # upper labels
        self.lives = 3
        self.money = 1500
        # states
        self.buyingSecret = False
        self.removeInnerBoard = False
        self.showRooms = False
        self.roomsDrawn = False
        # rooms and secrets
        self.selectedRoom = None
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
            self.drawSecret('character secret', self.selectedRoom.characterSecret)

        elif self.selectedRoom.roomSecretOwner == None:
            pass
    
    def drawSecret(self, secretType, secretString):
        centerX = self.innerLeft + (self.innerSize / 2)
        drawLabel(f'The {secretType} is:', centerX, self.innerTop + 110)
        currY = self.innerTop + 130
        for line in secretString.splitlines():
            currY += 20
            drawLabel(line, centerX, currY)

    # this should be called at the end of displaying the secret
    def yesBuySecret(self):
        priceOfSecret = self.currCell.price
        self.editMoney(-priceOfSecret)
        self.updateOwnership()

    def editMoney(self, money):
        self.money += money
    
    def updateOwnership(self):
        self.currCell.secretOwned = True
        self.currCell.secretOwner = self.name
        # change the selectedRoom secret ownership when user closes the popup

    def checkOnCell(self):
        if isinstance(self.currCell, Secret):
            # checks the secretOwned status of the cell, not the room
            if self.currCell.secretOwned == False and self.removeInnerBoard == False:
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
                    self.drawSelectedRoom()

                # change the cell and room secret ownership state at the end:
                # self.currCell.secretOwned = True  
                # self.currCell.secretOwner = self.name
                # self.selectedRoom.characterSecretOwner = self.name  
                
            # need to check how to break lines for room secret

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


def redrawAll(app):
    # drawLabel('112 Murder Mystery', 200, 200)
    # drawLabel(app.paused, 200, 250)

    app.gameBoard.drawBoard()


def onMousePress(app, mouseX, mouseY):
    # change the player name based on whose turn it is --> create a variable

    # check if clicked on yes or no buttons
    if (app.gameBoard.player1.buyingSecret == True) and (app.gameBoard.player1.showRooms == False):
        # check if mouseX and mouseY is within bounds of Yes or No box
        if (app.gameBoard.player1.yesBtnLeft <= mouseX <= (app.gameBoard.player1.yesBtnLeft + app.gameBoard.player1.btnW) 
            and app.gameBoard.player1.yesBtnTop <= mouseY <= (app.gameBoard.player1.yesBtnTop + app.gameBoard.player1.btnH)
        ):
            print("yes")

            app.gameBoard.player1.showRooms = (
                True  # change this state would trigger draw options for rooms
            )
            # app.gameBoard.player1.yesBuySecret() do this after the player gets the secret
            # print(app.gameBoard.cellDict[app.gameBoard.player1.currCell.cellId])
        elif app.gameBoard.player1.noBtnLeft <= mouseX <= (
            app.gameBoard.player1.noBtnLeft + app.gameBoard.player1.btnW
        ) and app.gameBoard.player1.noBtnTop <= mouseY <= (
            app.gameBoard.player1.noBtnTop + app.gameBoard.player1.btnH
        ):
            print("no")
            app.gameBoard.player1.buyingSecret = False
            app.gameBoard.player1.removeInnerBoard = True

    # check which room the player selected
    if app.gameBoard.player1.roomsDrawn == True:  # need to set this state back to False
        for i in range(len(app.gameBoard.player1.roomsDict) // 2):  # 3
            rectTop = (app.gameBoard.player1.roomBtnTop + i * (app.gameBoard.player1.btnH + 20) + 50)
            col1Left = app.gameBoard.player1.roomBtnCol1Left
            col2Left = app.gameBoard.player1.roomBtnCol2Left
            btnW = app.gameBoard.player1.btnW
            btnH = app.gameBoard.player1.btnH
            # column 1
            if col1Left <= mouseX <= col1Left + btnW:
                if rectTop <= mouseY <= rectTop + btnH:
                    print(f"clicked on {app.gameBoard.player1.roomsDict[i]}")
                    app.gameBoard.player1.selectedRoom = (
                        app.gameBoard.player1.roomsDict[i]
                    )
                    app.gameBoard.player1.showRooms = False
            # column 2
            elif col2Left <= mouseX <= col2Left + btnW:
                if rectTop <= mouseY <= rectTop + btnH:
                    print(f"clicked on {app.gameBoard.player1.roomsDict[i+3]}")
                    app.gameBoard.player1.selectedRoom = (
                        app.gameBoard.player1.roomsDict[i + 3]
                    )


def onKeyPress(app, key):
    if key == "c":
        print("running camera")
        # runCamera()
        print("finished running camera")
    if key.isdigit():
        print(key)
        app.gameBoard.player1.updatePlayerCell(int(key))


def onStep(app):
    app.paused = not app.paused


runApp()
