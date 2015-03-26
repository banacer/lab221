#include <XBee.h>
#define dampCntrlPin 9

uint8_t payload[3] = {0,0,0};
uint8_t* data;
int dataLen;
int remoteID; 
XBee xbee = XBee();


Tx16Request tx = Tx16Request(remoteID, payload, sizeof(payload));
Rx16Response rx = Rx16Response();


int cntrlDamper(int data)
{
int dampCntrlVal = 0;
dampCntrlVal = (255/100)* data;
analogWrite(dampCntrlPin, dampCntrlVal);
Serial.println(dampCntrlVal);
return dampCntrlVal;
}


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
	   if(data[0] == 100)
	   {
	      if(data[1] < 0 || data[1] > 100)
	      {
		   Serial.print("Control Value OUT OF BOUNDS");
	      }
	      else
	      {
		   payload[0] = cntrlDamper(data[1]);
		   Serial.println(payload[0]);
		   tx.setAddress16(remoteID);
		   xbee.send(tx);
              }

	  }

		    
      }
      
      
    }

	
}

