#include <XBee.h>
#include <TF>
#include "kSeries.h"
#include <dht.h>

dht DHT;
kSeries K_30(12,13);
#define DHT22_PIN 5

uint8_t payload[5] = {0,0,0,0,0};
uint8_t* data;
int dataLen;
int remoteID; 
short temp, humid;
XBee xbee = XBee();


Tx16Request tx = Tx16Request(remoteID, payload, sizeof(payload));
Rx16Response rx = Rx16Response();


short getTemperature()
{
    int chk = DHT.read22(DHT22_PIN);
    short data = (short) (DHT.temperature*100);
    return data;

}

short getHumidity()
{
    int chk = DHT.read22(DHT22_PIN);
    short data = (short) (DHT.humidity*100);
    return data;
}

/*int getCO2()
{

}*/

void setup()
{
	Serial.begin(9600);
	xbee.setSerial(Serial);
}

void loop()
{
	delay(1500);
	xbee.readPacket();
	if(xbee.getResponse().isAvailable())
	{
		if(xbee.getResponse().getApiId() == RX_16_RESPONSE)
		{
			xbee.getResponse().getRx16Response(rx);
			data = rx.getData();
			remoteID = rx.getRemoteAddress16();
                        //remoteID = getHex(remoteID);
			dataLen = rx.getDataLength();
			for(int i  = 0; i < dataLen; i++)
			{
			    Serial.print("Receive Data = ");
		            Serial.print(data[i]);
		            Serial.print(" ");
			}
		    Serial.println();
		    Serial.print("RemoteID = ");
		    Serial.println(remoteID);

		    switch (data[0]) {

		        case 116:
		          temp = getTemperature();
                          payload[0] = highByte(temp);
                          payload[1] = lowByte(temp);
                          tx.setAddress16(remoteID);
                          xbee.send(tx);
                          Serial.print("Temp = ");
		          Serial.println(temp, HEX);  
		          break;

		        case 104:
		          humid = getHumidity();
                          payload[0] = highByte(humid);
                          payload[1] = lowByte(humid);
                          tx.setAddress16(remoteID);
                          xbee.send(tx);
		          Serial.print("Humid = ");
		          Serial.println(humid, HEX);
		          break;

		        case 99:
		          //int co2 = getCO2();
		          break;

		        default:
		          break;
		    }
		}

	}
}

