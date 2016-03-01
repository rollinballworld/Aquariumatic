#include <Wire.h>
//include OneWire for temp probe
//include library for pH probe
//include library for lcd screen

char x = "";

/* Define all pins here for relays, probes and screen*/


void setup() {
  // setup relay pins as outputs here:
  //setup screen pins here
  //setup probe pins

  Wire.begin(10);                // join i2c bus with slave address #10
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}

void loop(){
  //Check ph
  //check temp
  //write to screen
  //check for incoming i2c commands
}

void Heating(string state){
 //handle heating relays 
}

void Lighting(int light){
 //handle light relays 
}


void receiveEvent(int howMany)
{
  // function that executes whenever data is received from master
  // this function is registered as an event, see setup()
  x = "";
  while( Wire.available()){
    x += (char)Wire.read();
  }
  do_command(x);
}

void requestEvent()
{
  //Return temp and pH Readings as a char
  //Collect data as a string then convert using c_str
  Wire.write(data.c_str());
}

void do_command(char x) {
  switch(x) {
    case 'HeatingOn': Heating("On"); break;
    case 'HeatingOff': Heating("Off"); break;
    case 'Lighting1': Lighting(1); break;
    case 'Lighting2': Lighting(2); break;
    case 'Lighting3': Lighting(3); break;
    default: break;
  }
}
