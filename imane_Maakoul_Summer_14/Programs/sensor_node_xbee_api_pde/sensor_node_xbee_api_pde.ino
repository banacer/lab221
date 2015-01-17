#include <XBee.h>
#include <TF>
#include "kSeries.h" //include kSeries Library 
#include <dht.h>

dht DHT;

#define DHT22_PIN 5
kSeries K_30(12,13); //Initialize a kSeries Sensor with pin 12 as Rx and 13 as Tx 
XBee xbee = XBee();
int whatSensor = 0;
unsigned long start = millis();

// allocate two bytes for to hold a 10-bit analog reading
uint8_t payload[3];

// with Series 1 you can use either 16-bit or 64-bit addressing

// 16-bit addressing: Enter address of remote XBee, typically the coordinator
Tx16Request tx = Tx16Request(0x5678, payload, sizeof(payload));

TxStatusResponse txStatus = TxStatusResponse();

int statusLed = 11;
int errorLed = 12;

void flashLed(int pin, int times, int wait) 
{
    
    for (int i = 0; i < times; i++) {
      digitalWrite(pin, HIGH);
      delay(wait);
      digitalWrite(pin, LOW);
      
      if (i + 1 < times) {
        delay(wait);
      }
    }
}

void setup() 
{
  pinMode(statusLed, OUTPUT);
  pinMode(errorLed, OUTPUT);
  Serial.begin(9600);
  xbee.setSerial(Serial);
}

void loop() 
{
    
   
   // start transmitting after a startup delay.  Note: this will rollover to 0 eventually so not best way to handle
    if (millis() - start > 10000) {
      // break down 10-bit reading into two bytes and place in payload
      if(whatSensor == 0)
      {
          short data = (short) K_30.getCO2('p');
          payload[0] = 0;
          payload[1] = data >> 8 & 0xff;
          payload[2] = data & 0xff; 
      }
      else if(whatSensor == 1)
      {
          int chk = DHT.read22(DHT22_PIN);
          short data = (short) (DHT.humidity * 100);
          payload[0] = 1;
          payload[1] = data >> 8 & 0xff;
          payload[2] = data & 0xff;             
      }
      else if(whatSensor == 2)
      {
          int chk = DHT.read22(DHT22_PIN);
          short data = (short) (DHT.temperature * 100);
          payload[0] = 2;
          payload[1] = data >> 8 & 0xff;
          payload[2] = data & 0xff;          
      }
      
      xbee.send(tx);       
      // flash TX indicator
      flashLed(statusLed, 1, 100);
    }
  
    // after sending a tx request, we expect a status response
    // wait up to 5 seconds for the status response
    if (xbee.readPacket(5000)) {
        // got a response!

        // should be a znet tx status            	
    	if (xbee.getResponse().getApiId() == TX_STATUS_RESPONSE) {
    	   xbee.getResponse().getZBTxStatusResponse(txStatus);
    		
    	   // get the delivery status, the fifth byte
           if (txStatus.getStatus() == SUCCESS) {
            	// success.  time to celebrate
             	flashLed(statusLed, 5, 50);
           } else {
            	// the remote XBee did not receive our packet. is it powered on?
             	flashLed(errorLed, 3, 500);
           }
        }      
    } else if (xbee.getResponse().isError()) {
      //nss.print("Error reading packet.  Error code: ");  
      //nss.println(xbee.getResponse().getErrorCode());
      // or flash error led
    } else {
      // local XBee did not provide a timely TX Status Response.  Radio is not configured properly or connected
      flashLed(errorLed, 2, 50);
    }
    whatSensor++;
    whatSensor = whatSensor % 3;
    delay(1000);
}
