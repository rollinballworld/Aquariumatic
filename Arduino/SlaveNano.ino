/*Script to be ran on my test Nano, with lcd screen and two relays.
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

// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

//Define the Relay pins
#define RELAY1  6                        
#define RELAY2  7 

void setup() {
  //set up the Relays as outputs
  pinMode(RELAY1, OUTPUT);       
  pinMode(RELAY2, OUTPUT);
  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("Aquariumatic v1");
  Splash_Screen();
}

void loop() {
  // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  lcd.setCursor(0, 1);
  // print the number of seconds since reset:
  lcd.print("Temp: " & );
}

void startupinfo(){
Serial.println("Aquariumatic Test Unit");
Serial.println("");
Serial.println("http://www.facebook.com/Aquariumatic");
Serial.println("");
Serial.println("This unit is to simulate temp and pH sensor readings");
Serial.println("and to process incoming requests from the master unit.");
Serial.println("");
Serial.println("This process is a serial");
 
}

void ToggleRelay(RelayNo) {
    if (digitalRead (RelayNo) == LOW)
      digitalWrite (RelayNo, HIGH);
      Serial.print(RelayNo & " toggled ON");
    else
      digitalWrite (RelayNo, LOW);
      Serial.print(RelayNo & " toggled OFF");
}
