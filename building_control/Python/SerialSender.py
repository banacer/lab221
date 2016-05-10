'''
A Serial communication module with Arduino to read
temperature, humidity, CO2 and control the damper
'''
from time import sleep
import serial
from threading import Lock

class SerialSender(object):
    '''
    Class to get temperature, humidity, CO2 and control
    the damper connected to an arduino
    '''
    def __init__(self, serial_):
        self.ser = serial.Serial(serial_, 9600, timeout=1)
        self.__mutex = Lock()

    def send_damper_command(self, val):
        """
        send command to damper to control
        :param val: the val of the damper between 0 and 100
        """
        self.__mutex.acquire() #acquiring mutex
        print 'mutex acquired'
        self.ser.write(['d',chr(val)])
        #self.ser.flushOutput()
        ack = self.ser.readline().rstrip()
        if ack == 'A':
            pass
        else:
            raise Exception('Damper command failed')
        self.__mutex.release() #releasing mutex
        print 'mutex released'

    def get_temp(self):
        """
        get temperature
        :return: temperature in F
        """
        self.__mutex.acquire()  # acquiring mutex
        print 'mutex acquired'
        self.ser.write('t')
        #self.ser.flushOutput()
        val = self.ser.readline()
        val = val.rstrip()
        try:
            val = float(val)
        except ValueError,e:
            val = self.get_temp()
        print 'val is ', val
        return val
        self.__mutex.release()
        print 'mutex released'

    def get_humidity(self):
        """
        get humidity
        :return: humidity in %
        """
        try:
            self.__mutex.acquire()
            self.ser.write('h')
            #self.ser.flushOutput()
            val = self.ser.readline().rstrip()
            return float(val)
        except Exception, e:
            print e
        finally:
            self.__mutex.release()
    def get_co2(self):
        """
        get CO2
        :return: CO2 in p
        """
        try:
            self.__mutex.acquire()
            self.ser.write('c')
            #self.ser.flushOutput()
            val = self.ser.readline().rstrip()
            return float(val)
        except Exception, e:
            print e
        finally:
            self.__mutex.release()

    def set_temp(self, target_temp, current_temp):
        """
        set room temp to requested temp in a rather simplistic fashion
        :param target_temp: the temperature to be set
        """
        #current_temp = self.get_temp()
        damper_opened = False
        if target_temp < current_temp:  # if target is smaller then we can cool the
        # room if not we expect the someone to manually turn on the heater
            self.send_damper_command(100)
            damper_opened = True

        while target_temp != current_temp:
            sleep(10)
            current_temp = self.get_temp()
        if damper_opened is True:
            self.send_damper_command(0)