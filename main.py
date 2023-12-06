from cmu_graphics import *
import copy, random, string, json
import jsonpickle
from imageManager import loadImages
from handDetection import runCamera
from dice import Dice # imports the class Dice


"""
read these articles on writing and reading json file: 
https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
https://www.freecodecamp.org/news/loading-a-json-file-in-python-how-to-read-and-parse-json/
https://www.w3docs.com/snippets/python/how-to-make-a-class-json-serializable.html#:~:text=In%20order%20to%20make%20a,can%20be%20converted%20to%20JSON.
https://stackoverflow.com/questions/22281059/set-object-is-not-json-serializable
https://medium.com/@KaranDahiya2000/modify-json-fields-using-python-1b2d88d16908
https://stackoverflow.com/questions/10895028/python-append-to-array-in-json-object
"""

'''
read this on using %s
https://www.javatpoint.com/python-s-string-formatting#:~:text=The%20%25s%20allow%20us%20to,value%20to%20string%20data%20type.
'''


'''
read this on converting string to variable names:
https://www.geeksforgeeks.org/convert-string-into-variable-name-in-python/
'''


class Colors:
    def __init__(self, name):
        self.name = name
        self.dustyBlue = rgb(116, 136, 168)
        self.mossGreen = rgb(89, 125, 92)
        self.sand = rgb(247, 246, 228)
        self.moonLight = rgb(255, 249, 199)
    
    def to_json(self):
        return {
            'name': self.name,
            'dustyBlue': self.dustyBlue,
            'mossGreen': self.mossGreen,
            'sand': self.sand
        }
    
    def __hash__(self):
        return hash(str(self))
    
    def __repr__(self):
        return f"Colors(dustyBlue, mossGreen, sand)"
    
    def __eq__(self, other):
        return isinstance(other, Colors)
    
    
        
class Guess:
    def __init__(self, charGuess, weaponGuess, roomGuess, name='playerGuess'):
        self.name = name
        self.charGuess = self.capitalization(charGuess)
        self.weaponGuess = self.capitalization(weaponGuess)
        self.roomGuess = self.capitalization(roomGuess)

    def to_json(self):
        return {
            'name': self.name,
            'charGuess': self.charGuess,
            'weaponGuess': self.weaponGuess,
            'roomGuess': self.roomGuess  
        }
    
    def __repr__(self):
        return f"{self.charGuess}, using {self.weaponGuess}, killed Colonel Mustard in the {self.roomGuess}."
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return (isinstance(other, Guess) and self.charGuess == other.charGuess and 
                self.weaponGuess == other.weaponGuess and self.roomGuess == other.roomGuess)
    
    def capitalization(self, s):
        if s == "":
            return s
        newString = ""
        for word in s.split(" "):
            newString += word[0].upper() + word[1:]
            newString += " "
        return newString


class PlayerNotes:
    def __init__(self, currPlayer, notesBoardLeft, notesBoardTop, notesBoardW, notesBoardH, colors):
        self.currPlayer = currPlayer
        self.notesBoardLeft = notesBoardLeft
        self.notesBoardTop = notesBoardTop
        self.notesBoardW = notesBoardW
        self.notesBoardH = notesBoardH
        self.colors = colors
        self.name = str(self)
        
    def to_json(self):
        return {
            "currPlayer": self.currPlayer,
            "name": self.name
        }
    def __hash__(self):
        return hash(str(self))
    def __repr__(self):
        return f"Player notes of {self.currPlayer.name}"
    def __eq__(self, other):
        return isinstance(other, PlayerNotes) and self.currPlayer == other.currPlayer
    
    def drawIndividualNotes(self, charSecretOwned, weaponSecretOwned, roomSecretOwned):
        xLeft = self.notesBoardLeft + (self.notesBoardW /20)
        currY = self.notesBoardTop + 80
        i = 0
        if charSecretOwned != set():
            drawLabel("Character Secret Owned:", xLeft, currY + 20 * i, size=16, align='left')
            i+= 1
            for secret in charSecretOwned:
                drawLabel(secret, xLeft, currY + 20* i, align='left')
                i+= 1
        
        if weaponSecretOwned != set():
            drawLabel("Weapon Secret Owned:", xLeft, currY + 20 * i, size=16, align='left')
            i += 1
            for secret in weaponSecretOwned:
                drawLabel(secret, xLeft, currY + 20* i, align='left')
                i+= 1
        
        if roomSecretOwned != set():
            drawLabel("Room Secret Owned:", xLeft, currY + 20 * i, size=16, align='left')
            i += 1
            for secret in roomSecretOwned:
                drawLabel(secret, xLeft, currY + 20* i, align='left')
                i+= 1
    
    def drawNotes(self):
        drawLabel(
            f"It is {self.currPlayer.name}'s turn.",
            self.notesBoardLeft + (self.notesBoardW/2),
            self.notesBoardTop - 40,
            size=20,
            fill='white'
        )
        
        drawRect(self.notesBoardLeft, self.notesBoardTop, self.notesBoardW, self.notesBoardH, fill=self.colors.sand)
        
        cx = self.notesBoardLeft + (self.notesBoardW /2)
        cy = self.notesBoardTop + (self.notesBoardH /2)
        drawLabel(f"{self.currPlayer.name} Notes", cx, self.notesBoardTop + 50)
        

        self.drawIndividualNotes(self.currPlayer.charSecretOwned, self.currPlayer.weaponSecretOwned, self.currPlayer.roomSecretOwned)
        

class Board:
    def __init__(self, width, height, rows, cols, imageDict):
        self.boardLoaded = False # will not be stored in json file
        self.imageDict = imageDict
        self.name = 'gameBoard'
        self.width = width  # 500
        self.height = height  # 500
        self.rows = rows  # 7
        self.cols = cols  # 7
        self.cellBorderWidth = 1
        self.cellSize = self.width / self.cols
        print(self.cellSize)
        self.boardLeft = 400 # was 150
        self.boardTop = 100
        self.colors = Colors('colors')
        self.dice = Dice(self.boardLeft, self.boardTop, self.width, self.height, self.colors)
        self.rollDiceState = False
        # inner box properties
        self.innerLeft = self.boardLeft + self.cellSize
        self.innerTop = self.boardTop + self.cellSize
        self.innerSize = self.width - (2 * self.cellSize)
        # instances of cell class
        self.cellDict = dict()
        self.isFirstIteration = True
        # players
        self.player1 = None
        self.player2 = None
        # rooms
        self.roomsDict = dict()
        # weapons
        self.weaponsDict = dict()  # [charName, weapon, bool for assignedToCell]
        # Alternate turns
        self.currTurn = None
        self.otherPlayer = None
        # make a guess
        self.makingAGuess = False
        self.textboxDict = dict()
        # player notes
        self.player1Notes = None
        self.player2Notes = None
    
    def to_json(self):
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "rows": self.rows,
            "cols": self.cols,
            "cellBorderWidth": self.cellBorderWidth,
            "cellSize": self.cellSize,
            "boardLeft": self.boardLeft,
            "boardTop": self.boardTop,
            "colors": self.colors,
            # inner box properties
            "innerLeft": self.innerLeft,
            "innerTop": self.innerTop,
            "innerSize": self.innerSize,
            # instances of cell class
            "cellDict": self.cellDict,
            "isFirstIteration": self.isFirstIteration,
            # players
            "player1": self.player1,
            "player2": self.player2,
            # rooms
            "roomsDict": self.roomsDict,
            # weapons
            "weaponsDict": self.weaponsDict,  # [charName, weapon, bool for assignedToCell]
            # Alternate turns
            "currTurn": self.currTurn,
            "otherPlayer": self.otherPlayer,
            # make a guess
            "makingAGuess": self.makingAGuess,
            "textboxDict": self.textboxDict,
            # player notes
            "player1Notes": self.player1Notes,
            "player2Notes": self.player2Notes
        }
        
    def __repr__(self):
        return f"Board({self.player1}, {self.player2})"
    
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return isinstance(other, Board) and self.player1 == other.player1 and self.player2 == other.player2

    def readJsonFile(self):
        # resume previous game
        # Opening JSON file
        with open('prevGame.json') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
    
        # update cellDict
        for cellNum in json_object["cellDict"]:
            # pseudo code: for propertyName in json_object["cellDict"][cellNum]:
                # propertyNameStr = propertyName
            gameBoardCell = self.cellDict[int(cellNum)]
            jsonCell = json_object["cellDict"][cellNum]
            if gameBoardCell.cellType == "secret":
                gameBoardCell.price = jsonCell["price"]
                gameBoardCell.secretOwned = jsonCell["secretOwned"]
                gameBoardCell.secretOwner = jsonCell["secretOwner"]
                gameBoardCell.secretRoom = jsonCell["secretRoom"]
                gameBoardCell.secretType = jsonCell["secretType"]
                gameBoardCell.secret = jsonCell["secret"]
                gameBoardCell.yesBuy = jsonCell["yesBuy"]
                gameBoardCell.yesRent = jsonCell["yesRent"]
            elif gameBoardCell.cellType == "oops":
                gameBoardCell.currPlayerChoice = jsonCell["currPlayerChoice"]
                gameBoardCell.murdererChoice = jsonCell["murdererChoice"]
                gameBoardCell.playerWonOops = jsonCell["playerWonOops"]
                gameBoardCell.tied = jsonCell["tied"]
            elif gameBoardCell.cellType == "weapon":
                gameBoardCell.weapon = jsonCell["weapon"]
                gameBoardCell.weaponChar = jsonCell["weaponChar"]
                gameBoardCell.cellOccupied = jsonCell["cellOccupied"]
        
        # update roomsDict
        for roomNum in json_object["roomsDict"]:
            gameBoardRoom = self.roomsDict[int(roomNum)]
            jsonRoom = json_object["roomsDict"][roomNum]
            gameBoardRoom.accessible = jsonRoom["accessible"]
            gameBoardRoom.characterSecretOwner = jsonRoom["characterSecretOwner"]
            gameBoardRoom.roomSecretOwner = jsonRoom["roomSecretOwner"]
        
        # update weaponsDict
        for weaponNum in json_object["gameBoard"]["weaponsDict"]:
            self.weaponsDict[int(weaponNum)] = json_object["gameBoard"]["weaponsDict"][weaponNum]
        
        # updates textboxDict
        for textboxNum in json_object["textboxDict"]:
            self.textboxDict[int(textboxNum)].selected = json_object["textboxDict"][textboxNum]["selected"]
            self.textboxDict[int(textboxNum)].label = json_object["textboxDict"][textboxNum]["label"]
        
        self.makingAGuess = json_object["gameBoard"]["makingAGuess"]
        
        # reassign properties to player
        for playerName in [self.player1, self.player2]:
            # playerName is app object, jsonPlayer is json file object
            jsonPlayer = json_object[playerName.name]
            playerName.isCurrPlayer = jsonPlayer["isCurrPlayer"]
            playerName.cellDict = self.cellDict
            playerName.roomsDict = self.roomsDict
            playerName.weaponsDict = self.weaponsDict
            playerName.currCellNum = jsonPlayer["currCellNum"]
            playerName.currCell = self.cellDict[playerName.currCellNum]
            playerName.playerColor = jsonPlayer["playerColor"]
            playerName.lives = jsonPlayer["lives"]
            playerName.money = jsonPlayer["money"]
            playerName.buyingSecret = jsonPlayer["buyingSecret"]
            playerName.removeInnerBoard = jsonPlayer["removeInnerBoard"]
            playerName.showRooms = jsonPlayer["showRooms"]
            playerName.roomsDrawn = jsonPlayer["roomsDrawn"]
            playerName.rentingSecret = jsonPlayer["rentingSecret"]
            playerName.processingRent = jsonPlayer["processingRent"]
            playerName.rentOKRect = jsonPlayer["rentOKRect"]
            playerName.showWeaponSecret = jsonPlayer["showWeaponSecret"]
            playerName.weaponOKRect = jsonPlayer["weaponOKRect"]
            playerName.processingWeaponSecret = jsonPlayer["processingWeaponSecret"]
            playerName.shownWeaponSecret = jsonPlayer["shownWeaponSecret"]
            playerName.showOopsInstructions = jsonPlayer["showOopsInstructions"]
            playerName.oopsInstructionsRect = jsonPlayer["oopsInstructionsRect"]
            playerName.oopsInPlay = jsonPlayer["oopsInPlay"]
            playerName.shownOopsInstructions = jsonPlayer["shownOopsInstructions"]
            playerName.charSecretOwned = set(jsonPlayer["charSecretOwned"])
            playerName.roomSecretOwned = set(jsonPlayer["roomSecretOwned"])
            playerName.weaponSecretOwned = set(jsonPlayer["weaponSecretOwned"])
            selectedRoomStr = jsonPlayer["selectedRoom"]
            if selectedRoomStr != None:
                roomIdx = selectedRoomStr[0:1]
                playerName.selectedRoom = self.roomsDict[int(roomIdx)]
            else:
                playerName.selectedRoom = jsonPlayer["selectedRoom"]
            playerName.secretOKRect = jsonPlayer["secretOKRect"]
            playerName.textboxDict = self.textboxDict
            playerName.checkGuessRect = jsonPlayer["checkGuessRect"]
            playerName.wrongGuess = jsonPlayer["wrongGuess"]
            
        # create new instances of playerNOtes
        self.player1Notes = PlayerNotes(self.player1, self.boardLeft - 350, self.boardTop, 250, self.height, self.colors)
        self.player2Notes = PlayerNotes(self.player2, self.boardLeft - 350, self.boardTop, 250, self.height, self.colors)

    
    def drawBoard(self):
        originalCellId = 0
        # only passes in originalCellId when app is first created
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
                self.cellDict[cellNum].name = str(self.cellDict[cellNum])
            self.createRooms()

            # initiate makeAGuess textboxes
            self.textboxDict = self.initiateTextboxes()

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
                self.weaponsDict,
                self.textboxDict,
                self.imageDict
            )
            self.player2 = Player(
                "player2",
                self.cellDict,
                self.roomsDict,
                20,
                (self.innerLeft, self.innerTop, self.innerSize),
                (self.boardLeft, self.boardTop, self.width),
                "purple",
                self.weaponsDict,
                self.textboxDict,
                self.imageDict
            )


            self.currTurn = self.player1
            self.player1.isCurrPlayer = True
            # initiates player notes
            self.player1Notes = PlayerNotes(self.player1, self.boardLeft - 350, self.boardTop, 250, self.height, self.colors)
            self.player2Notes = PlayerNotes(self.player2, self.boardLeft - 350, self.boardTop, 250, self.height, self.colors)
            
            self.boardLoaded = True

            
            self.isFirstIteration = False
        else:
            # draw cell using the new cellDict
            for cellNum in self.cellDict:
                self.cellDict[cellNum].drawCell()
                self.cellDict[cellNum].drawCellType()
            # draw Player1
            self.player1.drawPlayer()
            # draw player2
            self.player2.drawPlayer()
            self.drawLowerBtns()
            if self.player2.isCurrPlayer == True:
                self.player2Notes.drawNotes()
            else:
                self.player1Notes.drawNotes()

    def initiateTextboxes(self):
        textboxLeft = self.innerLeft + (self.innerSize / 20) + 100
        textboxTop = self.innerTop + 85  # add + 85 + 60i
        textboxW = 200
        textboxH = 30
        color = self.colors.mossGreen
        charTextbox = Textbox(
            "charTextbox", textboxLeft, textboxTop, textboxW, textboxH, color, 0
        )
        weaponTextbox = Textbox(
            "weaponTextbox", textboxLeft, textboxTop + 60, textboxW, textboxH, color, 1
        )
        roomTextbox = Textbox(
            "roomTextbox", textboxLeft, textboxTop + 120, textboxW, textboxH, color, 2
        )
        return {0:charTextbox, 1:weaponTextbox, 2:roomTextbox}

    def createRooms(self):  # also add character weapons to the weaponsDict
        # need to change all char secret descriptions according to the linebreaks
        # Kitchen
        kitchenCharSecret = (
            "To most people, Mrs. White seems like an honest \n"
            + "and optimistic woman who runs Colonel Mustard’s kitchen \n"
            + "efficiently on a daily basis. Would anyone suspect that \n"
            + "she has covertly taken money from Mustard and stolen \n"
            + "valuable antiques to sell on the black market?"
        )
        kitchenRoomSecret = "Mustard was not in the kitchen at 9pm"
        kitchen = Rooms(
            "Kitchen", 0, "Mrs. White", kitchenCharSecret, kitchenRoomSecret
        )
        self.weaponsDict[0] = ["Mrs. White", "Candlestick", False]
        self.roomsDict[0] = kitchen

        # Master Bedroom
        bedroomCharSecret = (
            "Everyone knows Colonel Mustard is a decorated war \n"
            + "hero. He is also from a venerated and wealthy family.\n"
            + "Ironically, he wasn’t actually in the battle for which \n"
            + "he was awarded his most prestigious medal."
        )
        bedroomRoomSecret = "Mustard was not in the bedroom at 9pm"
        bedroom = Rooms(
            "Master Bedroom", 1, "Colonel Mustard", bedroomCharSecret, bedroomRoomSecret
        )
        self.weaponsDict[1] = ["Colonel Mustard", "Pistol", False]
        self.roomsDict[1] = bedroom
        # Billiard Room
        billiardCharSecret = (
            "Mr. Green is a businessman who is a closeted homosexual.\n"
            + "He is desperately in love with his partner and wants to \n"
            + "get married, but Mustard used his influence to make gay \n"
            + "marriage illegal in his state. Green now can’t pursue \n"
            + "his love –– he wants revenge…"
        )
        billiardRoomSecret = "Mustard was not in the billiard room at 9pm"
        billiard = Rooms(
            "Billiard Room", 2, "Mr. Green", billiardCharSecret, billiardRoomSecret
        )
        self.weaponsDict[2] = ["Mr. Green", "Dagger", False]
        self.roomsDict[2] = billiard
        # Study
        studyCharSecret = (
            "Plum is a professor of antiquities. He identifies \n"
            + "counterfeits and occasionally makes them, including\n"
            + "his PhD certificate. Beware, Plum knows that \n"
            + "Mustard knows his secret…"
        )
        studyRoomSecret = "Mustard was not in the study room at 9pm"
        study = Rooms("Study", 3, "Professor Plum", studyCharSecret, studyRoomSecret)
        self.weaponsDict[3] = ["Professor Plum", "Rope", False]
        self.roomsDict[3] = study
        # Parlor
        parlorCharSecret = (
            "Mrs. Peacock is a lawyer and the mother of a soldier\n"
            + "under Mustard. What an honor you might think! \n"
            + "Well, Mustard killed her son because\n"
            + "her son attempted to unveil Mustard’s secret."
        )
        parlorRoomSecret = "Mustard was in the Parlor at approximately 9pm"
        parlor = Rooms("Parlor", 4, "Mrs. Peacock", parlorCharSecret, parlorRoomSecret)
        self.weaponsDict[4] = ["Mrs. Peacock", "Hammer", False]
        self.roomsDict[4] = parlor
        # Ballroom
        ballroomCharSecret = (
            "Miss Scarlet is a movie actress whose career is crumbling.\n"
            + "She also lost a lot of money due to gambling.\n"
            + "Hmmm, life must be hard for her right now."
        )
        ballroomRoomSecret = "Mustard was not in the Ballroom at 9pm."
        ballroom = Rooms(
            "Ballroom", 5, "Miss Scarlet", ballroomCharSecret, ballroomRoomSecret
        )
        self.weaponsDict[5] = ["Miss Scarlet", "Poison", False]
        self.roomsDict[5] = ballroom

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
            cellName = Oops(originalCellId, "oops", cellLeft, cellTop, cellSize)
            self.cellDict[originalCellId] = cellName
            # self.originalCellId.append(cellName)
        elif originalCellId == 17:
            cellName = Cell(originalCellId, "Go", cellLeft, cellTop, cellSize)
            self.cellDict[originalCellId] = cellName
            # self.originalCellId.append(cellName)
        else:
            # price for each secret is 100
            cellName = Secret(
                originalCellId, "secret", cellLeft, cellTop, cellSize, 100
            )
            self.cellDict[originalCellId] = cellName
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
        # save progress
        drawRect(self.boardLeft - 350, self.boardTop + self.height + 20, 250, 40, fill=self.colors.dustyBlue, border='black')
        drawLabel("Save Progress", self.boardLeft - 350 + 125, self.boardTop + self.height + 40, size=20)
        
        # make a guess
        drawRect(
            self.boardLeft - 15,
            self.boardTop + self.height + 20,
            150,
            40,
            fill=self.colors.dustyBlue,
            border="black",
        )
        drawLabel(
            "Make a guess",
            self.boardLeft + 60,
            self.boardTop + self.height + 40,
            size=20,
        )

        # switch turns
        drawRect(
            self.boardLeft + 60 + 400 - 100,
            self.boardTop + self.height + 20,
            200,
            40,
            fill=self.colors.dustyBlue,
            border="black",
        )
        self.dice.drawRollDiceBtn()
        
        drawLabel(
            "click here to switch turns",
            self.boardLeft + 60 + 400,
            self.boardTop + self.height + 40,
            size=16,
        )


class Cell:
    cellDict = dict()

    def __init__(self, originalCellId, cellType, cellLeft, cellTop, cellSize):
        self.name = ''
        self.cellType = cellType  # secret, oops, weapon
        self.originalCellId = originalCellId
        self.cellDictId = None  # will be changed when updating cellDict
        self.cellLeft = cellLeft
        self.cellTop = cellTop
        self.cellSize = cellSize
        self.cx = cellLeft + cellSize / 2
        self.cy = cellTop + cellSize / 2
    
    def to_json(self):
        return {
            "name": self.name,
            "cellType": self.cellType,
            "originalCellId": self.originalCellId,
            "cellDictId": self.cellDictId,
        }

    def __repr__(self):
        return f"{self.cellDictId}. {self.cellType}"

    def __eq__(self, other):
        return (
            isinstance(other, Cell)
            and (self.cellType == other.cellType)
            and (self.name == other.name)
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


class Oops(Cell):
    def __init__(self, originalCellId, cellType, cellLeft, cellTop, cellSize):
        super().__init__(originalCellId, cellType, cellLeft, cellTop, cellSize)
        self.rockPaperScissors = ["rock", "paper", "scissors"]
        self.currPlayerChoice = None
        self.murdererChoice = None
        self.playerWonOops = None
        self.tied = False
    
    def to_json(self):
        return {
            "name": self.name,
            "cellType": self.cellType,
            "rockPaperScissors": self.rockPaperScissors,
            "currPlayerChoice": self.currPlayerChoice,
            "murdererChoice": self.murdererChoice,
            "playerWonOops": self.playerWonOops,
            "tied": self.tied
        }

    def reset(self):
        self.currPlayerChoice = None
        self.murdererChoice = None
        self.playerWonOops = None
        self.tied = False


class Weapon(Cell):
    def __init__(self, originalCellId, cellType, cellLeft, cellTop, cellSize):
        super().__init__(originalCellId, cellType, cellLeft, cellTop, cellSize)
        self.weapon = None
        self.weaponChar = None
        self.cellOccupied = False
    
    def to_json(self):
        return {
            "name": self.name,
            "cellType": self.cellType,
            "weapon": self.weapon,
            "weaponChar": self.weaponChar,
            "cellOccupied": self.cellOccupied
        }


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
        self.secretChar = None
        self.secret = None
        self.yesBuy = False
        self.yesRent = False
    
    def to_json(self):
        return {
            "name": self.name,
            "cellType": self.cellType,
            "secretChar": self.secretChar,
            "price": self.price,
            "secretOwned": self.secretOwned,
            "secretOwner": self.secretOwner,
            "secretRoom": self.secretRoom,
            "secretType": self.secretType,
            "secret": self.secret,
            "yesBuy": self.yesBuy,
            "yesRent": self.yesRent,
        }

    def __repr__(self):
        return f"{self.cellDictId}. {self.cellType}, owner is {self.secretOwner}, secretRoom is {self.secretRoom}, secret is {self.secret}"

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
    
    def to_json(self):
        return {
            "name": self.name,
            "id": self.id,
            "accessible": self.accessible,
            "character": self.character,
            "characterSecret": self.characterSecret,
            "roomSecret": self.roomSecret,
            "characterSecretOwner": self.characterSecretOwner,
            "roomSecretOwner": self.roomSecretOwner
        }

    def __repr__(self):
        return f"{self.id}. {self.name}({self.character}, {self.characterSecretOwner}, {self.roomSecretOwner})"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return isinstance(other, Rooms) and (other.name == self.name)

    def checkSecret(self):
        if self.characterSecretOwner == None:
            return f"You can buy a character secret"
        elif self.roomSecretOwner == None:
            return f"You can buy a room secret"
        else:
            return f"The secrets in this room have been claimed."


class Textbox:
    def __init__(self, name, rectLeft, rectTop, rectW, rectH, fill, dictKey):
        self.name = name
        self.rectLeft = rectLeft
        self.rectTop = rectTop
        self.rectW = rectW
        self.rectH = rectH
        self.fill = fill
        self.dictKey = dictKey
        self.selected = False
        # self.addingKey = False
        self.label = ""
    
    def to_json(self):
        return {
            "name": self.name,
            "rectLeft": self.rectLeft,
            "rectTop": self.rectTop,
            "rectW": self.rectW,
            "rectH": self.rectH,
            "fill": self.fill,
            "dictKey": self.dictKey,
            "selected": self.selected,
            "label": self.label
        }

    def __repr__(self):
        return (
            f"Textbox({self.name}, selected is {self.selected}, text is {self.label})"
        )

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return isinstance(other, Textbox) and self.name == other.name

    def reset(self):
        self.selected = False
        self.label = ""

    def drawTextbox(self):
        if self.selected == True:
            border = "red"
            color = None
        else:
            border = None
            color = self.fill
        drawRect(
            self.rectLeft,
            self.rectTop,
            self.rectW,
            self.rectH,
            fill=color,
            border=border,
        )

        drawLabel(
            self.label,
            self.rectLeft + (0.5 * self.rectW),
            self.rectTop + (0.5 * self.rectH),
            fill='white'
        )

    def addLabel(self, key):
        self.label += key

    def deleteOneChar(self):
        self.label = self.label[:-1]


class Player:
    def __init__(
        self,
        name,
        cellDict,
        roomsDict,
        xPos,
        innerBoard,
        outerBoard,
        playerColor,
        weaponsDict,
        textboxDict,
        imageDict,
    ):
        self.name = name
        self.isCurrPlayer = False
        self.cellDict = cellDict
        self.roomsDict = roomsDict
        self.weaponsDict = weaponsDict
        self.imageDict = imageDict
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
        self.colors = Colors('colors')
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
        self.shownWeaponSecret = False  # resets to False when gets to a new cell
        # oops states
        self.showOopsInstructions = (
            False  # connects to self.currCell.shownOopsInstructions state
        )
        self.oopsInstructionsRect = None
        self.oopsInPlay = False
        self.shownOopsInstructions = False  # for ties
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
        # check if guessed right
        self.textboxDict = textboxDict  # imported from gameboard
        self.checkGuessRect = None
        self.wrongGuess = False

    def to_json(self):
        return {
            "name": self.name,
            "isCurrPlayer": self.isCurrPlayer,
            "cellDict": self.cellDict,
            "roomsDict": self.roomsDict,
            "weaponsDict": self.weaponsDict,
            "currCellNum": self.currCellNum,
            "currCell": self.currCell,
            "playerColor": self.playerColor,
            # upper labels
            "lives": self.lives,
            "money": self.money,
            # states
            "buyingSecret": self.buyingSecret,
            "removeInnerBoard": self.removeInnerBoard,
            "showRooms": self.showRooms,
            "roomsDrawn": self.roomsDrawn,
            # renting states
            "rentingSecret": self.rentingSecret,
            "processingRent": self.processingRent,
            "rentOKRect": self.rentOKRect,
            # weapon states
            "showWeaponSecret": self.showWeaponSecret,
            "weaponOKRect": self.weaponOKRect,
            "processingWeaponSecret": self.processingWeaponSecret,
            "shownWeaponSecret": self.shownWeaponSecret,  # resets to False when gets to a new cell
            # oops states
            "showOopsInstructions": self.showOopsInstructions,
            "oopsInstructionsRect": self.oopsInstructionsRect,
            "oopsInPlay": self.oopsInPlay,
            "shownOopsInstructions": self.shownOopsInstructions,  # for ties
            # rooms and secrets
            "charSecretOwned": self.charSecretOwned,
            "roomSecretOwned": self.roomSecretOwned,
            "weaponSecretOwned": self.weaponSecretOwned,
            "selectedRoom": self.selectedRoom,
            "secretOKRect": self.secretOKRect,
            # check if guessed right
            "textboxDict": self.textboxDict,
            "checkGuessRect": self.checkGuessRect,
            "wrongGuess": self.wrongGuess
        }

    def __repr__(self):
        return f"{self.name}"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return isinstance(other, Player) and self.name == other.name

    def updatePlayerCoordinates(self):
        self.cx = self.currCell.cx + self.dX
        self.cy = self.currCell.cy

    def updatePlayerCell(self, steps):  # this should be called when rolled a dice
        # before moving to a new cell, reset the state of the current cell
        if isinstance(self.currCell, Oops):
            self.shownOopsInstructions = False
        if isinstance(self.currCell, Weapon):
            self.shownWeaponSecret = False

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
                fill='white'
            )
            drawLabel(
                f"{self.name} money: ${self.money}",
                self.boardLeft + 35,
                self.boardTop - 40,
                size=20,
                fill='white'
            )
        elif self.name == "player2":
            drawLabel(
                f"{self.name} lives: {self.lives}",
                self.boardLeft + self.boardSize - 35,
                self.boardTop - 70,
                size=20,
                fill='white'
            )
            drawLabel(
                f"{self.name} money: ${self.money}",
                self.boardLeft + self.boardSize - 35,
                self.boardTop - 40,
                size=20,
                fill='white'
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
            size=20,
            fill='white'
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
        drawLabel(
            "Please select a room to investigate",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + (self.innerSize / 2) - 100,
            fill='white'
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
        drawImage(self.imageDict[self.selectedRoom.name], 650, 350, align="center", width=self.innerSize, height=self.innerSize)
        drawLabel(
            f"You have entered the {self.selectedRoom.name}",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 50,
            size=20,
            fill='white'
        )
        if self.selectedRoom.characterSecretOwner == None:
            secretDisplayed = "characterSecret"
            self.drawSecret("character secret", self.selectedRoom.characterSecret)

        # shows the room secret if the character secret is already owned
        elif self.selectedRoom.roomSecretOwner == None:
            secretDisplayed = "roomSecret"
            self.drawSecret("room secret", self.selectedRoom.roomSecret)
        # draws the OK button in the drawSecret method

        # updates ownership if the OK button is clicked
        if self.buyingSecret == False:
            if secretDisplayed == "characterSecret":
                self.charSecretOwned.add(
                    self.selectedRoom.character
                )  # updates list of player secrets
                self.selectedRoom.characterSecretOwner = self.name
                self.currCell.secretRoom = self.selectedRoom.name
                self.currCell.secretType = "characterSecret"
                self.currCell.secretChar = self.selectedRoom.character
                self.currCell.secret = self.selectedRoom.characterSecret
            elif secretDisplayed == "roomSecret":
                self.roomSecretOwned.add(self.selectedRoom.roomSecret)
                self.selectedRoom.roomSecretOwner = self.name
                self.currCell.secretRoom = self.selectedRoom.name
                self.currCell.secretType = "roomSecret"
                self.currCell.secretChar = self.selectedRoom.character
                self.currCell.secret = self.selectedRoom.roomSecret
            self.yesBuySecret()

    def drawSecret(self, secretType, secretString):
        centerX = self.innerLeft + (self.innerSize / 2)
        drawRect(centerX - 100, self.innerTop + 95, 200, 30, fill='black', opacity= 80)
        drawLabel(f"The {secretType} is:", centerX, self.innerTop + 110, fill='white')
        currY = self.innerTop + 130
        for line in secretString.splitlines():
            currY += 20
            drawRect(centerX - 170, currY-15, 340, 30, fill='black', opacity= 80)
            drawLabel(line, centerX, currY, fill='white')

        # OK button
        dustyBlue = rgb(116, 136, 168)
        drawRect(centerX - 50, currY + 50, 100, 40, fill=dustyBlue)
        drawLabel("OK", centerX, currY + 70)
        self.secretOKRect = (centerX - 50, currY + 50, 100, 40)

    def drawRoomNotAvailable(self):
        drawLabel(
            f"Sorry, the secrets in {self.selectedRoom.name}",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 50,
            size=16,
            fill='white'
        )
        drawLabel(
            f"have been owned.",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 70,
            size=16,
            fill='white'
        )
        drawLabel(
            f"Please select a different room.",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 95,
            size=16,
            fill='white'
        )

        drawRect(
            self.innerLeft + (self.innerSize / 2) - 50,
            self.innerTop + 150,
            100,
            40,
            fill=self.colors.dustyBlue,
        )
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
        drawLabel(
            "The secret of this cell has already been owned.",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + (self.innerSize / 2) - 130,
            size=16,
            fill='white'
        )
        drawLabel(
            "You'll need to pay a rent.",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + (self.innerSize / 2) - 100,
            size=16,
            fill='white'
        )
        # OK label
        drawRect(
            self.yesBtnLeft,
            self.yesBtnTop,
            self.btnW,
            self.btnH,
            fill=self.colors.mossGreen,
        )
        drawLabel(f"OK (Pay ${int(self.currCell.price*.75)})", yesCX, yesCY)
        self.rentOKRect = (self.yesBtnLeft, self.yesBtnTop, self.btnW, self.btnH)

    def drawRentSecret(self):
        drawImage(self.imageDict[self.currCell.secretRoom], 650, 350, align="center", width=self.innerSize, height=self.innerSize)
        drawLabel(
            f"You have entered the {self.currCell.secretRoom}",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 50,
            size=20,
            fill='white'
        )
        self.drawSecret(self.currCell.secretType, self.currCell.secret)

        if self.rentingSecret == False:
            self.processRentMethod()

    def processRentMethod(self):
        # the + - money is done in the onclick of APP
        if self.currCell.secretType == "characterSecret":
            self.charSecretOwned.add(self.currCell.secretChar)
        elif self.currCell.secretType == "roomSecret":
            self.roomSecretOwned.add(self.currCell.secret)
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
                self.currCell.weaponChar = self.weaponsDict[i][
                    0
                ]  # update cell char info
                self.currCell.weapon = self.weaponsDict[i][1]  # update cell weapon info
                self.weaponsDict[i][
                    2
                ] = True  # indicate that this weapon clue has been claimed
                self.showWeaponSecret = True
                self.currCell.cellOccupied = True
                break

    def drawWeaponSecret(self):
        centerX = self.innerLeft + (self.innerSize / 2)
        drawLabel(
            f"{self.currCell.weaponChar}'s weapon is {self.currCell.weapon}.",
            centerX,
            self.innerTop + 110,
            size=20,
            fill='white'
        )
        btnX = centerX - 50
        btnY = self.innerTop + 110 + 100

        # OK button
        drawRect(btnX, btnY, 100, 40, fill=self.colors.dustyBlue)
        drawLabel("OK", centerX, btnY + 20)
        self.weaponOKRect = (btnX, btnY, 100, 40)

    def processWeaponSecret(self):
        self.weaponSecretOwned.add(
            f"{self.currCell.weaponChar}'s weapon is {self.currCell.weapon}."
        )
        self.processingWeaponSecret = False
        self.showWeaponSecret = False
        self.shownWeaponSecret = True

    def drawOopsInstructions(self):
        drawLabel(
            f"The murderer has noticed you:",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 50,
            size=20,
            fill='white'
        )
        drawLabel(
            f"Beat him in a game of rock, paper, ",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 80,
            size=16,
            fill='white'
        )
        drawLabel(
            f"and scissors to win investigation funds!",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 100,
            size=16,
            fill='white'
        )
        drawLabel(
            f"Click on 'rock', 'paper', or 'scissors'",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 130,
            size=16,
            fill=self.colors.moonLight
        )

        centerX = self.innerLeft + (self.innerSize / 2)
        btnX = centerX - 50
        btnY = self.innerTop + 110 + 100

        # OK button
        drawRect(btnX, btnY, 100, 40, fill=self.colors.dustyBlue)
        drawLabel("OK", centerX, btnY + 20)
        self.oopsInstructionsRect = (btnX, btnY, 100, 40)

    def drawOopsPlayingScreen(self):
        drawLabel(
            f"3 . . 2 . . 1 . .",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 50,
            size=30,
            fill=self.colors.moonLight
        )
        if self.currCell.currPlayerChoice == None:
            drawLabel(
                f"You choose: ",
                self.innerLeft + (self.innerSize / 20),
                self.innerTop + 100,
                size=18,
                align="left",
                fill='white'
            )
            # draw the rock, paper, scissors btn
            for i in range(len(self.currCell.rockPaperScissors)):
                x = self.innerLeft + (self.innerSize / 80) + 90 * (i + 1)
                y = self.innerTop + 100 + 50
                drawRect(x - 40, y - 15, 80, 30, fill="yellow")
                drawLabel(f"{self.currCell.rockPaperScissors[i]}", x, y, size=16)

            drawLabel(
                f"The Murderer choose: ?",
                self.innerLeft + (self.innerSize / 20),
                self.innerTop + 200,
                size=18,
                align="left",
                fill='white'
            )

            if self.currCell.tied == True:
                drawLabel(
                    f"You tied. You'll need to play another",
                    self.innerLeft + (self.innerSize / 2),
                    self.innerTop + 260,
                    size=16,
                    fill=self.colors.moonLight,
                )
                drawLabel(
                    f"round of rock, paper, and scissors.",
                    self.innerLeft + (self.innerSize / 2),
                    self.innerTop + 280,
                    size=16,
                    fill=self.colors.moonLight,
                )
        else:  # after the player makes a choice
            drawLabel(
                f"You chose: {self.currCell.currPlayerChoice}",
                self.innerLeft + (self.innerSize / 20),
                self.innerTop + 100,
                size=18,
                align="left",
                fill='white'
            )

            drawLabel(
                f"The Murderer chose: {self.currCell.murdererChoice}",
                self.innerLeft + (self.innerSize / 20),
                self.innerTop + 130,
                size=18,
                align="left",
                fill='white'
            )

            # checks the results for rock, paper, scissors
            result = self.checkOopsResults()
            if result == None:
                # would return to the previous screen
                self.currCell.currPlayerChoice = self.currCell.murdererChoice = None
                self.currCell.tied = True
            elif result == True:
                self.currCell.tied = False
                self.currCell.playerWonOops = True
                drawLabel(
                    f"{self.name} won!",
                    self.innerLeft + (self.innerSize / 2),
                    self.innerTop + 210,
                    size=16,
                    fill=self.colors.moonLight,
                )
                drawLabel(
                    f"You'll get $100 investigation fund.",
                    self.innerLeft + (self.innerSize / 2),
                    self.innerTop + 230,
                    size=16,
                    fill=self.colors.moonLight,
                )
            else:
                print(f"{self.name} lost.")
                self.currCell.tied = False
                self.currCell.playerWonOops = False
                drawLabel(
                    f"{self.name} lost.",
                    self.innerLeft + (self.innerSize / 2),
                    self.innerTop + 210,
                    size=16,
                    fill=self.colors.moonLight,
                )
                drawLabel(
                    f"You'll be deducted $200 investigation fund.",
                    self.innerLeft + (self.innerSize / 2),
                    self.innerTop + 230,
                    size=16,
                    fill=self.colors.moonLight,
                )
            if result == True or result == False:
                centerX = self.innerLeft + (self.innerSize / 2)
                btnX = centerX - 50
                btnY = self.innerTop + 270
                # OK button
                drawRect(btnX, btnY, 100, 40, fill=self.colors.dustyBlue)
                drawLabel("OK", centerX, btnY + 20)
                self.oopsInstructionsRect = (btnX, btnY, 100, 40)

    def checkOopsResults(self):
        # None --> tied, True --> currPlayer won, False --> Murderer won
        if self.currCell.currPlayerChoice == self.currCell.murdererChoice:
            return None
        elif (
            self.currCell.currPlayerChoice == "rock"
            and self.currCell.murdererChoice == "scissors"
        ):
            return True
        elif (
            self.currCell.currPlayerChoice == "paper"
            and self.currCell.murdererChoice == "rock"
        ):
            return True
        elif (
            self.currCell.currPlayerChoice == "scissors"
            and self.currCell.murdererChoice == "paper"
        ):
            return True
        else:
            return False

    def drawMakeAGuessScreen(self):
        charTextbox = self.textboxDict[0]
        weaponTextbox = self.textboxDict[1]
        roomTextbox = self.textboxDict[2]

        drawLabel(
            f"Please enter your guess.",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 50,
            size=20,
            fill='white'
        )
        drawLabel(
            f"Character: ",
            self.innerLeft + (self.innerSize / 20),
            self.innerTop + 100,
            size=20,
            align="left",
            fill='white'
        )
        charTextbox.drawTextbox()

        drawLabel(
            f"Weapon: ",
            self.innerLeft + (self.innerSize / 20),
            self.innerTop + 160,
            size=20,
            align="left",
            fill='white'
        )
        weaponTextbox.drawTextbox()

        drawLabel(
            f"Room: ",
            self.innerLeft + (self.innerSize / 20),
            self.innerTop + 220,
            size=20,
            align="left",
            fill='white'
        )
        roomTextbox.drawTextbox()

        drawRect(
            self.innerLeft + (self.innerSize / 2) - 50,
            self.innerTop + 280 - 20,
            100,
            40,
            fill=self.colors.dustyBlue,
        )
        # update the dimensions for checkGuessRect
        self.checkGuessRect = (
            self.innerLeft + (self.innerSize / 2) - 50,
            self.innerTop + 280 - 20,
            100,
            40,
        )
        drawLabel(
            f"Check",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 280,
            size=20,
        )
        
    def drawMadeAWrongGuess(self):
        drawLabel(
            f"Sorry this is not the correct answer.",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 50,
            size=20,
            fill='white'
        )
        drawLabel(
            f"The murderer has fooled you.",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 100,
            size=18,
            fill='white'
        )
        drawLabel(
            f"You are going to lose a life.",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 130,
            size=18,
            fill='white'
        )
        drawLabel(
            f"Reminder: having 0 lives or 0 money",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 160,
            size=16,
            fill=self.colors.moonLight
        )
        drawLabel(
            f"will result in you losing the game.",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 180,
            size=16,
            fill=self.colors.moonLight
        )
        drawRect(
            self.innerLeft + (self.innerSize / 2) - 50,
            self.innerTop + 280 - 20,
            100,
            40,
            fill=self.colors.dustyBlue,
        )
        # update the dimensions for checkGuessRect
        self.checkGuessRect = (
            self.innerLeft + (self.innerSize / 2) - 50,
            self.innerTop + 280 - 20,
            100,
            40,
        )
        drawLabel(
            f"OK",
            self.innerLeft + (self.innerSize / 2),
            self.innerTop + 280,
            size=20,
        )
        

    def checkOnCell(self):
        if isinstance(self.currCell, Secret):
            # checks the secretOwned status of the cell, not the room
            if self.currCell.secretOwned == False:
                if self.removeInnerBoard == False:
                    # change state
                    self.buyingSecret = True  # state
                    # self.drawInnerBoard()
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
                    if (
                        self.selectedRoom.characterSecretOwner == None
                        or self.selectedRoom.roomSecretOwner == None
                    ):
                        self.drawSelectedRoom()
                    else:
                        if self.roomsDrawn == False:
                            self.drawRoomNotAvailable()
                            # if click on OK, self.showRooms = True
            # process rent if cell secret has been owned
            if self.currCell.secretOwned == True:
                if self.currCell.secretOwner != self.name:
                    if self.removeInnerBoard == False:
                        self.rentSecretPopup()  # would create the rentOKRect
                    if (
                        self.rentingSecret == True
                    ):  # this state is changed when clicked 'ok' on popup
                        print("renting secret: should display secret of the cell")
                        self.drawRentSecret()
                    if self.processingRent == True:
                        self.processRentMethod()

                else:
                    # since you are the owner of the cell, don't need to pay rent
                    pass
        elif isinstance(self.currCell, Weapon):
            if self.currCell.cellOccupied == False:
                self.checkWeaponCellOwnership()
            elif self.currCell.cellOccupied == True and self.shownWeaponSecret == False:
                self.showWeaponSecret = True
            if (
                self.showWeaponSecret == True
            ):  # this will run if player clicked ok on checkWeaponCellOwnership
                self.drawWeaponSecret()
            if self.processingWeaponSecret == True:
                self.processWeaponSecret()
        elif isinstance(self.currCell, Oops):
            if self.shownOopsInstructions == False and self.removeInnerBoard == False:
                self.drawOopsInstructions()
            if self.oopsInPlay == True and self.removeInnerBoard == False:
                self.drawOopsPlayingScreen()
        else:
            self.removeInnerBoard = True

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
    app.width = 1000
    app.pause = True
    # for dice animation
    app.stepsPerSecond = 5
    app.stepsCounter = 0   
    app.imageDict = loadImages() # this returns the imageDict
    app.instructions = "You are invited to a wedding banquet on a lonely island,\n but on the day of the wedding, the groom \n died at 9PM. Everyone is grieving. \nYou are a detective that vows to find out \nwho, using what weapon, at which room, \nkilled the groom."
    app.colors = Colors('colors')
    app.instructionScreen = True
    app.resumePrevGame = False # not included in json file
    

    
def drawInstructionScreen(app):
    # draw instructions screen
    drawRect(0, 0, app.width, app.height, fill="black")
    drawImage(app.imageDict["beachWedding"], app.width/2, app.height/2, align="center", width=app.width, height=app.height)
    drawLabel("Wedding Mystery", app.width/2, 150, fill='white', size=36)
    
    centerX = app.width/2
    currY = 180
    for line in app.instructions.splitlines():
        currY += 30
        drawLabel(line, centerX, currY, fill='white', size = 16)
    
    drawRect(app.width/10 * 2.5 - 150, app.height/2 + 150 - 30, 300, 60, fill=app.colors.dustyBlue)
    drawLabel("Start New Game", app.width/10 * 2.5, app.height/2 + 150, fill='white', size=18)
    
    drawRect(app.width/10 * 7.5 - 150, app.height/2 + 150 - 30, 300, 60, fill=app.colors.dustyBlue)
    drawLabel("Resume Previous Game", app.width/10 * 7.5, app.height/2 + 150, fill='white', size=18)
    
def setupGame(app):
    app.playerWon = False
    app.playerLost = False
    app.gameBoard = Board(500, 500, 7, 7, app.imageDict)
    app.currPlayer = app.gameBoard.player1
    app.otherPlayer = app.gameBoard.player2
    app.answer = Guess("Mrs Peacock", "Hammer", "Parlor", "answer")
        
def restart(app):
    app.instructionScreen = True
    setupGame(app)
    


def redrawAll(app):
    if app.instructionScreen == True:
        drawInstructionScreen(app)
    else:
        drawImage(app.imageDict["oceanMoon"], app.width/2, app.height/2, align="center", width=app.width, height=app.height)
        app.gameBoard.drawBoard()
        
        # draws the make a guess screen
        if app.gameBoard.makingAGuess == True and app.currPlayer.wrongGuess != True:
            app.currPlayer.drawMakeAGuessScreen()
            
        # draw the dice animation
        if app.gameBoard.rollDiceState == True and app.playerSteps != None and app.pause == False:
            # draw the animation with the ramdom number of player steps from onMousePress
            app.gameBoard.dice.drawDice()
            
        # winning page
        if app.currPlayer != None:
            if app.playerWon == True:
                drawWinningScreen(app)
            elif app.playerLost == True:
                drawPlayerLostScreen(app)
            elif app.currPlayer.wrongGuess == True:
                app.currPlayer.drawMadeAWrongGuess()



def drawPlayerLostScreen(app):
    drawImage(app.imageDict["lonelyMansionOnSea"], app.width/2, app.height/2, align="center", width=app.width, height=app.height)
    drawLabel(f"{app.currPlayer.name} Lost.", app.width/2, app.height/2, align="center", size=40, fill='white')
    drawLabel(f"Press 'r' to restart game.", app.width/2, app.height/2 + 40, align="center", fill='white')
    
def drawWinningScreen(app):
    drawImage(app.imageDict["sunsetSea"], app.width/2, app.height/2, align="center", width=app.width, height=app.height)
    drawLabel(f"{app.currPlayer.name} Won!", app.width/2, app.height/2, align="center", size=40, fill='black')
    drawLabel(f"Press 'r' to restart game.", app.width/2, app.height/2 + 40, align="center", fill='black')

def checkMakeAGuess(app, x, y):
    rectLeft = app.gameBoard.boardLeft - 15
    rectTop = app.gameBoard.boardTop + app.gameBoard.height + 20
    rectW = 150
    rectH = 40
    if rectLeft <= x <= rectLeft + rectW and rectTop <= y <= rectTop + rectH:
        app.gameBoard.makingAGuess = True

def checkSaveProgress(app, mouseX, mouseY):
    rectLeft = app.gameBoard.boardLeft - 350
    rectTop = app.gameBoard.boardTop + app.gameBoard.height + 20
    rectW = 250
    rectH = 40
    if (rectLeft <= mouseX <= rectLeft + rectW and rectTop <= mouseY <= rectTop + rectH):
        print('save progress')
        saveToJson(app)
        
        
def saveToJson(app):
    # write to json file
    
    appPropertiesDict = {
        "name": "app",
        "height": app.height,
        "width": app.width,
        "paused": app.pause,
        "stepsPerSecond": app.stepsPerSecond,
        "playerWon": app.playerWon,
        "playerLost": app.playerLost,
        "gameboard": app.gameBoard, 
        "instructionScreen": app.instructionScreen,
        "currPlayer": app.currPlayer,
        "otherPlayer": app.otherPlayer, 
        "answer": app.answer
    }

    
    
    with open('prevGame.json') as openfile:
        # read JSON data
        data = json.load(openfile)
        
        # add app properties to json file
        data["appProperties"] = appPropertiesDict
        
        
        py_objects = [app.gameBoard, app.gameBoard.player1, app.gameBoard.player2]
        
        # add field
        for obj in py_objects:
            data[obj.name] = obj.to_json()
        
        
        # objects with instances of classes: app.gameBoard.cellDict, app.gameBoard.roomsDict, 
        # app.gameBoard.weaponsDict, app.gameBoard.textboxDict
        
        # initiate the new json object
        data["cellDict"] = {}
        # add to that json object
        for cell in app.gameBoard.cellDict:
            data["cellDict"][app.gameBoard.cellDict[cell].cellDictId] = app.gameBoard.cellDict[cell].to_json()
                
        # roomsDict
        data["roomsDict"] = {}
        for room in app.gameBoard.roomsDict:
            data["roomsDict"][app.gameBoard.roomsDict[room].id] = app.gameBoard.roomsDict[room].to_json()
        
        # textboxDict
        data["textboxDict"] = {}
        for textbox in app.gameBoard.textboxDict:
            data["textboxDict"][textbox] = app.gameBoard.textboxDict[textbox].to_json()
        
        newData = json.dumps(data, indent=4, default=set_default)
        
    with open("prevGame.json", "w") as outfile:
        outfile.write(newData)


def readJsonFile(app):
    # Opening JSON file
    with open('prevGame.json') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    
    # update gameBoard
    # use a for loop and reassign the properties of each object
    
    # update cellDict
    for cellNum in json_object["cellDict"]:
        gameBoardCell = app.gameBoard.cellDict[int(cellNum)]
        jsonCell = json_object["cellDict"][cellNum]
        if gameBoardCell.cellType == "secret":
            gameBoardCell.price = jsonCell["price"]
            gameBoardCell.secretOwned = jsonCell["secretOwned"]
            gameBoardCell.secretOwner = jsonCell["secretOwner"]
            gameBoardCell.secretRoom = jsonCell["secretRoom"]
            gameBoardCell.secretType = jsonCell["secretType"]
            gameBoardCell.secret = jsonCell["secret"]
            gameBoardCell.secretChar = jsonCell["secretChar"]
            gameBoardCell.yesBuy = jsonCell["yesBuy"]
            gameBoardCell.yesRent = jsonCell["yesRent"]
        elif gameBoardCell.cellType == "oops":
            gameBoardCell.currPlayerChoice = jsonCell["currPlayerChoice"]
            gameBoardCell.murdererChoice = jsonCell["murdererChoice"]
            gameBoardCell.playerWonOops = jsonCell["playerWonOops"]
            gameBoardCell.tied = jsonCell["tied"]
        elif gameBoardCell.cellType == "weapon":
            gameBoardCell.weapon = jsonCell["weapon"]
            gameBoardCell.weaponChar = jsonCell["weaponChar"]
            gameBoardCell.cellOccupied = jsonCell["cellOccupied"]
    
    # update roomsDict
    for roomNum in json_object["roomsDict"]:
        gameBoardRoom = app.gameBoard.roomsDict[int(roomNum)]
        jsonRoom = json_object["roomsDict"][roomNum]
        gameBoardRoom.accessible = jsonRoom["accessible"]
        gameBoardRoom.characterSecretOwner = jsonRoom["characterSecretOwner"]
        gameBoardRoom.roomSecretOwner = jsonRoom["roomSecretOwner"]
    
    # update weaponsDict
    for weaponNum in json_object["gameBoard"]["weaponsDict"]:
        app.gameBoard.weaponsDict[int(weaponNum)] = json_object["gameBoard"]["weaponsDict"][weaponNum]
    
    # updates textboxDict
    for textboxNum in json_object["textboxDict"]:
        app.gameBoard.textboxDict[int(textboxNum)].selected = json_object["textboxDict"][textboxNum]["selected"]
        app.gameBoard.textboxDict[int(textboxNum)].label = json_object["textboxDict"][textboxNum]["label"]
    
    app.gameBoard.makingAGuess = json_object["gameBoard"]["makingAGuess"]
    
    # reassign properties to player
    for playerName in [app.gameBoard.player1, app.gameBoard.player2]:
        # playerName is app object, jsonPlayer is json file object
        jsonPlayer = json_object[playerName.name]
        playerName.isCurrPlayer = jsonPlayer["isCurrPlayer"]
        playerName.cellDict = app.gameBoard.cellDict
        playerName.roomsDict = app.gameBoard.roomsDict
        playerName.weaponsDict = app.gameBoard.weaponsDict
        playerName.currCellNum = jsonPlayer["currCellNum"]
        playerName.currCell = app.gameBoard.cellDict[playerName.currCellNum]
        playerName.playerColor = jsonPlayer["playerColor"]
        playerName.lives = jsonPlayer["lives"]
        playerName.money = jsonPlayer["money"]
        playerName.buyingSecret = jsonPlayer["buyingSecret"]
        playerName.removeInnerBoard = jsonPlayer["removeInnerBoard"]
        playerName.showRooms = jsonPlayer["showRooms"]
        playerName.roomsDrawn = jsonPlayer["roomsDrawn"]
        playerName.rentingSecret = jsonPlayer["rentingSecret"]
        playerName.processingRent = jsonPlayer["processingRent"]
        playerName.rentOKRect = jsonPlayer["rentOKRect"]
        playerName.showWeaponSecret = jsonPlayer["showWeaponSecret"]
        playerName.weaponOKRect = jsonPlayer["weaponOKRect"]
        playerName.processingWeaponSecret = jsonPlayer["processingWeaponSecret"]
        playerName.shownWeaponSecret = jsonPlayer["shownWeaponSecret"]
        playerName.showOopsInstructions = jsonPlayer["showOopsInstructions"]
        playerName.oopsInstructionsRect = jsonPlayer["oopsInstructionsRect"]
        playerName.oopsInPlay = jsonPlayer["oopsInPlay"]
        playerName.shownOopsInstructions = jsonPlayer["shownOopsInstructions"]
        playerName.charSecretOwned = set(jsonPlayer["charSecretOwned"])
        playerName.roomSecretOwned = set(jsonPlayer["roomSecretOwned"])
        playerName.weaponSecretOwned = set(jsonPlayer["weaponSecretOwned"])
        selectedRoomStr = jsonPlayer["selectedRoom"]
        if selectedRoomStr != None:
            roomIdx = selectedRoomStr[0:1]
            playerName.selectedRoom = app.gameBoard.roomsDict[int(roomIdx)]
        else:
            playerName.selectedRoom = jsonPlayer["selectedRoom"]
        playerName.secretOKRect = jsonPlayer["secretOKRect"]
        playerName.textboxDict = app.gameBoard.textboxDict
        playerName.checkGuessRect = jsonPlayer["checkGuessRect"]
        playerName.wrongGuess = jsonPlayer["wrongGuess"]
        
    # create new instances of playerNOtes
    app.gameBoard.player1Notes = PlayerNotes(app.gameBoard.player1, app.gameBoard.boardLeft - 350, app.gameBoard.boardTop, 250, app.gameBoard.height, app.gameBoard.colors)
    app.gameBoard.player2Notes = PlayerNotes(app.gameBoard.player2, app.gameBoard.boardLeft - 350, app.gameBoard.boardTop, 250, app.gameBoard.height, app.gameBoard.colors)



# part of this function was taken from the stackOverflow link above
def set_default(obj):
    try:
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, str) or isinstance(obj, list) or isinstance(obj, int) or isinstance(obj, float):
            return obj
        else: 
            return str(obj)
    except:
        print("an error occurred")




def onMousePress(app, mouseX, mouseY):
    if app.instructionScreen == True:
        # checks if should start new game
        startNewGameRect = (app.width/10 * 2.5 - 150, app.height/2 + 150 - 30, 300, 60)
        startNewGameRectLeft = startNewGameRect[0]
        startNewGameRectTop = startNewGameRect[1]
        startNewGameRectW = startNewGameRect[2]
        startNewGameRectH = startNewGameRect[3]
        resumeGameRect = (app.width/10 * 7.5 - 150, app.height/2 + 150 - 30, 300, 60)
        resumeGameRectLeft = resumeGameRect[0]
        resumeGameRectTop = resumeGameRect[1]
        resumeGameRectW = resumeGameRect[2]
        resumeGameRectH = resumeGameRect[3]
        if startNewGameRectLeft <= mouseX <= startNewGameRectLeft + startNewGameRectW and startNewGameRectTop <= mouseY <= startNewGameRectTop + startNewGameRectH:
            app.instructionScreen = False
            setupGame(app)
        elif resumeGameRectLeft <= mouseX <= resumeGameRectLeft + resumeGameRectW and resumeGameRectTop <= mouseY <= resumeGameRectTop + resumeGameRectH:
            app.instructionScreen = False
            app.resumePrevGame = True
            setupGame(app)
            
    else:
        # check if need to save progress and write to json file
        checkSaveProgress(app, mouseX, mouseY)
        
        # check if need to roll dice
        if app.gameBoard.dice != None:
            app.gameBoard.dice.mouseX = mouseX
            app.gameBoard.dice.mouseY = mouseY
            # rollDiceState will be set to bool value
            app.gameBoard.rollDiceState = app.gameBoard.dice.checkBtnClick()
            if app.gameBoard.rollDiceState == True:
                app.playerSteps = random.randint(1, 6)
                app.pause = False
            
            # resets at the end
            app.gameBoard.dice.mouseX = app.gameBoard.dice.mouseY = None
        
        # change the player name based on whose turn it is --> create a variable
        changePlayerRectLeft = app.gameBoard.boardLeft + 60 + 400 - 100
        changePlayerRectTop = app.gameBoard.boardTop + app.gameBoard.height + 20
        changePlayerRectW = 200
        changePlayerRectH = 40
        # switch curr player in onStep
        if (
            changePlayerRectLeft <= mouseX <= changePlayerRectLeft + changePlayerRectW
            and changePlayerRectTop <= mouseY <= changePlayerRectTop + changePlayerRectH
        ):
            if app.gameBoard.currTurn == app.gameBoard.player1:
                app.gameBoard.currTurn = app.gameBoard.player2
                app.currPlayer = app.gameBoard.currTurn
                app.currPlayer.isCurrPlayer = True
                app.gameBoard.otherPlayer = app.gameBoard.player1
                app.gameBoard.otherPlayer.isCurrPlayer = False
            else:
                app.gameBoard.currTurn = app.gameBoard.player1
                app.currPlayer = app.gameBoard.currTurn
                app.currPlayer.isCurrPlayer = True
                app.gameBoard.otherPlayer = app.gameBoard.player2
                app.gameBoard.otherPlayer.isCurrPlayer = False

        if (
            app.currPlayer != None and app.instructionScreen == False
        ):  # this is when the game starts
            
            # check if player chose to make a guess
            checkMakeAGuess(app, mouseX, mouseY)
            
            # check if makeAGuess textbox is being clicked on --> change selected to True --> allow keyPress
            if app.gameBoard.makingAGuess == True:
                if len(app.gameBoard.textboxDict) == 3:
                    textboxList = [app.gameBoard.textboxDict[0]] + [app.gameBoard.textboxDict[1]] + [app.gameBoard.textboxDict[2]]
                    for i in range(len(textboxList)):
                        currTextbox = textboxList[i]
                        rest = (
                            textboxList[0:i] + textboxList[i + 1 :]
                        )
                        rectLeft = currTextbox.rectLeft
                        rectTop = currTextbox.rectTop
                        rectW = currTextbox.rectW
                        rectH = currTextbox.rectH
                        if (
                            rectLeft <= mouseX <= rectLeft + rectW
                            and rectTop <= mouseY <= rectTop + rectH
                        ):
                            app.gameBoard.textboxDict[i].selected = not app.gameBoard.textboxDict[i].selected

                            # resets all other textbox's selected state
                            for textboxInstance in rest:
                                app.gameBoard.textboxDict[textboxInstance.dictKey].selected = False

            
                # checks if checkGuess btn is being clicked on
                if app.currPlayer.checkGuessRect != None:
                    rectLeft = app.currPlayer.checkGuessRect[0]
                    rectTop = app.currPlayer.checkGuessRect[1]
                    rectW = app.currPlayer.checkGuessRect[2]
                    rectH = app.currPlayer.checkGuessRect[3]
                    if (
                        rectLeft <= mouseX <= rectLeft + rectW
                        and rectTop <= mouseY <= rectTop + rectH
                    ):
                        if app.currPlayer.wrongGuess==False:
                            playerGuess = Guess(app.gameBoard.textboxDict[0].label, app.gameBoard.textboxDict[1].label, app.gameBoard.textboxDict[2].label)
                            if playerGuess == app.answer:
                                # reset
                                currTextbox.selected = False
                                app.playerWon = True
                                for textbox in app.gameBoard.textboxDict:
                                    app.gameBoard.textboxDict[textbox].reset()
                                app.gameBoard.makingAGuess = False
                                app.currPlayer.checkGuessRect = None
                            else:
                                app.currPlayer.wrongGuess = True
                        elif app.currPlayer.wrongGuess==True:
                            app.currPlayer.lives -= 1
                            currTextbox.selected = False
                            app.playerWon = False
                            for textbox in app.gameBoard.textboxDict:
                                app.gameBoard.textboxDict[textbox].reset()
                            app.gameBoard.makingAGuess = False
                            app.currPlayer.checkGuessRect = None
                            app.currPlayer.wrongGuess=False

                        

            # check if clicked on yes or no buttons for buying
            if (app.currPlayer.buyingSecret == True) and (
                app.currPlayer.showRooms == False
            ):
                # check if mouseX and mouseY is within bounds of Yes or No box
                if app.currPlayer.yesBtnLeft <= mouseX <= (
                    app.currPlayer.yesBtnLeft + app.currPlayer.btnW
                ) and app.currPlayer.yesBtnTop <= mouseY <= (
                    app.currPlayer.yesBtnTop + app.currPlayer.btnH
                ):

                    app.currPlayer.showRooms = (
                        True  # change this state would trigger draw options for rooms
                    )
                    app.currPlayer.removeInnerBoard = (
                        True  # this gets rid of the yes and no btns
                    )

                    # app.gameBoard.player1.yesBuySecret() do this after the player gets the secret
                elif app.currPlayer.noBtnLeft <= mouseX <= (
                    app.currPlayer.noBtnLeft + app.currPlayer.btnW
                ) and app.currPlayer.noBtnTop <= mouseY <= (
                    app.currPlayer.noBtnTop + app.currPlayer.btnH
                ):
                    app.currPlayer.buyingSecret = False
                    app.currPlayer.removeInnerBoard = True

            # check which room the player selected
            if app.currPlayer.roomsDrawn == True:  # need to set this state back to False
                for i in range(len(app.currPlayer.roomsDict) // 2):  # 3
                    rectTop = (
                        app.currPlayer.roomBtnTop + i * (app.currPlayer.btnH + 20) + 50
                    )
                    col1Left = app.currPlayer.roomBtnCol1Left
                    col2Left = app.currPlayer.roomBtnCol2Left
                    btnW = app.currPlayer.btnW
                    btnH = app.currPlayer.btnH
                    # column 1
                    if col1Left <= mouseX <= col1Left + btnW:
                        if rectTop <= mouseY <= rectTop + btnH:
                            app.currPlayer.selectedRoom = app.currPlayer.roomsDict[i]
                            app.currPlayer.showRooms = False
                    # column 2
                    elif col2Left <= mouseX <= col2Left + btnW:
                        if rectTop <= mouseY <= rectTop + btnH:
                            app.currPlayer.selectedRoom = app.currPlayer.roomsDict[i + 3]

            # checks if the OK btn is clicked at the buy secret screen. If so, resets.
            if (
                app.currPlayer.secretOKRect != None and app.currPlayer.buyingSecret == True
            ):  # secretOKRect is the coordinates for OK btn
                rectLeft = app.currPlayer.secretOKRect[0]
                rectTop = app.currPlayer.secretOKRect[1]
                rectW = app.currPlayer.secretOKRect[2]
                rectH = app.currPlayer.secretOKRect[3]
                if (
                    rectLeft <= mouseX <= rectLeft + rectW
                    and rectTop <= mouseY <= rectTop + rectH
                ):
                    app.currPlayer.buyingSecret = False
                    app.currPlayer.secretOKRect = None

            # checks if the OK btn is clicked on the roomsNotAvailable screen
            if app.currPlayer.roomsDrawn == False:
                rectLeft = app.currPlayer.innerLeft + (app.currPlayer.innerSize / 2) - 50
                rectTop = app.currPlayer.innerTop + 150
                rectW = 100
                rectH = 40
                if (
                    rectLeft <= mouseX <= rectLeft + rectW
                    and rectTop <= mouseY <= rectTop + rectH
                ):
                    app.currPlayer.showRooms = True
                    app.currPlayer.selectedRoom = None


            ####### Renting

            # check if ok btn clicked on rentPopup screen
            if (app.currPlayer.removeInnerBoard == False) and (
                app.currPlayer.rentOKRect != None
            ):
                # check if mouseX and mouseY is within bounds of OK Btn
                rectLeft = app.currPlayer.rentOKRect[0]
                rectTop = app.currPlayer.rentOKRect[1]
                rectW = app.currPlayer.rentOKRect[2]
                rectH = app.currPlayer.rentOKRect[3]

                if (
                    rectLeft <= mouseX <= rectLeft + rectW
                    and rectTop <= mouseY <= rectTop + rectH
                ):
                    app.currPlayer.rentingSecret = True
                    app.currPlayer.removeInnerBoard = True

            # checks if the OK btn is clicked on the rent secret screen
            if (
                app.currPlayer.secretOKRect != None and app.currPlayer.rentingSecret == True
            ):  # secretOKRect is the coordinates for OK btn
                rectLeft = app.currPlayer.secretOKRect[0]
                rectTop = app.currPlayer.secretOKRect[1]
                rectW = app.currPlayer.secretOKRect[2]
                rectH = app.currPlayer.secretOKRect[3]
                if (
                    rectLeft <= mouseX <= rectLeft + rectW
                    and rectTop <= mouseY <= rectTop + rectH
                ):
                    processRentOfBothPlayers(app)
                    app.currPlayer.processingRent = True
                    app.currPlayer.secretOKRect = None

            # checks if the OK btn is clicked on the weapon screen
            if (
                app.currPlayer.showWeaponSecret == True
                and app.currPlayer.weaponOKRect != None
            ):
                rectLeft = app.currPlayer.weaponOKRect[0]
                rectTop = app.currPlayer.weaponOKRect[1]
                rectW = app.currPlayer.weaponOKRect[2]
                rectH = app.currPlayer.weaponOKRect[3]
                if (
                    rectLeft <= mouseX <= rectLeft + rectW
                    and rectTop <= mouseY <= rectTop + rectH
                ):
                    # close the weapon secret screen
                    app.currPlayer.showWeaponSecret = False
                    app.currPlayer.weaponOKRect = None
                    app.currPlayer.processingWeaponSecret = True

            # checks if the OK btn is clicked on the oopsInstructions screen
            if (
                isinstance(app.currPlayer.currCell, Oops)
                and app.currPlayer.shownOopsInstructions == False
                and app.currPlayer.oopsInstructionsRect != None
            ):
                rectLeft = app.currPlayer.oopsInstructionsRect[0]
                rectTop = app.currPlayer.oopsInstructionsRect[1]
                rectW = app.currPlayer.oopsInstructionsRect[2]
                rectH = app.currPlayer.oopsInstructionsRect[3]
                if (
                    rectLeft <= mouseX <= rectLeft + rectW
                    and rectTop <= mouseY <= rectTop + rectH
                ):
                    # close the instructions screen and open oopsPlayingScreen screen
                    app.currPlayer.shownOopsInstructions = True
                    app.currPlayer.oopsInstructionsRect = None
                    app.currPlayer.oopsInPlay = True

            # checks which rock, paper, scissors btn the player clicked on
            if (
                isinstance(app.currPlayer.currCell, Oops)
                and app.currPlayer.oopsInPlay == True
                and app.currPlayer.currCell.currPlayerChoice == None
            ):
                for i in range(len(app.currPlayer.currCell.rockPaperScissors)):
                    rectLeft = (
                        app.currPlayer.innerLeft
                        + (app.currPlayer.innerSize / 80)
                        + 90 * (i + 1)
                        - 40
                    )
                    rectTop = app.currPlayer.innerTop + 100 + 50 - 15
                    rectW = 80
                    rectH = 30
                    if (
                        rectLeft <= mouseX <= rectLeft + rectW
                        and rectTop <= mouseY <= rectTop + rectH
                    ):
                        app.currPlayer.currCell.currPlayerChoice = (
                            app.currPlayer.currCell.rockPaperScissors[i]
                        )
                        randomInt = random.randint(0, 2)  # both ends are inclusive
                        app.currPlayer.currCell.murdererChoice = (
                            app.currPlayer.currCell.rockPaperScissors[randomInt]
                        )

            # checks if ok btn clicked on oops result screen
            if (
                isinstance(app.currPlayer.currCell, Oops)
                and app.currPlayer.currCell.currPlayerChoice != None
                and app.currPlayer.oopsInstructionsRect != None
            ):
                rectLeft = app.currPlayer.oopsInstructionsRect[0]
                rectTop = app.currPlayer.oopsInstructionsRect[1]
                rectW = app.currPlayer.oopsInstructionsRect[2]
                rectH = app.currPlayer.oopsInstructionsRect[3]
                if (
                    rectLeft <= mouseX <= rectLeft + rectW
                    and rectTop <= mouseY <= rectTop + rectH
                ):
                    processOops(app)
                    app.currPlayer.oopsInstructionsRect = None
                    app.currPlayer.oopsInPlay = False
                    # need to process the payment before this line, and reset any other states


def processOops(app):
    if (
        isinstance(app.currPlayer.currCell, Oops)
        and app.currPlayer.currCell.playerWonOops == True
    ):
        app.currPlayer.currCell.currPlayerChoice = (
            app.currPlayer.currCell.murdererChoice
        ) = None
        app.currPlayer.currCell.playerWonOops = None
        app.currPlayer.editMoney(100)
    elif (
        isinstance(app.currPlayer.currCell, Oops)
        and app.currPlayer.currCell.playerWonOops == False
    ):
        app.currPlayer.currCell.currPlayerChoice = (
            app.currPlayer.currCell.murdererChoice
        ) = None
        app.currPlayer.currCell.playerWonOops = None
        app.currPlayer.editMoney(-200)


def processRentOfBothPlayers(app):
    rentMoney = int(app.currPlayer.currCell.price * 0.75)
    app.currPlayer.editMoney(-rentMoney)
    app.otherPlayer.editMoney(rentMoney)


def onKeyPress(app, key):
    if key == "j" and app.gameBoard.makingAGuess == False:
        saveToJson(app)
        
    if app.currPlayer != None:
        if key == "c" and app.gameBoard.makingAGuess == False:
            print("running camera")
            # runCamera()
            print("finished running camera")
        if key == "r" and app.gameBoard.makingAGuess == False:  
            restart(app)
        if key.isdigit():
            print(key)
            app.gameBoard.rollDiceState = True
            app.playerSteps = int(key)
            app.pause = False
            
            # app.currPlayer.updatePlayerCell(int(key))

        for i in range(len(app.gameBoard.textboxDict)):
            currTextbox = app.gameBoard.textboxDict[i]
            if currTextbox.selected == True:
                if key in string.ascii_letters:
                    currTextbox.addLabel(key)
                elif key == "space":
                    currTextbox.addLabel(" ")
                elif key == "backspace":
                    currTextbox.deleteOneChar()

def checkGameStatus(app):
    if app.currPlayer.money <= 0 or app.currPlayer.lives <= 0:
        app.playerLost = True

def onStep(app):
    if app.instructionScreen == False:
    # declares the player that is making the moves
        if app.gameBoard.currTurn == None:
            app.currPlayer = app.gameBoard.player1
            app.otherPlayer = app.gameBoard.player2
        else:
            app.currPlayer = app.gameBoard.currTurn
            app.otherPlayer = app.gameBoard.otherPlayer
        
        if app.resumePrevGame == True and app.gameBoard.boardLoaded == True:
            readJsonFile(app)
            app.resumePrevGame = False
        
        
        if app.gameBoard.rollDiceState == True and app.playerSteps != None:
            app.stepsCounter += 1
            totalSteps = app.playerSteps + len(app.gameBoard.dice.diceList)
            
            if app.stepsCounter >= totalSteps:
                app.pause = True
                app.currPlayer.updatePlayerCell(app.playerSteps)
                app.stepsCounter = 0
                app.playerSteps = None
            elif app.stepsCounter < totalSteps:
                app.gameBoard.dice.currFrame = (1 + app.gameBoard.dice.currFrame) % len(app.gameBoard.dice.diceList)

        # checks if player lost
        checkGameStatus(app)
        


runApp()