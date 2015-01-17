command for running java program in Linux environnment 

cd xbee_api/
java -cp target/xbeeapi-1.0.jar:/home/pi/xbee-api/lib/log4j.jar:/home/pi/xbee-api/lib/RXTXcomm.jar com.rapplogic.xbee.app.XbeeGateway /dev/ttyUSB0