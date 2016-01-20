#This will contain all functions required to send data to ad from the Arduinos attached via i2c.
#import the i2c libraries
#
#


def SlaveButtonSend(AquariumNumber, FunctionName, FunctionValue):
  #Send AquariumNumber to i2cList to have the i2c address returned
  AqAddress=i2cList(AquariumNumber)
  #Send FunctionName & FunctionValue to the returned i2c Address
  if FunctionName == 'test':
    #Setup a test return value
    print("Test Script receipt")
  else:
    #Run normal i2c send to - TO WRITE
  

def SlaveParameterSend(AquariumNumber, FunctionName, MinValue, MaxValue):
  #Send AquariumNumber to i2cList to have the i2c address returned
  AqAddress=i2cList(AquariumNumber)
  #Send FunctionName & FunctionValue to the returned i2c Address
  if FunctionName == 'test':
    #Setup a test return value
    print("Test Script receipt")
  else:
    #Run normal i2c send to - TO WRITE


def i2cList(AquariumNumber):
  #Contain a list of i2c addresses and return the appropriate address when provided with an Aquarium number
  #TO WRITE
  ListedValue = 0x15
  return ListedValue
