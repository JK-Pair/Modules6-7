from keepFunction import *
Serial = keepFunc()

#sendPosToPIC(self, bagPosX, bagDirX, bagPosY, bagDirY, Angle, goPosX, goDirX, goPosY, goDirY, AngGrip)
Serial.sendPosToPIC(100, 1, 100, 1, 0, 100, 1, 100, 1, 00)
# print(Serial.readDatafromPIC())
ser.close()

