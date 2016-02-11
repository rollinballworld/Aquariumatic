#This script will contain functions for polling the i2c data and
#writing it to a table or a csv file
#
#This will be scheduled to run on a Cron job every x minutes, and the server script can then retrieve values from the csv files.
#Allows the page to use the values independently of Arduinos.

def i2cList():
  #compile a list of i2c addresses to query
  return addresslist
  

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
    
    
