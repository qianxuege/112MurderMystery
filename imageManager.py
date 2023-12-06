from cmu_graphics import *
from PIL import Image
# I took some of the code I wrote for load iamges in the Hack112 Project

def loadImages():
    imageDict = {
        # https://playgroundai.com/post/something-wicked-this-way-comes-the-scariest---ever-1800s-l-clnw10id70acas601l2nbfeif
        # https://playgroundai.com/post/french-style-library-haze-ultra-detailed-film-photography-clpbl9wyi0m8es601vgjyeso0
        # https://playgroundai.com/post/bright-kitchen-in-gothic-style--trending-on-artstation-sha-clpct2qhw0bygs6016ejp7j9t
        # https://playgroundai.com/post/its-hard-to-wake-up-perfect-composition-beautiful-detaile-clpbmoye212uos601n4be3q0u
        # https://playgroundai.com/post/cll8llw0o02ucs6017rnvuj36
        # https://playgroundai.com/post/5-of-people-have-the-wealth-of-the-world-however-the-remai-clo504c8n06gis601np21i1pn
        # https://playgroundai.com/post/closed-veranda-at-the-cottage-3-m-by-25-m-sheathed-with-vag-clnincq7900zis6015vq7quh6
        # https://playgroundai.com/post/in-the-enormous-ornate-house-when-walking-through-the-front--cllrzqwsa056es601n05d0ofn
        # https://playgroundai.com/post/clny1gor3004ms6010y01ppwp
        
        # https://playgroundai.com/post/stylized-sunset-skybox-unity-unreal-engine-clouds-4k-hq-clp4hq71o0558s601ilvl8ds8
        # https://playgroundai.com/post/clmef9sb0060us6018fq1ypct
        # https://playgroundai.com/post/clo91s44d0l0ss601hrdhqc18
        "lonelyMansionOnSea": "img/lonelyMansionOnSea.png",
        "sunsetSea": "img/sunsetSea.png", 
        "oceanMoon": "img/oceanMoon.png",
        "mansionFloorPlan": "img/mansionFloorPlan.png",
        "Ballroom": "img/ballroom1.png",
        "Billiard Room": "img/billiardRoom.png",
        "Kitchen": "img/kitchen.png",
        "Master Bedroom": "img/masterBedroom.png",
        "Parlor": "img/parlor.png",
        "Study": "img/study.png",
        "beachWedding": "img/beachWedding.png",
        "dice1": "img/dice1.png",
        "dice2": "img/dice2.png",
        "dice3": "img/dice3.png",
        "dice4": "img/dice4.png",
        "dice5": "img/dice5.png",
        "dice6": "img/dice6.png",
    }
    
    for imgName in imageDict:
            fileName = imageDict[imgName]
            imageDict[imgName] = CMUImage(Image.open(fileName))
    
    return imageDict