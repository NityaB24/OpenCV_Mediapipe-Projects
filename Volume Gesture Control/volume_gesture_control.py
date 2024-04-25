import math
import numpy as np
import cv2 as cv
import mediapipe as mp
import time
import handtrackingmodule as ht
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

##################
wcam, hcam = 640, 480
##################

capture = cv.VideoCapture(0)
capture.set(3,wcam)
capture.set(4, hcam)
pt = 0
ct = 0
detector = ht.hand()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()


minV = volRange[0]
maxV = volRange[1]
volbar = 400
vol = 0
volper = 0
while True:
    success, img = capture.read()
    img = detector.findhands(img)
    lmlist = detector.findposition(img,draw=False)
    if len(lmlist) != 0:
        # print(lmlist[4],lmlist[8])

        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2) // 2, (y1+y2) // 2
        cv.circle(img,(x1,y1),10,(255,0,255),cv.FILLED)
        cv.circle(img,(x2,y2),10,(255,0,255),cv.FILLED)
        cv.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv.circle(img,(cx,cy),10,(255,0,255),cv.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        # print(length)

        # HAnd range 40 - 350
        # Volume range -65 to 0

        vol = np.interp(length,[50,200],[minV,maxV])
        volbar = np.interp(length,[50,200],[400,150])
        volper = np.interp(length,[50,200],[0,100])


        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length < 40:
            cv.circle(img, (cx, cy), 10, (0,255, 0), cv.FILLED)
    # cv.rectangle(img,(50, 150), (85, 400), (255,255,255),2)
    # cv.rectangle(img,(50, int(volbar)), (85, 400), (255,255,255),cv.FILLED)
    # cv.putText(img, f'{int(volper)}%', (40, 450), cv.FONT_ITALIC, 1, (255, 255, 255), 2)


    ct = time.time()
    fps = 1 / (ct - pt)
    pt = ct
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_ITALIC, 1, (0, 255, 0), 2)

    cv.imshow("Image", img)
    cv.waitKey(1)