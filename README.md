# Aquariumatic
Code repository for a Pi-Arduino Aquarium Management system, by Liam O'Reilly

To Address - Pi
Install
VNC Server - for desktop access over wifi Possibly not required; will run headless once complete
Python script to monitor web page for user input and will send input to the Arduinos for processing
rc.local - run the server.py script on startup. On client versions also run a pull from github before running script to ensure most up to date code running.

Python libraries required:
Tornado - for serving web-based GUI
i2c - for sending commands to Arduino Mega (i2c slave) and a 16x2 LCD display (also i2c Slave)

To Address - Arduino Mega
i2c slave. 
Arduino will receive a set of temperature and pH ranges from the Pi via i2c and will save to EEPROM.
Will then monitor the temp and pH sensor input, displaying on the LCD display.
If temp strays outside of range the heaters (on the relay board) will be triggered
If pH strays outside of range an alert will be sent to the Pi

Attached devices
16x2 LCD display (i2c Slave)
8 Channel Relay Board (connected to Arduino Mega)
DS18B20 Digital Thermal Probe (Connected via OneWire to Arudino)
pH Analog Meter Kit (Connected to Arduino)
