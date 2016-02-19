# Aquariumatic
Code repository for a Pi-Arduino Aquarium Management system, by Liam O'Reilly




To Do

server.py
Look at integrating a static handler for the js, css and images folders in templates. Something like:
(r"/js/(.*)", web.StaticFileHandler, {"path": "/var/www"})
OR - move all to static directory and amend aquariumatic.html accordingly

tank.html
amend Ajax script and add in something to append the returned data from the server:
success: function(data)
{
    $('#results').append(
        '<p>Value one: '+data['result1']+'</p><p>Value 2: '+data['result2']+'</p>';
    );
}

data.py
create code to poll i2c devices and save their returned data as a csv file.
schedule this file to be ran every few minutes. The server can then read tank stats from this csv instead of direct request?
Test with direct requesting too.

functions.py
create functions for i2c sending data, receiving i2c data, emailing alerts via gmail, reading csv file.

aquariumatic.html
update links to static directory for js, css, images
integrate ajax used in tank.html; tweak to fit the provided html.

index.html
create a nice little splash page.
Later add ajax listing attached devices and a button to redirect to the tank settings (/aquarium1, /aquarium56 etc)



Arduino Mega
i2c slave. 
Arduino will receive a set of temperature and pH ranges from the Pi via i2c and will save to EEPROM.
Will then monitor the temp and pH sensor input, displaying on the LCD display.
If temp strays outside of range the heaters (on the relay board) will be triggered
If pH strays outside of range an alert will be sent to the Pi

Attached devices
16x2 LCD display (i2c Slave) - replace with normal wiring; arduino to control screen locally.
8 Channel Relay Board (connected to Arduino Mega)
DS18B20 Digital Thermal Probe (Connected via OneWire to Arduino)
pH Analog Meter Kit (Connected to Arduino)
