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
  
def main():
  #for each address in addreslist:
    getValues(address)
    
    
