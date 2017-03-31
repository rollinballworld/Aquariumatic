/*This sketch will:
Connect to a wifi network on startup
Start the serial connection to the Arduino
Request a data string from the Arduino (in json format)
Forward string via websocket connection

Check whether best to set up the websocket server on the Pi and have the ESP8266s connect to that, or 
whether to have the ESP8266s as the Socket servers and have the pi operate as the client.

Check out these sources:
https://github.com/morrissinger/ESP8266-Websocket/blob/master/examples/WebSocketClient_Demo/WebSocketClient_Demo.ino*/