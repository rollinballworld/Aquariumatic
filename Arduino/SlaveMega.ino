#include <Wire.h>

char x = "";

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany)
{
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

void setup() {
  // setup relay pins here:

  Wire.begin(15);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}

void loop(){
  //Check ph and Temp here
}

void Heating(string state){
 //handle heating relays 
}

void Lighting(int light){
 //handle light relays 
}
