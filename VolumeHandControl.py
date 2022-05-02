import cv2
import time
import numpy as np
import math
import handTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam  = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

cTime , pTime = 0,0

detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
minVol = volRange[0]
maxVol = volRange[1]

vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    cv2.flip(img, 10, img)

    detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:
        # print(lmList[4],lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx = int((x1+x2)/2)
        cy = int((y1+y2)/2)

        cv2.circle(img, (x1, y1), 6, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 6, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy),6, (255,0,0), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        # hand range 50-300
        # vol range -65 - 0

        vol = np.interp(length,[5,120],[minVol,maxVol])
        volBar = np.interp(length, [5, 120],[400,150])
        volPer = np.interp(length, [5,120],[0,100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<15:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50,150), (85,400),(255,0,255),3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 255), cv2.FILLED)
    cv2.putText(img, f'{(int(volPer))}%', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)



    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime= cTime

    cv2.putText(img, str(int(fps)), (40,70), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),5)

    cv2.imshow("Img",img)
    cv2.waitKey(1)