#include <Wire.h>					// For the i2c devices
#include <LiquidCrystal_I2C.h>	// For the LCD

LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

// SCL - check pins for Mega
// SDA - check pins for Mega


const byte MY_ADDRESS = 42;
const byte PI_ADDRESS = 40;
const byte SCREEN_ADDRESS = 25;

byte tMSB, tLSB;

float my_temp;
char my_array[100];            // Character array for printing something.

void setup()
{
  Wire.begin (MY_ADDRESS);
  Serial.begin(9600);
  lcd.init();                      // initialize the lcd 
  for (byte i = 2; i <= 7; i++)   // Change this to the Relay board pins when the time comes
    pinMode (i, OUTPUT);
  Wire.onReceive (receiveEvent);
  
}

void loop()
{
  int v = analogRead (0);
  Wire.beginTransmission (PI_ADDRESS);
  Wire.write (v < 512);       //Change to temp and pH readings
  Wire.endTransmission ();
  Serial.print(" - Temp: "); 
  Serial.println(my_temp);    //Change to temp & pH readings
  delay (2000);               //To toggle
  
// Print a message to the LCD.
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Test Display I2C");
  lcd.setCursor(0,1);
  lcd.print(my_array);
  delay(1000);
}

// called by interrupt service routine when incoming data arrives
//Amend this to receive various commands to trigger the relays
void receiveEvent (int howMany)
 {
  for (int i = 0; i < howMany; i++)
    {
    byte c = Wire.read ();
    // toggle requested LED
    if (digitalRead (c) == LOW)
      digitalWrite (c, HIGH);
    else
      digitalWrite (c, LOW);
    }  // end of for loop
  }  // end of receiveEvent
