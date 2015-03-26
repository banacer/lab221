import sys
import send_Xbee
from time import sleep

xbee = send_Xbee.send_Xbee(serialport = "COM10")
sleep(1)
while True:
	val = input("value: ")
	if val == -1:
		sys.exit()
	else:
		xbee.sendInt(data = str(val),addr = 0x2191, options = 0x01,frameid = 0x00)
	#xbee.rx()
xbee.close()

    
