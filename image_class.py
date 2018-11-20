from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2

class image_class() :

    def __init__(self,type,pattern):
        self.BagInBox = 0
        self.CameraCoToWorldCo_X = 13.5   #14 #13.5
        self.CameraCoToWorldCo_Y = -1 #-0.2  #-1.5
        self.CenterGripper = 350
        self.PositionBag_X = None
        self.PositionBag_Y = None
        self.Type = type
        self.pattern = pattern
        self.layerBagInBox = 0


    # -----------------------------------------------------------------> sub function in class
    def centroid(self,vertexes):
        _x_list = [vertex[0] for vertex in vertexes]
        _y_list = [vertex[1] for vertex in vertexes]
        _len = len(vertexes)
        x = sum(_x_list) / _len
        y = sum(_y_list) / _len
        return (x, y)

    def midpoint(self,ptA, ptB):
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

    def distance(self,ptA, ptB):
        x = ((ptA[0] - ptB[0]) ** 2) + ((ptA[1] - ptB[1]) ** 2)
        return x ** 0.5

    def adjust_gamma(self,image, gamma=1.0):

        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

        return cv2.LUT(image, table)

    def addFilter(self,image):

        gamma_frame = self.adjust_gamma(image, 0.5)
        gaussian = cv2.GaussianBlur(gamma_frame, (9, 9), 10.0)
        bilateral = cv2.bilateralFilter(gamma_frame, 9, 75, 75)
        cv2.addWeighted(gamma_frame, 1.5, gaussian, -0.5, 0, gamma_frame)
        cv2.addWeighted(gamma_frame, 1.5, bilateral, -0.5, 10, gamma_frame)

        return gamma_frame

    def edge_detection(self,image):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(gray, 65, 175)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        if cnts != []:
            (cnts, _) = contours.sort_contours(cnts)

        return cnts

    def find_typeBag(self,bag_frame):

        hsv = cv2.cvtColor(bag_frame, cv2.COLOR_BGR2HSV)
        lower = np.array([150, 66, 160])
        upper = np.array([179, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)

        # cv2.imshow("bag_frame", bag_frame)
        # out = bag_frame.copy()
        # output = cv2.bitwise_and(out, out, mask=mask)
        # cv2.imshow("output", output)
        # cv2.waitKey(0)
        # print("mask ="+str(np.sum(mask)))

        if np.sum(mask) > 10000:
            out = bag_frame.copy()
            output = cv2.bitwise_and(out, out, mask=mask)
            cv2.imshow("output", output)
            print("mask =" + str(np.sum(mask)))
            cv2.waitKey(0)
            cv2.destroyWindow('output')

            bagType = 1

        else:

            lower = np.array([0, 37, 160])
            upper = np.array([56, 102, 255])
            mask = cv2.inRange(hsv, lower, upper)

            out = bag_frame.copy()
            output = cv2.bitwise_and(out, out, mask=mask)
            cv2.imshow("output", output)
            print("mask =" + str(np.sum(mask)))
            cv2.waitKey(0)
            cv2.destroyWindow('output')


            if np.sum(mask) < 2000000:
                bagType = 2

            elif np.sum(mask) >= 2000000:
                bagType = 3

        return bagType

    def ChangeDegreeToSentValue(self,rotate):
        degree = rotate[0]
        OneDegreeEqualSentValue = 420/180
        Gripper90Degree = OneDegreeEqualSentValue * 90

        if degree == -90 or degree == 90:
            sentZeta = self.CenterGripper

        elif degree == 0:
            if rotate[1] == 0:
                sentZeta = self.CenterGripper - Gripper90Degree
            elif rotate[1] == 1:
                sentZeta = self.CenterGripper + Gripper90Degree

        elif degree > -90 and degree < 0 :
            theta = OneDegreeEqualSentValue * np.absolute(degree)
            sentZeta = (self.CenterGripper - Gripper90Degree)+ theta

        elif degree < 90 and degree > 0 :
            theta = OneDegreeEqualSentValue * degree
            sentZeta = (self.CenterGripper + Gripper90Degree) - theta


        return int(sentZeta)

    # -----------------------------------------------------------------> main function in class

    def calculate_bag(self,image):
        OnePixelsEqualCm = 10 / 170
        image = self.addFilter(image)
        bag_frame = image[510:720, 0:600]
        # cv2.imshow("bag_frame", bag_frame)
        # cv2.waitKey(0)

        cnts = self.edge_detection(bag_frame)

        for c in cnts:

            if cv2.contourArea(c) < 1500:
                continue

            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)

            cen1 = self.centroid(box)

            (tl, tr, br, bl) = box
            (Tx, Ty) = self.midpoint(tl, tr)
            (Bx, By) = self.midpoint(bl, br)
            (Lx, Ly) = self.midpoint(tl, bl)
            (Rx, Ry) = self.midpoint(tr, br)

            disY = self.distance((Tx, Ty), (Bx, By))
            disX = self.distance((Lx, Ly), (Rx, Ry))

            if disX <= disY:
                Zeta = (np.arctan2(Tx - cen1[0], Ty - cen1[1]) * 180 / np.pi) - 180
                if Zeta < -90:
                    Zeta += 360

            elif disX > disY:
                Zeta = (np.arctan2(cen1[1] - Ty, Tx - cen1[0]) * 180 / np.pi) - 180
                if Zeta < -90:
                    Zeta += 180
                X = disY
                disY = disX
                disX = X


            position_X_pix = cen1[0]
            position_Y_pix = cen1[1] + 510

            positionWorld_Y_Cm = (position_X_pix * OnePixelsEqualCm) - self.CameraCoToWorldCo_Y
            positionWorld_X_Cm = (position_Y_pix * OnePixelsEqualCm) - self.CameraCoToWorldCo_X

            positionWorld_Y_mm = positionWorld_Y_Cm * 10
            positionWorld_X_mm = positionWorld_X_Cm * 10

            self.PositionBag_X = int(positionWorld_X_mm)
            self.PositionBag_Y = int(positionWorld_Y_mm)

            A = [int(positionWorld_X_mm), int(positionWorld_Y_mm)]
            B = self.ChangeDegreeToSentValue([Zeta,0])

        return [A[0],A[1],B]

    def find_GoPosition(self,image, type, pattern):
        bag_frame = image[510:720, 0:600]
        bag_frame = self.addFilter(bag_frame)
        bagType = self.find_typeBag(bag_frame)
        print(bagType)

        if bagType != type:
            print("TwT")
            Go_X = 53
            Go_Y = 300
            angle = self.ChangeDegreeToSentValue([0, 0])
            layer = 4


        else:
            print(";P")
            if pattern == 1:
                print("pattern 1")
                if self.BagInBox % 2 == 0:
                    Go_X = 73
                    Go_Y = 90
                    angle = self.ChangeDegreeToSentValue([0, 0])
                    layer = self.layerBagInBox
                elif self.BagInBox % 2 == 1:
                    Go_X = 73
                    Go_Y = 170
                    angle = self.ChangeDegreeToSentValue([0, 1])
                    layer = self.layerBagInBox
                    self.layerBagInBox += 1
                self.BagInBox += 1

            elif pattern == 2:
                print("pattern 2")
                if self.BagInBox % 4 == 0:
                    Go_X = 88
                    Go_Y = 90
                    angle = self.ChangeDegreeToSentValue([0, 0])
                    layer = self.layerBagInBox
                elif self.BagInBox % 4 == 1:
                    Go_X = 13
                    Go_Y = 95
                    angle = self.ChangeDegreeToSentValue([90, 0])
                    layer = self.layerBagInBox
                elif self.BagInBox % 4 == 2:
                    Go_X = 15
                    Go_Y = 170
                    angle = self.ChangeDegreeToSentValue([0, 1])
                    layer = self.layerBagInBox
                elif self.BagInBox % 4 == 3:  #test
                    Go_X = 155
                    Go_Y = 150
                    angle = self.ChangeDegreeToSentValue([90, 0])
                    layer = 4
                    self.layerBagInBox += 1
                self.BagInBox += 1

            elif pattern == 3:
                print("pattern 3")
                if self.BagInBox % 6 == 0:
                    Go_X = 15
                    Go_Y = 90
                    angle = self.ChangeDegreeToSentValue([0, 0])
                    layer = self.layerBagInBox
                    self.layerBagInBox += 1
                elif self.BagInBox % 6 == 1:
                    Go_X = 15
                    Go_Y = 170
                    angle = self.ChangeDegreeToSentValue([0, 1])
                    layer = self.layerBagInBox
                elif self.BagInBox % 6 == 2:
                    Go_X = 39 #53
                    Go_Y = 90
                    angle = self.ChangeDegreeToSentValue([0, 0])
                    layer = self.layerBagInBox
                    self.layerBagInBox += 1
                elif self.BagInBox % 6 == 3:
                    Go_X = 39 #53
                    Go_Y = 170
                    angle = self.ChangeDegreeToSentValue([0, 1])
                    layer = self.layerBagInBox
                elif self.BagInBox % 6 == 4:
                    Go_X = 88
                    Go_Y = 90
                    angle = self.ChangeDegreeToSentValue([0, 0])
                    layer = self.layerBagInBox
                    self.layerBagInBox += 1
                elif self.BagInBox % 6 == 5:
                    Go_X = 88
                    Go_Y = 170
                    angle = self.ChangeDegreeToSentValue([0, 1])
                    layer = self.layerBagInBox
                self.BagInBox += 1

        return [Go_X, Go_Y, angle,layer,bagType]


    def sentCommand(self,image):


        CapImage = image[180:900, 720:1320]
        # cv2.imshow("CapImage2", CapImage)
        # cv2.waitKey(0)
        dataBag = self.calculate_bag(CapImage)
        Go = self.find_GoPosition(CapImage,self.Type,self.pattern)
        goX = Go[0] - self.PositionBag_X
        goY = Go[1] - self.PositionBag_Y

        if goX < 0 :
            X = [0, np.absolute(goX)]
        else :
            X = [1, goX]

        if goY < 0 :
            Y = [0, np.absolute(goY)]
        else :
            Y = [1, goY]

        command = {'positionX':[1,dataBag[0]] , 'positionY': [1,dataBag[1]], 'angleBag': dataBag[2],
                   'goX': X, 'goY': Y, 'angleGo': Go[2] ,'layerBag': Go[3],'typeBag': Go[4]}

        return command