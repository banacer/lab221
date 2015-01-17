//Variable declarations 
const int pingPin1 = 7;//Pin number for the SIG of the sensor 1
const int pingPin2 = 8;
const int speakerPin = 2;
int node_id = 5;
int occupancy=0;
unsigned long time; //time of occupancy in milliseconds
// defining the border of the interval
long minDistance = 10; //10cm
long maxDistance = 200; //200cm


void setup(){
  Serial.begin(9600); //intialize serial communication
  //Testing speaker 
  //pinMode(speakerPin, OUTPUT);
  //here goes the code of the Piezo speaker



}

void loop()
{ //Serial.println("I am here");
  long cm1, cm2;
  boolean beam1Crossed =false;
  boolean beam2Crossed = false;
  boolean passage= false;
  boolean here=false; // we presume we cannot have an entrance and an exit at the same time

    //calculate distance for the first time
  cm1= getEchoDistance(pingPin1);
  delay(5);
  //delay(50); //delay to have no interference between the two beams
  cm2= getEchoDistance(pingPin2);


  while ( cm1 < maxDistance && cm1 > minDistance )
  { 
    delay(10);
    cm1 = getEchoDistance(pingPin1);
    beam1Crossed= true;
  }
  if ( (cm1 >= (maxDistance + 30 ) ) && (beam1Crossed == true)) //Object has quitted beam1 after previously crossing the beam1
  {  
    delay(2);
    cm2= getEchoDistance(pingPin2); 
    int i=0;
    while ( cm2 >= maxDistance || cm2 <= minDistance){

      i++;  
      cm2 = getEchoDistance(pingPin2); 

    }

    while ( cm2 < maxDistance && cm2 > minDistance) //Object crossed beam2
    {          


      delay(10);
      cm2 = getEchoDistance(pingPin2);
      beam2Crossed= true;

    }
    //delay(200); // delay to make sure the object has quitted the beam
    if( (cm2 >= (maxDistance + 30)) && (beam2Crossed == true))//Object has quitted beam2
    { 


      occupancy++;//object entered room
      time=millis(); //time when object entered room
      roomOccupancy();
      delay(2000);//minimum time required between two passages 
      passage = true;
    }
  }
  if( !passage && ( cm2 < maxDistance && cm2 > minDistance))
  {
    //Serial.println(cm2);

    while( cm2 < maxDistance && cm2 > minDistance)//Object crossed beam2 first
    { 
      delay(10);

      cm2 = getEchoDistance(pingPin2);
      beam2Crossed= true;
    }
    if ( (cm2 >= (maxDistance + 30)) && (beam2Crossed == true)) //Object has quitted beam2 after previously crossing the beam2
    { 
      delay(2);
      cm1= getEchoDistance(pingPin1);

      int j =0;
      while ( cm1 >= maxDistance || cm1 <= minDistance ) { 

        j++; 
        cm1 = getEchoDistance(pingPin1); 

      }

      while ( cm1 < maxDistance && cm1 > minDistance) //Object crossed beam1
      { 
        delay(10);
        cm1 = getEchoDistance(pingPin1);
        beam1Crossed= true;

      }

      if( ((cm1 >= (maxDistance + 30))|| (cm1 == 0)) && (beam1Crossed == true))//Object has quitted beam1
      { 

        if (occupancy > 0) occupancy--;//object entered room
        time=millis(); //time when object entered room
        roomOccupancy();
        delay(2000); // minimum time required between two passages 

      }
    }
  }

}




long getEchoDistance(int pinNumber)
{   
  long distance, duration;
  pinMode(pinNumber, OUTPUT);
  digitalWrite(pinNumber, LOW);
  delayMicroseconds(2);
  digitalWrite(pinNumber, HIGH);
  delayMicroseconds(5);
  digitalWrite(pinNumber, LOW);
  //Sensor is transmitting the time it tooks the echo to get back
  pinMode(pinNumber, INPUT);
  duration= pulseIn(pinNumber, HIGH);
  distance = duration / 29 / 2; // microseconds to centimeters
  return distance; 
}

void roomOccupancy()
{ 
  Serial.print("node_");
  Serial.print(node_id);
  Serial.print("\t");
  Serial.print("Occupancy = ");
  Serial.println(occupancy) ;
}





