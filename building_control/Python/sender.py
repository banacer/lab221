from time import sleep
import XBee
#from xbee import XBee

class Sender:
    def __init__(self,serial_,nodeId):
        self.xbee = XBee.XBee(serial_)
        self.nodeId = nodeId

    def sendDamperCmd(self, val):
        val = ['d', int(val)]
        self.xbee.Send(msg = val, addr = self.nodeId, options = 0x01, frameid = 0x00)

    def getTemp(self):

        self.xbee.RxMessages.clear()
        self.xbee.Send(msg = 't', addr = self.nodeId, options = 0x01, frameid = 0x00)
        sleep(2)
        response = self.xbee.Receive()
        if response == None:
            return None
        temp = float((response[7]<< 8) | response[8])/100.0
	return temp

    def getHum(self):
        self.xbee.RxMessages.clear()
        self.xbee.Send(msg = 'h', addr = self.nodeId, options = 0x01, frameid = 0x00)
        sleep(2)
        response = self.xbee.Receive()
        if response == None:
            return None
        hum = float((response[7]<< 8) | response[8])/100.0
	return hum

    def getCO2(self):
        self.xbee.RxMessages.clear()
        self.xbee.Send(msg = 'c', addr = self.nodeId, options = 0x01, frameid = 0x00)
        response = self.xbee.Receive()
        if response == None:
            return None
        co2 = float((response[7]<< 8) | response[8])
        return co2

    def set_temp(self, target_temp):
        """
        set room temp to requested temp in a rather simplistic fashion
        :param target_temp: the temperature to be set
        """
        current_temp = self.getTemp()
        damper_opened = False
        if target_temp < current_temp: #if target is smaller then we can cool the room if not we expect the someone to manually turn on the heater
            self.sendDamperCmd(100)
            damper_opened = True

        while target_temp != current_temp:
            sleep(10)
            current_temp = self.getTemp()
        if damper_opened == True:
            self.sendDamperCmd(0)
