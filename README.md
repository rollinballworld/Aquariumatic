# Aquariumatic
Code repository for a Pi-Arduino Aquarium Management system, by Liam O'Reilly

To Address - Pi
Install
VNC Server - for desktop access over wifi

Python libraries required:
Tornado - for serving web-based GUI
i2c - for sending commands to Arduino Mega (i2c slave) and a 16x2 LCD display (also i2c Slave)


To Address - Arduino Mega
i2c slave. 
Send data to Pi for monitoring.
Monitor incoming data and process commands and changes.

Attached devices
16x2 LCD display (i2c Slave)
8 Channel Relay Board (connected to Arduino Mega)
DS18B20 Digital Thermal Probe (Connected via OneWire to Arudino)
pH Analog Meter Kit (Connected to Arduino)
