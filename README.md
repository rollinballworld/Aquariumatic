# Aquariumatic
Code repository for a Pi-Arduino Aquarium Management system, by Liam O'Reilly


# To Do

data.py
create code to poll i2c devices and save their returned data as a csv file.
schedule this file to be ran every few minutes. The server can then read tank stats from this csv instead of direct request?
This will be integrated after the deviceis up and running using direct requesting between the aquarium class and the arduino.

aquarium.py
complete the serial communication elements in each of the functions.
Once working with a serial connection complete the i2c coding.


index.html
create a nice little splash page.
Later add ajax listing attached devices and a button to redirect to the tank settings (/tank1, /tank56 etc)

aquariumatic.html
restructure to work with the code of tank.html

Arduino Mega
i2c slave. 
Arduino will receive a set of temperature and pH ranges from the Pi via i2c and will save to EEPROM.
Will then monitor the temp and pH sensor input, displaying on the LCD display.
If temp strays outside of range the heaters (on the relay board) will be triggered
If pH strays outside of range an alert will be sent to the Pi

Arduino - Attached devices
16x2 LCD display
4 Channel Relay Board
DS18B20 Digital Thermal Probe (Connected via OneWire)
pH Analog Meter Kit
