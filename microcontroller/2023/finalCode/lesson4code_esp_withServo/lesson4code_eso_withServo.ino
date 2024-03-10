//#include <ESP8266WiFi.h>
#include <WiFi.h>
#include <ESP32Servo.h>

Servo servo;

int servoPWM = 14; 

WiFiServer serverr(6500);

byte ContrInput;

//---------------------------------------------------------------------------------
void setup(){
  Serial.begin(9600);

  servo.setPeriodHertz(50);
  servo.attach(servoPWM);

  WiFi.softAP("(YOUR NAME)'s ESP32 Network", "thereisnospoon"); 
  Serial.println(WiFi.localIP());
  //WiFi.setSleep(WIFI_NONE_SLEEP);//WiFi.setSleepMode(WIFI_NONE_SLEEP);
  serverr.begin();
}
//---------------------------------------------------------------------------------

void loop(){
  WiFiClient controllerSock = serverr.available();

  while (controllerSock){
    ContrInput = controllerSock.read();
    while(ContrInput != 255){
      yield();

      //---------------Robot Functionality Starts Here------------------

      // say what you got:
      Serial.print("I received: ");
      Serial.println(ContrInput, DEC);

      if (ContrInput == 119) {
        servo.write(90);
      } else if (ContrInput == 115) {
        servo.write(0);
      }
      //---------------Robot Functionality Ends Here--------------------

      ContrInput = controllerSock.read();
    }
    delay(50);
  }
  
  delay(2000);
}



