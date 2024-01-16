import random

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)
startGame = False
timer = 0
stateRes = False
score = [0,0]

while True:
    imgBG = cv2.imread('Resources/BG.png')

    success, img = cap.read()

    scaledImg = cv2.resize(img, (0,0), None, 0.875, 0.875)
    scaledImg = scaledImg[:, 80:480]

    #Finding the hand here
    hands, img = detector.findHands(scaledImg)

    # As soon as it sees the hand timer starting

    if startGame:

        if stateRes is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605,435), cv2.FONT_HERSHEY_PLAIN, 6, (210,120,156),4)

            if timer > 3:
                stateRes = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    # print(fingers)

                    if np.sum(fingers) == 5:
                        playerMove = 2
                    elif np.sum(fingers) == 2:
                        playerMove = 3
                    else:
                        playerMove = 1

                    num = random.randint(1, 3)
                    imgAI = cv2.imread(f'Resources/{num}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    #condition of the player winning
                    if (playerMove == 1 and num == 3) or \
                        (playerMove == 2 and num == 1) or (playerMove == 3 and num == 2):
                        score[1] += 1

                    if (playerMove == 3 and num == 1) or \
                        (playerMove == 1 and num == 2) or (playerMove == 2 and num == 3):
                        score[0] += 1

    imgBG[234:654, 794:1194] = scaledImg

    if stateRes:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(score[0]), (414, 210), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3)
    cv2.putText(imgBG, str(score[1]), (1126, 210), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3)

    # cv2.imshow("Recorder", img)
    cv2.imshow("BG Image", imgBG)
    # cv2.imshow("scaled" , scaledImg)
    key = cv2.waitKey(1)

    if key == ord('s'):
        startGame = True
        stateRes = False
        initialTime = time.time()

    if key == ord('q'):
        break;