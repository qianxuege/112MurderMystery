import cv2
import mediapipe as mp
from functools import cache 

# used some code from https://www.section.io/engineering-education/creating-a-hand-tracking-module/
'''
articles I've read on OpenCV:
https://www.tutorialspoint.com/how-to-flip-an-image-in-opencv-python#:~:text=In%20OpenCV%2C%20an%20image%20can,the%20image%20across%20the%20axis.
https://www.geeksforgeeks.org/python-opencv-cv2-circle-method/
https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer/python
'''

@cache
class handTracker:
    def __init__(
        self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5
    ):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode,
            self.maxHands,
            self.modelComplex,
            self.detectionCon,
            self.trackCon,
        )
        self.mpDraw = mp.solutions.drawing_utils


    def handsFinder(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        image, handLms, self.mpHands.HAND_CONNECTIONS
                    )
        return image


    def positionFinder(self, image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            # print(Hand.landmark)
            for id, lm in enumerate(Hand.landmark):
                # The id are the 21 points. For instance, id 0 is the wrist point.
                # The shape of an image is accessed by img.shape. 
                # It returns a tuple of the number of rows, columns, and channels (if the image is color)
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h) 
                # needed to flip the x coordinates
                cx = int((1-lm.x)*w)
                
                lmlist.append([id, cx, cy])
            if draw:
                # cv2.circle(image, center_coordinates, radius, color, thickness)
                # draws the point on the wrist
                wristCoordinates = lmlist[0][1:]
                cv2.circle(image, wristCoordinates, 15, (255, 0, 255), cv2.FILLED)

        return lmlist

def runCamera():
    cap = cv2.VideoCapture(0)
    tracker = handTracker()
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    while True:
        success,image = cap.read()
        # my edits: changing the camera screen size
        success = cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        
        # my edits: flip the camera screen horizontally
        image = cv2.flip(tracker.handsFinder(image), 1)
        

        
        
         # Don't need the position finder
        lmList = tracker.positionFinder(image)
        if len(lmList) != 0:
            # print(lmList[4])
            pass
        

        cv2.imshow("Video", image)
        # code from opencv documentation
        # if cv2.waitKey(1) == ord('q'):
        if cv2.waitKey(10) & 0xFF==ord("q"):
            break
        
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    # exit()
    
if __name__ == "__main__":
    runCamera()

