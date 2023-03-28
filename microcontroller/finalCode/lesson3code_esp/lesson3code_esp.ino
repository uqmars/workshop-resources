

void setup() {
  Serial.begin(9600);

  // put your setup code here, to run once:
  pinMode(led, OUTPUT);
  pinMode(button, INPUT_PULLUP);

  servo.setPeriodHertz(50);
  servo.attach(servoPWM);
}

void loop() {
  // put your main code here, to run repeatedly:

  int buttonPress = digitalRead(button);

  Serial.println(buttonPress);


  if (buttonPress == 0) {
    digitalWrite(led, HIGH);
    servo.write(90);
  } else {
    digitalWrite(led, LOW);
    servo.write(0);
  }
  
  delay(300);
  

}