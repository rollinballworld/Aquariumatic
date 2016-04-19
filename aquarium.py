# for RPI version 1, use "bus = smbus.SMBus(0)"
#bus = smbus.SMBus(1)
import serial
#To replace the functions and data python scripts.
#Create and aquarium class which gathers the current sonsor data from the tank's 
#arduino (ID nubmer to be provided, i2c address to be found)
#
#add functions to deal with sending commands to the arduino, sending parameters, receiving alerts and receiving data.

class Aquarium():
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
  #define serial port. Try Windows COM port first.
  #On Error try Linux Port
  try:
    ser = serial.Serial(port = '\\\\.\\COM10',baudrate = 9600)
  except:
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate = 9600)

  def __init__(self, TankNo):
    self.TankNo = TankNo
    
  def SendCommand(self, FunctionName, FunctionValue):
    #Send AquariumNumber to i2cList to have the i2c address returned
    #AqAddress=i2cList(self.TankNo)
    #Send FunctionName & FunctionValue to the returned i2c Address
    ser=self.ser
    if FunctionName == 'test':
      #Setup a test return value
      print("Test Script receipt")
    else:
      #Run normal i2c send to - TO WRITE
      ToSend = FunctionName + FunctionValue
      ser.write(ToSend.encode('UTF-8'))
      ser.close
      print('Command Sent')
      #pass
    
  def SendParameter(self, NewMinTemp, NewMaxTemp, NewMinpH, NewMaxpH):
    #Send AquariumNumber to i2cList to have the i2c address returned
    #AqAddress=i2cList(self.TankNo)
    ser=self.ser
    #Send FunctionName & FunctionValue to the returned i2c Address
    if NewMinTemp == 'test':
      #Setup a test return value
      print("Test Script receipt")
    else:
      #Run normal i2c send to - TO WRITE
      ser.write('Parameters'.encode('UTF-8'))
      ser.write(str(NewMinTemp).encode('UTF-8'))
      ser.write(str(NewMaxTemp).encode('UTF-8'))
      ser.write(str(NewMinpH).encode('UTF-8'))
      ser.write(str(NewMaxpH).encode('UTF-8'))
      ser.close
      print('Parameters Sent')
      #pass
    
  def CurrentReading(self, requested):
    ser=self.ser
    #CurrentReading[]
    ToSend = 'Current' + requested
    ser.write(ToSend.encode('UTF-8'))
    CurrentValue = ser.readline()
    return str(CurrentValue)
    pass
  
  def CheckAlerts(self):
    ser=self.ser
    pass


def i2cList(self, AquariumNumber):
  #Contain a list of i2c addresses and return the appropriate address when provided with an Aquarium number
  #TO WRITE
  ListedValue = 0x10
  return ListedValue


def SendEmail(self, recipient, subject, body):
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
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")
