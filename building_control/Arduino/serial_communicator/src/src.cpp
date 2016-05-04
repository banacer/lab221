//#include <TF>
#include "../lib/kSeries.h"
#include "Arduino.h"
#include "../lib/DHT.h"
kSeries K_30(12,13);
#define DHTPIN 5
#define DHTTYPE DHT22
#define DAMPERPIN 9
DHT dht(DHTPIN,DHTTYPE);

/*
 * Returns the temperature in Fahrenheit
 */
float getTemperature()
{
    float t = dht.readTemperature(true);
    if(isnan(t))
      return -1;
    return t;
}

/*
 *  Returns relative humidity
 */
float getHumidity()
{
    float h = dht.readHumidity();
    if(isnan(h))
      return -1;
    return h;
}

float getCO2()
{
  float co2 = K_30.getCO2('p');
  return co2;
}
void setup()
{
  Serial.begin(9600);
  pinMode(DAMPERPIN, OUTPUT);
  dht.begin();
}
int control_damper(int data)
{
  int damper_value = 0;
  damper_value = (int) (2.55 * (float)data);
  analogWrite(DAMPERPIN, damper_value);
  return damper_value;
}

void loop()
{
  while (Serial.available() == 0)
    delay(100);
  char cmd = Serial.read();

  if(cmd == 'd') {
    int val = Serial.read();
    control_damper(val);
    Serial.println('A');
  }

  else if (cmd == 't') {
    float temp = getTemperature();
    Serial.println(temp);
    //Serial.println('\n');
  }

  else if (cmd == 'h') {
    float hum = getHumidity();
    Serial.println(hum);
    //Serial.println('\n');
  }

  else if (cmd == 'c') {
    float co2 = getCO2();
    Serial.println(co2);
    //Serial.println('\n');
  }
  else {
    Serial.println("E");
  }
}
