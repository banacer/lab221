import sys
import send_Xbee
from time import sleep


xbee = send_Xbee.send_Xbee(serialport = "COM12")
sleep(1)
while True:
    choice = raw_input('\n get?\n temp\n humid\n co2\n damper \n >> ')
    if choice == 'temp':
        xbee.rxI()
        try:
             nodeID = int(input('enter nodeID in HEX: '))
        except NameError:
            sys.exit('Not an Int or Hex value \nSystem Exit')
        xbee.sendInt(data = 't', addr = nodeID, options = 0x01,frameid = 0x00)
        xbee.rxI()
        sleep(5)
        xbee.rx()
    elif choice == 'humid':
        xbee.rxI()
        try:
             nodeID = int(input('enter nodeID in HEX: '))
        except NameError:
            sys.exit('Not an Int or Hex value \nSystem Exit')

        xbee.sendInt(data = 'h', addr = nodeID, options = 0x01, frameid = 0x00)
        xbee.rxI()
        sleep(5)
        xbee.rx()
    elif choice == 'co2':
        try:
             nodeID = int(input('enter nodeID in HEX: '))
        except NameError:
            sys.exit('Not an Int or Hex value \nSystem Exit')
        xbee.sendInt(data = 'c', addr = nodeID, options = 0x01, frameid = 0x00)
        xbee.rxI()
        sleep(5)
    elif  choice == 'damper':
        xbee.rxI()
        try:
             nodeID = int(input('enter nodeID in HEX: '))
        except NameError:
            sys.exit('Not an Int or Hex value \nSystem Exit')
        cntrl_val = int(input('enter the damper control value: '))
        val = ['d', cntrl_val]
        # print val
        xbee.sendInt(data = val, addr = nodeID, options = 0x01, frameid = 0x00)
        xbee.rxI()
        sleep(5)
        xbee.rx()
    elif choice == 'exit':
        sys.exit('System Exit!!')
    else :
        print 'wrong choice'




