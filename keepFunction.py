import serial
import time
BAUDRATE = 115200
PORT = 'COM9'
ser = serial.Serial()
ser.baudrate = BAUDRATE
ser.port = PORT
ser.timeout = 1
ser.dtr = 0
ser.rts = 0
ser.open()
print("connected to: " + ser.portstr)

class ConvertToHex:

    def Hex(self, hexNum):
        hexBox = []
        hex_Box = list(hex(hexNum))
        if(hexNum <= 15):
            hForward = str('0' + hex_Box[-1])
            hBackward = str('0' + hex_Box[-3])
        elif(hexNum > 15 and hexNum <= 255):
            hForward = str(hex_Box[-2] + hex_Box[-1])
            hBackward = str('00')
        elif(hexNum >= 256 and hexNum <=4095):
            hForward = str(hex_Box[-2] + hex_Box[-1])
            hBackward = str('0' + hex_Box[-3])
        elif (hexNum > 4095 and hexNum <= 5760):
            hForward = str(hex_Box[-2] + hex_Box[-1])
            hBackward = str('1' + hex_Box[-3])
        hexBox.append(hForward)
        hexBox.append(hBackward)
        return hexBox

class keepFunc:

    def convert(self, var, seq):
        cth = ConvertToHex()
        back = int(cth.Hex(int(var))[seq], 16)
        return back


    def sendPosToPIC(self, bagPosX, bagDirX, bagPosY, bagDirY, Angle, goPosX, goDirX, goPosY, goDirY, layer, AngGrip):

        k = keepFunc()
        bagPosX = bagPosX * 19.2
        bagPosY = bagPosY * 19.2
        goPosX = goPosX * 19.2
        goPosY = goPosY * 19.2

        send_data = [0xFF, 0xFF, 0x02,  0x06, k.convert(bagPosX, 0), k.convert(bagPosX, 1), int(hex(bagDirX), 16),
                     k.convert(bagPosY, 0), k.convert(bagPosY, 1), int(hex(bagDirY), 16), k.convert(Angle, 0),
                     k.convert(Angle, 1)]

        send_dataII = [k.convert(goPosX, 0), k.convert(goPosX, 1), int(hex(goDirX), 16),
                     k.convert(goPosY, 0),k.convert(goPosY, 1), int(hex(goDirY), 16), int(hex(layer), 16),
                    k.convert(AngGrip, 0), k.convert(AngGrip, 1)]

        ser.write(serial.to_bytes(send_data))
        time.sleep(2)
        ser.write(serial.to_bytes(send_dataII))

    def readDatafromPIC(self):
        line = ser.read(1000).decode('utf-8')
        return line








