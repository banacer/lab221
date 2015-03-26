from time import sleep
import XBee

def sendDamperCmd(serial_, nodeId, val):
    xbee = XBee.XBee(serial_)
    val = ['d', int(val)]
    xbee.Send(msg = val, addr = nodeId, options = 0x01, frameid = 0x00)
    xbee.Receive()

def getTemp(serial_, nodeId):
    xbee = XBee.XBee(serial_)
    xbee.Send(msg = 't', addr = nodeId, options = 0x01, frameid = 0x00)
    sleep(1)
    Msg = xbee.Receive()
    #content = Msg[7:-1]
    print("Msg: " + xbee.format(Msg))
    
def getHum(serial_, nodeId):
    xbee = XBee.XBee(serial_)
    xbee.Send(msg = 'h', addr = nodeId, options = 0x01, frameid = 0x00)
    response = xbee.Receive()
    print response
    
    print response
    
def getCO2(serial_, nodeId):
    xbee = XBee.XBee(serial_)
    xbee.Send(msg = 'c', addr = nodeId, options = 0x01, frameid = 0x00)
    response = xbee.Receive()
    print response
    
    