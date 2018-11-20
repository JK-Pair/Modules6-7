from image_class import *
import cv2

image = image_class(1,2)

cap = cv2.VideoCapture(0)
cap.set(3 , 1920 ) # width
cap.set(4 , 1080 ) # height

ret, CapImage = cap.read()
cv2.imshow("CapImage", CapImage)
cv2.waitKey(0)
while(1):

    k = cv2.waitKey(1)
    if k & 0xFF == ord('c'):
        ret, CapImage = cap.read()
        command = image.sentCommand(CapImage)

    elif k & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()