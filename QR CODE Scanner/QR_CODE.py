import cv2 as cv
from pyzbar.pyzbar import decode
import numpy as np

wcam, hcam = 640, 480
blank = np.zeros((hcam,wcam,3),dtype='uint8')

cap = cv.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
imgback = cv.imread('qrcode.png')
count = 0
while count < 1:
    success, img = cap.read()
    x = decode(img)
    print(x)

    if x:
        for d in x:
            img = cv.rectangle(blank, (d.rect.left, d.rect.top),
                               (d.rect.left + d.rect.width, d.rect.top + d.rect.height), (255, 0, 0), 3)
            img = cv.polylines(blank, [np.array(d.polygon)], True, (0, 255, 0), 2)
            img = cv.putText(blank, d.data.decode(), (d.rect.left, d.rect.height),
                             cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv.LINE_AA)
            count += 1
            # if cv.waitKey(0) & 0xFF == ord('s'):
            #     cv.imwrite('QRCode_' + str(count) + '.png', img)  # Save the image
            #     break

        cv.imshow('IMAGE', imgback)
        imgback[120:120 + 480, 72:72 + 640] = blank
        cv.imwrite('save2.png', imgback)


        cv.waitKey(1000)


