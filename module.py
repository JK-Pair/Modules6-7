from image_class import *
import cv2
from keepFunction import *
import time
Serial = keepFunc()

image = image_class(1,3)

cap = cv2.VideoCapture(0)
cap.set(3 , 1920 ) # width
cap.set(4 , 1080 ) # height
ret, CapImage = cap.read()

cv2.imshow("CapImage", CapImage)
cv2.waitKey(0)

command = image.sentCommand(CapImage)
print(command)
time.sleep(4)

#sendPosToPIC(self, bagPosX, bagDirX, bagPosY, bagDirY, Angle, goPosX, goDirX, goPosY, goDirY, AngGrip)
Serial.sendPosToPIC(command['positionX'][1], command['positionX'][0], command['positionY'][1], command['positionY'][0],
                    command['angleBag'],    command['goX'][1], command['goX'][0], command['goY'][1],command['goY'][0],
                    command['layerBag'] , command['angleGo'])

while(1):
    if(Serial.readDatafromPIC() == "End"):
        print(Serial.readDatafromPIC())
        ser.close()
        break
    # else:
    #     print(Serial.readDatafromPIC())


