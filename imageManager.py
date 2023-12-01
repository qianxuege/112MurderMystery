from cmu_graphics import *
from PIL import Image
# I took some of the code I wrote for load iamges in the Hack112 Project

def loadImages():
    imageDict = {
        # https://playgroundai.com/post/a-music-theater-on-a-very-beautiful-sea-with-the-lights-of-a-cllptvzw30tjus601ucgvr4hk
        "mansion": "img/lonelyMansionOnSea.png",
    }
    
    for imgName in imageDict:
            fileName = imageDict[imgName]
            imageDict[imgName] = CMUImage(Image.open(fileName))
    
    return imageDict