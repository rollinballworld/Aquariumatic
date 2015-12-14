/*
  Script to print PH to serial
 
 
  28/8/2015  Michael Ratcliffe  Mike@MichaelRatcliffe.com
 
 
          This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
 
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
 
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
    Parts:
    -Arduino - Uno/Mega
  -df Robot Ph Probe Kit [SKU:SEN0169] This is a great PH sensor compared to the ones ive had in the past
 
 
 
    See www.MichaelRatcliffe.com/Projects for a Pinout and user guide or consult the Zip you got this code from
 
*/
 
 
//************************** Libraries Needed To Compile The Script [See Read me In Download] ***************//
// Both below Library are custom ones [ SEE READ ME In Downloaded Zip If You Dont Know how To install] Use them or add a pull up resistor to the temp probe
 
 
#include <OneWire.h>
#include <DallasTemperature.h>
#include <LiquidCrystal.h> //Standard LCD Lbrary
#include <EEPROM.h> //Standard EEPROM Library
 
 
//*********************** User defined variables ****************************//
//pH meter Analog output to Arduino Analog Input 0
int PHPin =A15;
//The calibration constant for the PH probe
float K_PH=3.64;       
//used for min/max logs
float MinPH=10;
float MaxPH=0;
 
 
 
 
//************ Temp Probe Related *********************************************//
#define ONE_WIRE_BUS 26          // Data wire For Temp Probe is plugged into pin 10 on the Arduino
const int TempProbePossitive =22;  //Temp Probe power connected to pin 9
const int TempProbeNegative=24;    //Temp Probe Negative connected to pin 8
float Temperature=0.0;
float MinT=100;
float MaxT=0;
 
 
 
 
//********************** End Of Recomended User Variables ******************//
 
 
 
 
//************** Some values for working out the ph*****************//
float Kn=0;
float phValue=0;
int i=0;
long reading=0;
unsigned long sum=0;
float average=0;
 
 
// select the pins used on the LCD panel
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
 
 
// define some values used by the panel and buttons
int lcd_key    = 0;
int adc_key_in  = 0;
int button =0;
#define btnRIGHT  1
#define btnUP    2
#define btnDOWN  3
#define btnLEFT  4
#define btnSELECT 5
#define btnNONE  6
 
 
int Screen =1;
//Max number of screens on lcd
const int Last_Screen_no =4;
//used to debounce input button
int buttonLast=0;
 
 
OneWire oneWire(ONE_WIRE_BUS);// Setup a oneWire instance to communicate with any OneWire devices
DallasTemperature sensors(&oneWire);// Pass our oneWire reference to Dallas Temperature.
 
 
//************************** Just Some basic Definitions used for the Up Time LOgger ************//
long Day=0;
int Hour =0;
int Minute=0;
int Second=0;
int HighMillis=0;
int Rollover=0;
 
 
//***************** Specifying where to sotre the calibration value [non volatile memory **//
int value; //we use this to check if memory has been writen or not
int addresCalibrationPH=50;
 
 
//************************************** Setup Loop Runs Once ****************//
void setup()
{
  Serial.begin(9600);
  pinMode(TempProbeNegative , OUTPUT ); //seting ground pin as output for tmp probe
  digitalWrite(TempProbeNegative , LOW );//Seting it to ground so it can sink current
  pinMode(TempProbePossitive , OUTPUT );//ditto but for positive
  digitalWrite(TempProbePossitive , HIGH );
  read_Temp();// getting rid of the first bad reading
  Read_Eprom();
  Splash_Screen();
 
 
}
//******************************** End Of Setup **********************************//
 
 
//******************** Main Loops runs Forver ************************************//
void loop()
{
 
 
//All these functions are put below the main loop, keeps the loop logic easy to see
read_LCD_buttons();
read_Temp();
Log_Min_MaxTemp();
ReadPH();
Log_Min_MaxPH();
uptime();
CalibratePH();
PrintReadings();
delay(100);
};
 
 
//************************** End Of Main Loop ***********************************//
 
 
 
 
//*************************Print Some useful startup info **************************//
void startupinfo(){
Serial.println("pH Probe Script for arduino");
Serial.println("Released under GNU by Michael Ratcliffe");
Serial.println("www.MichaelRatcliffe.com");
Serial.println("Element14 'Adapted_Greenhouse'");
Serial.println("Using DFRobot PH Probe Pro ");
Serial.println("How to Use:");
Serial.println("1:Place Probe into pH7 calibration fluid, open serial ");
Serial.println("2:Take Recomened cell constand and change it in the top of code");
Serial.println("3:Rinse Probe and place in pH4 calibration fluid");
Serial.println("4:Adjust potentiometer on pH meter shield until ph reading in serial is 4");
Serial.println("    ");
Serial.println("Thats it your calibrated and your readings are accurate!");
 
}
 
 
//***************************** Function to read temperature ********************************//
void read_Temp(){
sensors.requestTemperatures();// Send the command to get temperatures
Temperature=sensors.getTempCByIndex(0); //Stores Value in Variable
 
 
 
 
}
 
 
 
 
 
 
//*************************Take Ten Readings And Average ****************************//
void ReadPH(){
  i=1;
  sum=0;
  while(i<=100){
  reading=analogRead(PHPin);
  sum=sum+reading;
    delay(20);
    i++;
  }
average=sum/i;
//converting the average to PH 3.5 part convers mv to ph
phValue=average*K_PH*5/1024;
 
}
 
 
 
 
 
 
 
 
 
 
//****************************** Reading LCd Buttons ****************************//
void read_LCD_buttons(){
  adc_key_in = analogRead(0);      // read the value from the sensor
// my buttons when read are centered at these valies: 0, 144, 329, 504, 741
// we add approx 50 to those values and check to see if we are close
if (adc_key_in > 1000)  button =0;
 
 
else if (adc_key_in < 50)  button =1;
else if (adc_key_in < 250)  button =2;
else  if (adc_key_in < 450)  button =3;
else if (adc_key_in < 650)  button =4;
else if (adc_key_in < 850)  button =5;
 
 
 
 
//Second bit stops us changing screen multiple times per input
if(button==2&&buttonLast!=button){
Screen++;
 
 
}
else if (button==3&&buttonLast!=button){
Screen--;
};
 
 
if (Screen>=Last_Screen_no) Screen=Last_Screen_no;
if(Screen<=1) Screen=1;
 
 
buttonLast=button;
};
 
 
 
 
 
 
//************************ Uptime Code - Makes a count of the total up time since last start ****************//
 
 
void uptime(){
//** Making Note of an expected rollover *****//
if(millis()>=3000000000){
HighMillis=1;
 
 
}
//** Making note of actual rollover **//
if(millis()<=100000&&HighMillis==1){
Rollover++;
HighMillis=0;
}
 
 
long secsUp = millis()/1000;
 
 
Second = secsUp%60;
 
 
Minute = (secsUp/60)%60;
 
 
Hour = (secsUp/(60*60))%24;
 
 
Day = (Rollover*50)+(secsUp/(60*60*24));  //First portion takes care of a rollover [around 50 days]
                 
};
 
 
 
 
//************************** Printing somthing useful to LCd on start up **************************//
void Splash_Screen(){
 
 
lcd.begin(16, 2);              // start the library
lcd.setCursor(0,0);
delay(1000);
lcd.print("PH meter      ");
lcd.setCursor(0,1);
delay(1000);
lcd.print("Mike Ratcliffe");
lcd.setCursor(0,1);
delay(1000);
lcd.setCursor(0,1);
lcd.print("Free Software  ");
delay(1000);
lcd.setCursor(0,1);
lcd.print("Mike Ratcliffe");
delay(1000);
lcd.setCursor(0,1);
lcd.print("Free Software  ");
delay(1000);
  lcd.setCursor(0,0);
lcd.print("To Navigate        ");
  lcd.setCursor(0,1);
lcd.print("Use Up-Down    ");
delay(3000);
  lcd.setCursor(0,0);
lcd.print("To Calibrate      ");
  lcd.setCursor(0,1);
lcd.print("Hold Select      ");
delay(3000);
 
 
 
 
};
 
 
void Read_Eprom(){
 
 
//************** Restart Protection Stuff ********************//
  //the 254 bit checks that the adress has something stored to read [we dont want noise do we?]
  value = EEPROM.read(addresCalibrationPH);
  if (value <=254) K_PH=value*0.02;
 
 
};
 
 
//******************************* Checks if Select button is held down and enters Calibration routine if it is ************************************//
void CalibratePH(){
 
 
 
//we check if we are on ph screen and the select button is held
if(Screen!=4) return;
if(button!=5) return;
else delay(1000);
read_LCD_buttons();
if(button!=5) return;
 
 
//we need to stop in this loop while the user calibrates
while(1){
read_LCD_buttons();
lcd.setCursor(0,0);
lcd.print("Ph Probe in pH7  ");
lcd.setCursor(0,1);
lcd.print("Press Right            ");
//user pressed right?
if(button==1) break;
delay(100);
      };
 
lcd.setCursor(0,0);
lcd.print("Calibrating              ");
lcd.setCursor(0,1);
lcd.print("pH Probe                ");
 
 
//let probe settle
delay(2000);
 
 
//read the ph probe
ReadPH();
Kn=((7*1024)/(average*5));
 
 
 
 
while (1) { // wee need to keep this function running until user opts out with return function
                         
  read_LCD_buttons();
  if(button==4) return; //exits the loop without saving becauser user asked so
  if (button==5){
                           
                           
  K_PH=Kn; //saving the new cell constant
                         
                         
  //*******Saving the new value to EEprom**********//
  value=Kn/0.02;
  EEPROM.write(addresCalibrationPH, value);
  lcd.setCursor(0,0);
  lcd.print("Saved Calibration        ");
                                                       
  lcd.setCursor(0,1);
  lcd.print("K:                        ");
  lcd.setCursor(3,1);
  lcd.print(Kn);
  delay(2000);
 
  lcd.setCursor(0,0);
  lcd.print("Now pH4 and          ");
                                                       
  lcd.setCursor(0,1);
  lcd.print("Adjust Pot                      ");
 
  delay(4000);
  //Put back to main screen and exit calibration
    Screen=1;
  return;
 
 
 
 
 
 
 
                              }
                         
if(millis()%4000>=2000){
      ReadPH();
    lcd.setCursor(0,0);
    lcd.print("Calibrated        ");
                         
                         
      lcd.setCursor(0,1);
      lcd.print("PH:                      ");
      lcd.setCursor(3,1);
      lcd.print(phValue);
      lcd.setCursor(8,1);
      lcd.print("K:");
      lcd.setCursor(11,1);
      lcd.print(Kn);
                         
                              }
else{
                         
      lcd.setCursor(0,0);
      lcd.print("Select To Save      ");                 
      lcd.setCursor(0,1);
      lcd.print("Down to Exit          ");
                              };
                         
                           
                              }
 
 
};
 
 
//******************************* LOGS Min/MAX Values*******************************//
                          void Log_Min_MaxTemp(){
                       
                     
                            if(Temperature>=MaxT) MaxT=Temperature;
                            if(Temperature<=MinT) MinT=Temperature;
                                           
                                             
                          };
 
 
//******************************* LOGS Min/MAX Values*******************************//
                          void Log_Min_MaxPH(){
                       
                     
                            if(phValue>=MaxPH) MaxPH=phValue;
                            if(phValue<=MinPH) MinPH=phValue;
                                           
                                             
                          };
 
 
 
 
 
 
void PrintReadings(){
           
                Serial.print("pH: ");
                Serial.print(phValue);
                Serial.print(Temperature);
                Serial.print(" *C  ");
 
                                      //** First Screen Shows Temp and EC **//
                                      if(Screen==1){
                                      lcd.setCursor(0,0);
                                      lcd.print("Arduino pH  ");
                                      lcd.setCursor(0,1);
                                      lcd.print("pH:              ");
                                      lcd.setCursor(3,1);
                                      lcd.print(phValue);
                                      lcd.setCursor(9,1);
                                      lcd.print(Temperature);
                                      lcd.print("'C");
                                      }
                                 
                                 
                                      //**Third Screen Shows Min and Max **//
                                      else if(Screen==2){
                                      lcd.setCursor(0,0);
                                      lcd.print("Min:              ");
                                      lcd.setCursor(4,0);
                                      lcd.print(MinPH);
                                      lcd.setCursor(9,0);
                                      lcd.print(MinT);
                                      lcd.print("'C");
                                      lcd.setCursor(0,1);
                                      lcd.print("Max:              ");
                                      lcd.setCursor(4,1);
                                      lcd.print(MaxPH);
                                      lcd.setCursor(9,1);
                                      lcd.print(MaxT);
                                      lcd.print("'C");
                                      }
                                 
                                 
                                      else if(Screen==3){
                               
                                      lcd.setCursor(0,0);
                                      lcd.print("Uptime Counter:              ");
                                 
                                      lcd.setCursor(0,1);
                                      lcd.print("                                    ");//Clearing LCD
                                      lcd.setCursor(0,1);
                                      lcd.print(Day);
                                      lcd.setCursor(3,1);
                                      lcd.print("Day");
                                      lcd.setCursor(8,1);
                                      lcd.print(Hour);
                                      lcd.setCursor(10,1);
                                      lcd.print(":");
                                      lcd.setCursor(11,1);
                                      lcd.print(Minute);
                                      lcd.setCursor(13,1);
                                      lcd.print(":");
                                      lcd.setCursor(14,1);
                                      lcd.print(Second);
                                 
                                 
                                      }
                   
                                      else if(Screen==4){
                                   
                                      lcd.setCursor(0,0);
                                      lcd.print("Calibrate pH          ");
                                 
                                 
                                      lcd.setCursor(0,1);
                                      lcd.print("Hold Select            ");
                               
                                      }
       
 
 
};
