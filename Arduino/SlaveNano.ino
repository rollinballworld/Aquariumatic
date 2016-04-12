#include <LiquidCrystal.h>
#include <Wire.h>
//include OneWire for temp probe
//include library for pH probe
//include library for lcd screen

/*AQUARIUMATIC TEST SKETCH
Script to be ran on my test Nano, with lcd screen and two relays.
The sensor data will be simulated; every time pH/Temp/Light status is requested 
they will step through a series of values to show change.
 Screen connection:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)
*/

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

//Define the Relay pins
#define RELAY1  6                    
#define RELAY2  7

//define variables
String stri2c = "";     // for incoming i2c data
String strSerial = "";  // for incoming serial data

void setup() {
 Serial.begin(9600);
  //set up the Relays as outputs
  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);
  
  // join i2c bus with slave address #10
  Wire.begin(10);                
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("Aquariumatic v1");
  startupinfo();
}

void loop() {
 CheckSerial();
  // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  lcd.setCursor(0, 1);
  // print the Temperature:
  lcd.print("Temp: " && CurrentTemp());
  delay(2000);
  lcd.setCursor(0, 1);
  // print the pH
  lcd.print("Temp: " && CurrentpH());
  delay(2000);
}

void receiveEvent(int howMany)
{
  // function that executes whenever data is received from master
  // this function is registered as an event, see setup()
  stri2c = "";
  while( Wire.available()){
    //x += (char)Wire.read();
    stri2c += Wire.readString();
  }
  do_command(stri2c);
}

void requestEvent()
{
  //Return temp and pH Readings as a char
  //Collect data as a string then convert using c_str
  //Wire.write(data.c_str());
}

void do_command(String x) {
  if (x == "HeatingOn"){
    ToggleRelay(RELAY1);
  }
  else if (x == "HeatingOff"){
    ToggleRelay(RELAY1);
  }
  else if (x == "LightOn"){
    ToggleRelay(RELAY2);
  }
  else if (x == "LightOff"){
    ToggleRelay(RELAY2);
  }
  else if (x == "PumpOn"){
    ToggleRelay(RELAY2);
  }
  else if (x == "PumpOff"){
    ToggleRelay(RELAY2);
  }
  else if (x == "CurrentTemp"){
    CurrentTemp();
  }
  else if (x == "CurrentpH"){
    CurrentpH();
  }
  else if (x == "CurrentLight"){
    CurrentLight();
  }
  else if (x == "CurrentPump"){
    CurrentPump();
  }
  else{
  }
}

void startupinfo(){
Serial.println("Aquariumatic Test Unit");
Serial.println("");
Serial.println("http://www.facebook.com/Aquariumatic");
Serial.println("");
Serial.println("This unit is to simulate temp and pH sensor readings");
Serial.println("and to process incoming requests from the master unit.");
Serial.println("");
Serial.println("Currently focusing on serial communication.");
Serial.println("i2c to follow"); 
}

void CheckSerial() {
  strSerial = "";
  while(Serial.available()){
   strSerial += Serial.readString();
  }
  Serial.print("Received: ");
  Serial.println(strSerial);
  do_command(strSerial);
}

float CurrentTemp(){
 //to write code to simulate changing values
 return 45;
}

float CurrentpH(){
 //to write code to simulate changing values
 return 7.0;
}

void CurrentLight(){
 return 'OFF';
}
void CurrentPump(){
 return 'ON';
}

void ToggleRelay(char RelayNo) {
    if (digitalRead (RelayNo) == LOW){
      digitalWrite (RelayNo, HIGH);
      Serial.print(RelayNo);
      Serial.println(" toggled ON");
    }
    else{
      digitalWrite (RelayNo, LOW);
      Serial.print(RelayNo);
      Serial.println(" toggled OFF");
    }
}
