# WeddingMystery

Wedding Mystery is my term project for the CMU course 15-112. Players essentially play Clue on a Monopoly board. 

The backstory is: You are invited to a wedding banquet on a lonely island,
but on the day of the wedding, the groom died at 9PM. Everyone is grieving. 
You are a detective that vows to find out who, using what weapon, at which room, killed the groom.

The player's goal is to correctly guess the character, weapon, and room, before their lives and money turn zero. 
When the player steps on the oops cell, they will need to play rock, paper, and scissors.
When the player steps on the weapon cell, they will get a free weapon clue.
When the player steps on the secret cell, they will be able to purchase a secret if the cell hasn't been owned, or pay rent to the owner of the cell.
Players can also use the save progress button to save their game to a JSON file, which
they can later open on the game instruction screen when restarting the python file.

You will need cmu_graphics and PIL to run the code. 
Although there is a file that requires OpenCV, I did not incorporate it into my project, so it is not necessary to install it.
You can run the project by running the main.py file. 
Some shortcuts include typing in digits to move the current player on the board, and press "r" to reset the gameboard.