import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands #extracts the hands class from the module
hands = mpHands.Hands()  #creates an object for storing hands
mpDraw = mp.solutions.drawing_utils  #for drawing points & lines between points

while True:
    success, img = cap.read()
    cv2.flip(img, 10, img);
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Image", img)
    cv2.waitKey(1)