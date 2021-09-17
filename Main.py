from cvzone.HandTrackingModule import HandDetector
import cv2
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
finalText = ""


# def drawALL(img, buttonList):

#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
#         # Here we are make a keyboard and ut some text
#         cv2.rectangle(img, button.pos, (x+w, y+h), (255, 0, 255), cv2.FILLED)
#         cv2.putText(img, button.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

#     return img

keyboard = Controller()
def drawALL(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        # cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button))
        cv2.rectangle(imgNew, button.pos, (x+button.size[0], y+button.size[1]), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x+40, y+60), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1-alpha, 0)[mask]
    return out


class Button():
    def __init__(self, pos, text, size = [85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

        


buttonList = []
keys = [["Q", "W","E", "R", "T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]


for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    # Get image frame
    success, img = cap.read()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)

    img = drawALL(img, buttonList)
    
    if hands:
        hand1 = hands[0]
        lmList = hand1["lmList"]
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

       

            if (x< lmList[8][0]< x + w and y < lmList[8][1] < y + h) and (x< lmList[12][0]< x + w and y < lmList[12][1] < y + h):
                keyboard.press(button.text)
                cv2.rectangle(img, button.pos, (x + w, y + h), (0,0,255), cv2.FILLED)
                cv2.putText(img, button.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                finalText += button.text
                sleep(0.15)
       
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (65, 425), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)           
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)