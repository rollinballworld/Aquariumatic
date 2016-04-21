//Required Libraries
#include <LiquidCrystal.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>

/*AQUARIUMATIC SLAVE UNIT
 Screen connection:
 * LCD RS pin to digital pin 12 | LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5  | LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3  | LCD D7 pin to digital pin 2
 * LCD R/W pin to ground        | LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground       | wiper to LCD VO pin (pin 3)
*/

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

//Define the Relay pins
#define BLPin   6   //Backlight Pin
#define HeatingRelay  7                    
#define LightRelay  8
#define PumpRelay  9
#define RELAY4  10
#define SensorPin A0
#define TempPin A1  //Change to Digital? Add 4.7k resistor between 5v and TempPin

OneWire oneWire(TempPin);
DallasTemperature sensors(&oneWire); 
DeviceAddress insideThermometer = { 0x28, 0xB4, 0x6B, 0xC8, 0x04, 0x00, 0x00, 0x1F };     // Assign the addresses of your 1-Wire temp sensors.

//define variables
String stri2c = "";     // for incoming i2c data
String strSerial = "";  // for incoming serial data
float MinTemp = 0;
float MaxTemp = 0;
float MinpH = 0;
float MaxpH = 0;

void setup() {
 Serial.begin(9600);
 sensors.begin();            //start up temp probe library
 sensors.setResolution(insideThermometer, 10);       // set the temp probe resolution to 10 bit

  //set up the Relays as outputs
  pinMode(BLPin, OUTPUT);
  pinMode(HeatingRelay, OUTPUT);
  pinMode(LightRelay, OUTPUT);
  pinMode(PumpRelay, OUTPUT);
  pinMode(RELAY4, OUTPUT);
  //pinMode(TempPin, INPUT);
  
  // join i2c bus with slave address #10
  Wire.begin(10);                
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  //Switch on Backlight
  digitalWrite (BLPin, HIGH);
  // Print a message to the LCD.
  lcd.print("Aquariumatic v1");
  //startupinfo();
}


void loop() {
 CheckSerial();
  // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  lcd.setCursor(0, 0);
  // print the Temperature:
  lcd.print("Temp: " + String(CurrentTemp()) + "     ");
  //lcd.print("Temp Value");

  lcd.setCursor(0,1);
  // print the pH
  lcd.print("pH: " + String(CurrentpH()) + "       ");
  //lcd.print("pH Value       ");
  delay(500);
}

void receiveEvent(int howMany){
  // function that executes whenever data is received from master
  // this function is registered as an event, see setup()
  stri2c = "";
  while( Wire.available()){
    //x += (char)Wire.read();
    stri2c += Wire.readString();
  }
  do_command(stri2c);
}

void requestEvent(){
  //Collect data as a string then convert using c_str
  //Wire.write(data.c_str());
  //Use to send mail requests etc?
}

void CheckSerial() {
  //Serial.println("Checking Serial");
  strSerial = "";
  while(Serial.available()){
   strSerial += Serial.readString();
  }
  do_command(strSerial);
}

void do_command(String x) {
  if (x == "HeatingOn"){
    Heating("on");
  }
  else if (x == "HeatingOff"){
    Heating("off");
  }
  else if (x == "LightOn"){
    Lights("on");
  }
  else if (x == "LightOff"){
    Lights("off");
  }
  else if (x == "PumpOn"){
    Pump("on");
  }
  else if (x == "PumpOff"){
    Pump("off");
  }
  else if (x == "CurrentTemp"){
    Serial.println(String(CurrentTemp()));
  }
  else if (x == "CurrentpH"){
    Serial.println(String(CurrentpH()));
  }
  else if (x == "CurrentLight"){
    Serial.println(Lights("check"));
  }
  else if (x == "CurrentPump"){
    Serial.println(Pump("check"));
  }
  else if (x == "Parameters"){
    //MinTemp = Serial.read();
  }
  else{
    return;
  }
}

void startupinfo(){
Serial.println("Aquariumatic Tank Unit");
Serial.println("");
Serial.println("http://www.facebook.com/Aquariumatic");
Serial.println("");
Serial.println("This unit is to simulate temp and pH sensor readings");
Serial.println("and to process incoming requests from the master unit.");
Serial.println("");
Serial.println("Currently focusing on serial communication.");
Serial.println("i2c to follow"); 
}

float CurrentTemp(){
 sensors.requestTemperatures();
 float tempC = sensors.getTempC(insideThermometer);
 //int tempC = analogRead(TempPin);
 return tempC;
}

float CurrentpH(){
 //to write code to simulate changing values
 return 7.0;
}

String CurrentLight(){
 return "OFF";
}
String CurrentPump(){
 return "ON";
}

String Heating(String x){
   if (x == "on"){
      digitalWrite (HeatingRelay, HIGH);
      //Serial.println("Heating Turned On");
      return "";}
  else if (x == "off"){
      digitalWrite (HeatingRelay, LOW);
      //Serial.println("Heating Turned Off");
      return "";}
  else if (x == "check"){
    if (digitalRead (HeatingRelay) == LOW){
      return "OFF";}
      else{return "ON";}
    }
  }

String Lights(String x){
  if (x == "on"){
    digitalWrite (LightRelay, HIGH);
    //Serial.println("Lights turned On");
    return "";
  }
  else if (x == "off"){
    digitalWrite (LightRelay, LOW);
    //Serial.println("Lights turned Off");
    return"";
  }
  else if (x == "check"){
    if (digitalRead (LightRelay) == LOW){
      return "OFF";}
    else{return "ON";}
    }
}

String Pump(String x){
  if (x == "on"){
    digitalWrite (PumpRelay, HIGH);
    //Serial.println("Pump turned On");
    return "";
  }
  else if (x == "off"){
    digitalWrite (PumpRelay, LOW);
    //Serial.println("Pump turned Off");
    return "";
  }
  else if (x == "check"){
    if (digitalRead (PumpRelay) == LOW){
      return "OFF";}
    else{return "ON";}
    }  
}
