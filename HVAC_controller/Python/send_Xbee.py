    # -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 10:05:47 2014

@author: krish
"""
import serial
from time import sleep
from collections import deque


class send_Xbee():
    '''XBee class for sending and receiving the data '''
    RxBuff = bytearray()
    RxMessages = deque()

    def __init__(self, serialport, baudrate = 9600):
        """set serial port parameters, with port "serialport" name and "baudrate"
           usually COM* for windows and /dev/ttyUSB* for linux
        """
        self.serialport = serialport
        self.set_serial = serial.Serial(port = serialport, baudrate = baudrate)
        print self.serialport
        if (self.set_serial.isOpen() == True):
            self.set_serial.close()
        else:
            self.set_serial.open()
        self.set_serial.open()

    def Strng(self, data, addr, options, frameid):
        """
        method string for sending string data to xbee, 'data' = string

        """
        self.data = data.encode('hex')
        self.addr = addr
        self.options = options
        self.frameid = frameid
        return self.send(data, addr, options, frameid)

    def send(self, data, addr, options, frameid ):
        if not data:
            return 0
        #print data
        #print 'addr in send is ' , addr

        make_frame = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
                      len(data) + 5,
                      frameid,
                      (addr & 0xFF00) >> 8,
                      addr & 0x00FF,
                      options
                      )
        frame = bytearray.fromhex(make_frame)
        frame.extend(data)
        checksum = 0xFF - (sum(frame[3:]) & 0xFF)
        frame.append(checksum)
        print ("Tx: " + self.format(frame))
        return self.set_serial.write(frame)


    def sendI(self, data, addr, options, frameid ):
        if not data:
            return 0
        #print data
        #print 'addr in send is ' , addr

        make_frame = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
                      len(data) + 5,
                      frameid,
                      (addr & 0xFF00) >> 8,
                      addr & 0x00FF,
                      options
                      )
        frame = bytearray.fromhex(make_frame)
        frame.extend(data)
        checksum = 0xFF - (sum(frame[3:]) & 0xFF)
        frame.append(checksum)
        return self.set_serial.write(frame)


    def format(self,data)   :
        return " ".join("{:02x}".format(b) for b in data)




    def sendInt(self, data, addr, options, frameid):
        self.set_serial.flush()
        self.data = data
        self.sendI(data, addr, options, frameid)
        sleep(3)
        self.send(data, addr, options, frameid)


    def close(self, arg):
        self.arg = arg
        print arg
        return self.set_serial.close()

    def rxI(self):
        readNumChar = self.set_serial.inWaiting()
        #print readNumChar
        #self.passNumChar = readNumChar
        rxData = bytearray(self.set_serial.read(readNumChar))
        lenrxData = len(rxData)
        #print 'rxData = ', rxData
        
        if (lenrxData > 0):
            self.checkValidI(rxData, lenrxData)
            return rxData

    def checkValidI (self, rxData, lenrxData):
        self.rxData = rxData
        self.lenChar = lenrxData
        lenData = rxData[2]
        if(rxData[0] == 126):      #check for 7E in the starting of Rx data
            validData = rxData[8:lenData + 3]




    def rx(self):
        #self.rxI()
        readNumChar = self.set_serial.inWaiting()
        # print(readNumChar)
        rxData = bytearray(self.set_serial.read(readNumChar))
        lenrxData = len(rxData)
        #print 'rxData = ', rxData

        if (lenrxData > 0):
            self.checkValid(rxData, lenrxData)
    
    def checkValid (self, rxData, lenrxData):
        self.rxData = rxData
        self.lenChar = lenrxData
        lenData = rxData[2]
        # print 'lenData = ', lenData
        if(rxData[0] == 126):      #check for 7E in the starting of Rx data
            validData = rxData[8:lenData + 3]
        
        print 'Rx Message Data: ' + self.format(validData)
        print 'Rx Message: ' + self.format(rxData), '\n  '
    
    def Receive(self):
        remaining = self.set_serial.inWaiting()
        while remaining:
            chunk = self.set_serial.read(remaining)
            remaining -= len(chunk)
            self.RxBuff.extend(chunk)

        msgs = self.RxBuff.split(bytes(b'\x7E'))
        for msg in msgs[:-1]:
            self.Validate(msg)

        self.RxBuff = (bytearray() if self.Validate(msgs[-1]) else msgs[-1])

        if self.RxMessages:
            return self.RxMessages.popleft()
        else:
            return None

    def Validate(self, msg):
        if (len(msg) - msg.count(bytes(b'0x7D'))) < 9:
            return False
        frame = self.Unescape(msg)
        LSB = frame[1]
        if LSB > (len(frame[2:]) - 1):
            return False
        if (sum(frame[2:3+LSB]) & 0xFF) != 0xFF:
            return False
        print("Rx: " + self.format(bytearray(b'\x7E') + msg))
        self.RxMessages.append(frame)
        return True


