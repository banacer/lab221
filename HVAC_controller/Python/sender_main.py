import sender
from time import sleep

sender.getTemp('/dev/ttyUSB0', 0x2211)