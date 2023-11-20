from cmu_graphics import *
from handDetection import runCamera

def onAppStart(app):
    app.paused = True

def redrawAll(app):
    drawLabel('112 Murder Mystery', 200, 200)
    drawLabel(app.paused, 200, 250)
    # runCamera()

def onKeyPress(app, key):
    if key == 's':
        print('running camera')
        runCamera()
        print('finished running camera')

runApp()