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
//#define RELAY4  10
#define TempPin 10  //Change to Digital? Add 4.7k resistor between 5v and TempPin
#define SensorPin A0
#define Offset -0.08            //deviation compensate
#define samplingInterval 20
#define printInterval 800
#define ArrayLenth  40    //times of collection
int pHArray[ArrayLenth];   //Store the average value of the sensor feedback
int pHArrayIndex=0;    

OneWire oneWire(TempPin);
DallasTemperature sensors(&oneWire); 

//define variables
String stri2c = "";     // for incoming i2c data
String strSerial = "";  // for incoming serial data
float MinTemp = 20;
float MaxTemp = 29;
float MinpH = 5.5;
float MaxpH = 8.5;

void setup() {
 //analogReference(DEFAULT);  //for use to determine whether it is safe to print to the lcd screen
 Serial.begin(9600);
 sensors.begin();            //start up temp probe library
 //sensors.setResolution(insideThermometer, 10);       // set the temp probe resolution to 10 bit

  //set up the Relays as outputs
  pinMode(BLPin, OUTPUT);
  pinMode(HeatingRelay, OUTPUT);
  pinMode(LightRelay, OUTPUT);
  pinMode(PumpRelay, OUTPUT);
  //pinMode(RELAY4, OUTPUT);
  pinMode(TempPin, INPUT);
  
  // join i2c bus with slave address #10
  Wire.begin(10);                
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  //Switch on Backlight
  digitalWrite (BLPin, HIGH);
  // Print a message to the LCD.
  lcd.setCursor(0,0);
  lcd.print("Aquariumatic v1");
  lcd.setCursor(0,1);
  lcd.print(" By L. O'Reilly ");
  delay(2000);
  //startupinfo();
}

void loop() {
 CheckSerial();
 LCDUpdate();
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
    Serial.println("Parameters received.");
  }
  else if (x == "ResetSlave"){
    //MinTemp = Serial.read();
    Serial.println("Resetting...");
    resetFunc();
  }
  else{
    return;
  }
}

void(* resetFunc) (void) = 0;//declare reset function at address 0

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
 float reading = sensors.getTempCByIndex(0);
 //float reading = analogRead(TempPin);
 /*
 // converting that reading to voltage, for 3.3v arduino use 3.3
 float voltage = reading * 5.0;
 voltage /= 1024.0;  
 // Temp in Celsius
 float tempC = (voltage - 0.5) * 100 ;
 // Temp in Fahrenheit
 float tempF = (tempC * 9.0 / 5.0) + 32.0;
 
 return tempC;*/
 return reading;
}

float CurrentpH(){
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue,voltage;
  if(millis()-samplingTime > samplingInterval)
  {
      pHArray[pHArrayIndex++]=analogRead(SensorPin);
      if(pHArrayIndex==ArrayLenth)pHArrayIndex=0;
      voltage = avergearray(pHArray, ArrayLenth)*5.0/1024;
      pHValue = 3.5*voltage+Offset;
      samplingTime=millis();
  }
  return pHValue;
}

double avergearray(int* arr, int number){
  int i;
  int max,min;
  double avg;
  long amount=0;
  if(number<=0){
    Serial.println("Error number for the array to avraging!/n");
    return 0;
  }
  if(number<5){   //less than 5, calculated directly statistics
    for(i=0;i<number;i++){
      amount+=arr[i];
    }
    avg = amount/number;
    return avg;
  }else{
    if(arr[0]<arr[1]){
      min = arr[0];max=arr[1];
    }
    else{
      min=arr[1];max=arr[0];
    }
    for(i=2;i<number;i++){
      if(arr[i]<min){
        amount+=min;        //arr<min
        min=arr[i];
      }else {
        if(arr[i]>max){
          amount+=max;    //arr>max
          max=arr[i];
        }else{
          amount+=arr[i]; //min<=arr<=max
        }
      }//if
    }//for
    avg = (double)amount/(number-2);
  }//if
  return avg;
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

void LCDUpdate(){
    // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  lcd.setCursor(0, 0);
  // print the Temperature:
  if (CurrentTemp() > MaxTemp){
    lcd.print("TEMP HIGH       ");}
  else if (CurrentTemp() < MinTemp){
    lcd.print("TEMP LOW        ");}
  else{
  lcd.print("Temp: " + String(CurrentTemp()) + "     ");
  }
  lcd.setCursor(0,1);
  // print the pH
  if (CurrentpH() > MaxpH){
    lcd.print("pH HIGH         ");}
  else if (CurrentpH() < MinpH){
    lcd.print("pH LOW          ");}
  else{
  lcd.print("pH: " + String(CurrentpH()) + "       ");
  }
}
