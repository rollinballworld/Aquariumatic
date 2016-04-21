#This script will contain functions for polling the i2c data and
#writing it to a table or a csv file
#
#This will be scheduled to run on a Cron job every x minutes, and the server script can then retrieve values from the csv files.
#Allows the page to use the values independently of Arduinos.
from time import sleep
import smbus

def i2cList():
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
    
