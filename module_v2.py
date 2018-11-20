import cv2
from image_class import *
from keepFunction import *
import time
Serial = keepFunc()

# -----------------------------------------> check Camera

cap = cv2.VideoCapture(0)
cap.set(3 , 1920 ) # width
cap.set(4 , 1080 ) # height
ret, CapImage = cap.read()
cv2.imshow("CapImage", CapImage)
cv2.waitKey(0)
CropImage = CapImage[180:900, 720:1320]
cv2.imshow("CropImage", CropImage)
cv2.waitKey(0)
bag_frame = CropImage[510:720, 0:600]
cv2.imshow("bag_frame", bag_frame)
cv2.waitKey(0)
cv2.destroyWindow("CapImage")
cv2.destroyWindow("CropImage")
cv2.destroyWindow("bag_frame")

# -----------------------------------------> start
state_on = True
state_type = True
state_run = False
Run = False
RunFinish = True

Type = 1
pattern = 1
state_typeCheck = 0
state_runCheck = 0
checkType = " "

def click_type(event,x,y,flags,param):
    global Type, pattern,state_run,state_on,state_type,state_typeCheck


    if event == cv2.EVENT_LBUTTONUP:
        # print('X =' + str(x))
        # print('Y =' + str(y))
        if y >= 165 and y <= 260:
            if x >= 585 and x <= 760:
                Type = 1
            elif x >= 780 and x <= 970:
                Type = 2
            elif x >= 1015 and x <= 1190:
                Type = 3

        elif y >= 310 and y <= 405:
            if x >= 585 and x <= 760:
                pattern = 1
            elif x >= 780 and x <= 970:
                pattern = 2
            elif x >= 1015 and x <= 1190:
                pattern = 3

        elif y >= 445 and y <= 555 and x >= 485 and x <= 795:
            # print("ok")
            state_typeCheck = 1
            state_on = True
            state_type = False
            state_run = True

        elif y >= 525 and y <= 615 and x >= 1170 and x <= 1250:
            # print("trun off")
            state_on = False
            state_type = False
            state_run = False

def click_SWrun(event,x,y,flags,param):
    global Run,state_run,state_on,state_type,state_runCheck,Type, pattern,RunFinish

    if event == cv2.EVENT_LBUTTONUP and RunFinish:
        # print('X =' + str(x))
        # print('Y =' + str(y))

        if y >=  80 and y <= 480 and x >= 595 and x <= 995 :
            # print("run1")
            Run = True
            RunFinish = False


        elif y >= 495 and y <= 605 and x >= 65 and x <= 370:
            # print("reset1")
            state_runCheck = 1
            Type = 1
            pattern = 1
            state_on = True
            state_type = True
            state_run = False

        elif y >= 525 and y <= 615 and x >= 1170 and x <= 1250:
            # print("trun off")
            state_on = False
            state_type = False
            state_run = False



type_patternPic = cv2.imread('module_pic/type&pattern.png')
SW_runPic = cv2.imread('module_pic/SW_run.png')

cv2.namedWindow('type_pattern')
cv2.moveWindow('type_pattern', 0, 0)
cv2.setMouseCallback('type_pattern',click_type)

while(state_on):

    while(state_type):
        type_pattern = type_patternPic.copy()
        cv2.putText(type_pattern, str(Type),(385, 105), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 5)
        cv2.putText(type_pattern, str(pattern), (1050, 105), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 5)
        cv2.imshow('type_pattern', type_pattern)
        cv2.waitKey(1)

    if state_typeCheck == 1:
        # print("ok2")
        cv2.destroyWindow('type_pattern')
        state_typeCheck = 0
        image = image_class(Type, pattern)

        cv2.namedWindow('SW_run')
        cv2.moveWindow('SW_run', 0, 0)
        cv2.setMouseCallback('SW_run', click_SWrun)


    while(state_run):
        SW_run = SW_runPic.copy()
        cv2.putText(SW_run, checkType, (105, 115), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 5)
        cv2.imshow('SW_run', SW_run)
        cv2.waitKey(1)

        if Run :
            # print('type = ' + str(image.Type))
            # print('pattern = '+str(image.pattern))
            # print("run2")
            SW_run = SW_runPic.copy()
            cv2.putText(SW_run, "LOADING...", (105, 115), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 5)
            cv2.imshow('SW_run', SW_run)
            cv2.waitKey(1)
            ret, CapImage = cap.read()
            command = image.sentCommand(CapImage)
            print(command)
            time.sleep(4)
            checkType = 'Type : '+str(command['typeBag'])
            Serial.sendPosToPIC(command['positionX'][1], command['positionX'][0], command['positionY'][1], command['positionY'][0],
                    command['angleBag'],    command['goX'][1], command['goX'][0], command['goY'][1],command['goY'][0],
                    command['layerBag'] , command['angleGo'])
            Run = False

        if (Serial.readDatafromPIC() == "End"):
            RunFinish = True
            checkType = " "



    if state_runCheck == 1:
        print("reset2")
        cv2.destroyWindow('SW_run')
        state_runCheck = 0
        cv2.namedWindow('type_pattern')
        cv2.moveWindow('type_pattern', 0, 0)
        cv2.setMouseCallback('type_pattern', click_type)


print("out")
cv2.destroyAllWindows()
ser.close()