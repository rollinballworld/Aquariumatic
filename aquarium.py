#To replace the functions and data python scripts.
#Create and aquarium class which gathers the current sonsor data from the tank's 
#arduino (ID nubmer to be provided, i2c address to be found)
#
#add functions to deal with sending commands to the arduino, sending parameters, receiving alerts and receiving data.

class Aquarium(TankID):
  #To fill out

  def SendCommand:
    pass
  
  def SendParameter:
    pass
    
  def CurrentReadings:
    CurrentReadings[]
    #write function to:
    #send via serial command for data
    #compile an array of returned data
    #return array
    pass
  
  def CheckAlerts:
    pass
