#This script will contain functions for:
#Storing i2c device information (Table/csv file?)
#Sending data requests
#Receiving and processing data
#
#Create a class when functions are complete

from time import sleep
import smbus

def i2cDevices():
  print("Scanning")
    bus = smbus.SMBus(1) # 1 indicates /dev/i2c-1; use 0 if not working
    found_slaves = []
    for device in range(128):
      try: #If you try to read and it answers, it's there
         bus.read_byte(device)
      except IOError: 
         pass
      else:
         found_slaves.append(str(hex(device)))
    device_count = len(found_slaves)
    if device_count == 0:
      print("No Aquariumatic slave devices found")
      sleep(2)
    else:
      return found_slaves

def getValues(address):
  # request values from i2c address provided and write it to csv file
  return values
  
def RetrieveData(address):
  #read last line of [address].csv
  #use this data to populate the web page
  
def main(): #to automate and run every few minutes - use a cron job?
  for each address in i2clist():
    ToWrite = getValues(address)
    #Then write values to a csv file called [address].csv
    writevalues(address, ToWrite)
    
