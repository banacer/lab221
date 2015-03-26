import send_Xbee
from time import sleep


print('\ncntrlDamper(address in HEX, cntrlVal in int)')
xbee = send_Xbee.send_Xbee(serialport = "COM12")
sleep(1)


def cntrlDamper(nodeID, cntrlVal):
    """
    :param nodeID: 16 bit address of the device in HEX; example 0x1234
    :param cnrtlVal: must be 0 < cntrlVal < 100
    """
    # def __init__(self, nodeID, cntrlVal):
    #     self.nodeID = int(nodeID)
    #     self.cnrlVal = int(cntrlVal)
    while True:
        if cntrlVal < 0 or cntrlVal > 100:
            print 'Error cntrlVal must be 0 < cntrlVal < 100'
        else:
            val = ['d', cntrlVal]
            xbee.sendInt(data = val, addr = nodeID, options = 0x01, frameid = 0x00)
        return






