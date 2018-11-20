import cv2
from image_class import *
image = image_class(1,1)

cap = cv2.VideoCapture(0)
cap.set(3 , 1920 ) # width
cap.set(4 , 1080 ) # height
ret, frame = cap.read()
(y, x) = frame.shape[:2]

def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("X_1", "Trackbars", 0, x, nothing)
cv2.createTrackbar("X_2", "Trackbars", x,x, nothing)
cv2.createTrackbar("Y_1", "Trackbars", 0, y, nothing)
cv2.createTrackbar("Y_2", "Trackbars", y, y, nothing)

while (True):
    X_1 = cv2.getTrackbarPos("X_1", "Trackbars")
    X_2 = cv2.getTrackbarPos("X_2", "Trackbars")
    Y_1 = cv2.getTrackbarPos("Y_1", "Trackbars")
    Y_2 = cv2.getTrackbarPos("Y_2", "Trackbars")

    ret, frame = cap.read()
    cv2.imshow('frame_ori', frame)
    frame2 = frame[180:900, 720:1320]
    cv2.imshow('frame', frame2)
    bag_frame = frame2[510:720, 0:600]
    cv2.imshow('frame_crop', bag_frame)

    k = cv2.waitKey(1)
    if k & 0xFF == ord('q'):
        break
    elif k & 0xFF == ord('c'):
        command = image.sentCommand(frame)
        print(command)


cap.release()
cv2.destroyAllWindows()