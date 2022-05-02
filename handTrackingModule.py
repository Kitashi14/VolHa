import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands  # extracts the hands class from the module
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)  # creates an object for storing hands
        self.mpDraw = mp.solutions.drawing_utils  # for drawing points & lines between points


    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw :
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        # return img

    def findPosition(self, img, handNo=0,draw=True):

                lmList = []
                if self.results.multi_hand_landmarks:
                    myHand = self.results.multi_hand_landmarks[handNo]
                    for id, lm in enumerate(myHand.landmark):
                        # print(lm, id);
                        # print("next")
                        h, w, c = img.shape  # provide the size of image
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        # print(id, cx, cy)
                        lmList.append([id,cx,cy])
                        if draw:
                            cv2.circle(img, (cx, cy), 6, (255, 0, 0), cv2.FILLED)
                return lmList

# def main():
#     cap = cv2.VideoCapture(0)
#     pTime = 0
#     cTime = 0
#
#     detector = handDetector();
#
#     while True:
#         success, img = cap.read()
#         cv2.flip(img, 10, img);
#
#         detector.findHands(img);
#         lmlist = detector.findPosition(img)
#         if len(lmlist) !=0:
#             print(lmlist[4])
#         cTime = time.time()  # provides current time
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
#
#         cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
#
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
#
#
# if True:
#     main()