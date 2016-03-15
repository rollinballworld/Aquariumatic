#To replace the functions and data python scripts.
#Create and aquarium class which gathers the current sonsor data from the tank's 
#arduino (ID nubmer to be provided, i2c address to be found)
#
#add functions to deal with sending commands to the arduino, sending parameters, receiving alerts and receiving data.

class Aquarium(AquariumNumber):
  """
  This class is to contain all of the Aquarium-based function for ease of use in the main script.
  The main script can create an instance for a tank (for example Tank1=Aquarium(1) )
  This can then set up the basics for the tank such as locating it's i2c address etc.
  This will allow short and simple sending of data:
  Tank1.SendCommand("test","")
  or requesting data from the tank
  CurrentpHValue = Tank1.CurrentReading("pH")
  CurrentTempValue = Tank1.CurrentReading("Temp")
  
  One day. One day...
  """
  def __init__(self, TankNo):
    self.TankNo = TankNo

  def SendCommand(FunctionName, FunctionValue):
    #Send AquariumNumber to i2cList to have the i2c address returned
    AqAddress=i2cList(self.TankNo)
    #Send FunctionName & FunctionValue to the returned i2c Address
    if FunctionName == 'test':
      #Setup a test return value
      print("Test Script receipt")
    else:
      #Run normal i2c send to - TO WRITE
      pass
    
  def SendParameter(FunctionName, MinValue, MaxValue):
    #Send AquariumNumber to i2cList to have the i2c address returned
    AqAddress=i2cList(self.TankNo)
    #Send FunctionName & FunctionValue to the returned i2c Address
    if FunctionName == 'test':
      #Setup a test return value
      print("Test Script receipt")
    else:
      #Run normal i2c send to - TO WRITE
      pass
    
  def CurrentReading:
    CurrentReading[]
    #write function to:
    #send via serial command for data
    #compile an array of returned data
    #return array
    pass
  
  def CheckAlerts:
    pass


def i2cList(AquariumNumber):
  #Contain a list of i2c addresses and return the appropriate address when provided with an Aquarium number
  #TO WRITE
  ListedValue = 0x10
  return ListedValue

def Gmail(recipient, subject, body):
    import smtplib

    gmail_user = "aquariumatic@gmail.com"
    gmail_pwd = "pw"
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"
