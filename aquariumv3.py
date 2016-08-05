#To replace aquarium.py
#Once complete name aquarium.py aquariumSerial, and this aquariumI2C
#The v3 Aquariumatic looks to combine the webserver and slave modules (Pi & Arduino respectively) into one module.
#This will be done by having the pH and temp sensors, relay board and lcd(now i2c) controlled by the Pi.
#If the webserver receives a request for /aq1 it shall refer to the GPIO based setup; /aq2+ will be directed to the i2c bus.
#ToAdd:
#Add function for i2c mapping (def SlaveList); an array to save the tank numbers and their slave addresses.

import serial, time, sys

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
  """
  #define serial port. Try Windows COM port first.
  #On Error try Linux Port
  if sys.platform == 'win32':
    locations=['\\\\.\\COM12']
    for device in locations:
        try:
            ser = serial.Serial(port = device,baudrate = 115200, timeout=5)
        except:
            print("Failed to connect on",device)
            time.sleep(3)
  elif sys.platform == 'linux':
    #for RPI version 1, use "bus = smbus.SMBus(0)"
    import smbus
    bus = smbus.SMBus(1)
  elif sys.platform == 'linux2':
    #for RPI version 1, use "bus = smbus.SMBus(0)"
    import smbus
    bus = smbus.SMBus(1)
  else:
    print('Unrecognised platform. Please contact Craig for updates.')
    

  def __init__(self, TankNo):
    self.TankNo = TankNo
    
  def SendCommand(self, TankNo, FunctionName, FunctionValue):
    #Send AquariumNumber to i2cList to have the i2c address returned
    #AqAddress=SlaveList(self.TankNo)
    #Send FunctionName & FunctionValue to the returned i2c Address
    ser=self.ser
    
    if FunctionName == 'test':
      #Setup a test return value
      print("Test Script receipt")
    else:
      if TankNo == 0:
        #/tank0 is the debug page, so return default values
      elif TankNo == 1:
        #/tank1 uses onboard sensors
      else:
        #Tanks numbered 2 upwards are i2c slaves; to write
        ser.flushInput()
        ToSend = FunctionName + FunctionValue
        ser.write(ToSend.encode('UTF-8'))
        time.sleep(.1)
        #ser.close
        print(ToSend +' Command Sent')
        return

  def CurrentStatus(self, TankNo):
    if TankNo == 0:
      #/tank0 is the debug page, so return default values
      FakeInput= "{\"Temp\": \"" + String(CurrentTemp()) + "\", ";
      json = json + "\"pH\": \"" + CurrentpH() + "\", ";
      json = json + "\"Lights\": \"" + Lights("check") + "\", ";
      json = json + "\"Pump\": \"" + Pump("check") + "\", ";
      json = json + "\"Heating\": \"" + Heating("check") + "\", ";
      json = json + "\"AqStatus\": \"" + "Healthy" + "\", ";
      json = json + "\"msg\": \"" + "Update Received" + "\"}";
      #return str(FakeInput)[1:]
    elif TankNo == 1:
      #/tank1 uses onboard sensors - TO WRITE
      ser=self.ser
      ser.flushInput()
      ser.write('CurrentStatus'.encode('UTF-8'))
      Received=ser.readline().rstrip()
      return str(Received)[1:]
    else:
      ser=self.ser
      ser.flushInput()
      ser.write('CurrentStatus'.encode('UTF-8'))
      Received=ser.readline().rstrip()
      return str(Received)[1:]
    
  def SendParameter(self, NewMinTemp, NewMaxTemp, NewMinpH, NewMaxpH):
    #Send AquariumNumber to i2cList to have the i2c address returned
    #AqAddress=i2cList(self.TankNo)
    ser=self.ser
    #ser.flushInput()
    #ser.flushOutput()
    #Send FunctionName & FunctionValue to the returned i2c Address
    if NewMinTemp == 'test':
      #Setup a test return value
      print("Test Script receipt")
    else:
      #Run normal i2c send to - TO WRITE
      ser.write('Parameters'.encode('UTF-8'))
      time.sleep(.1)
      ser.write(str(NewMinTemp).encode('UTF-8'))
      ser.write(str(NewMaxTemp).encode('UTF-8'))
      ser.write(str(NewMinpH).encode('UTF-8'))
      ser.write(str(NewMaxpH).encode('UTF-8'))
      #ser.close
      print('Parameters Sent')
      return
    
  def CurrentReading(self, requested):
    ser=self.ser
    #ser.flushInput()
    #ser.flushOutput()
    #CurrentReading[]
    ToSend = 'Current' + requested
    ser.write(ToSend.encode('UTF-8'))
    time.sleep(2)
    ToReturn = ser.readline()
    return str(ToReturn)
    #ser.close
    
  def CheckAlerts(self):
    ser=self.ser
    pass
  
  def ResetSlave(self):
    ser=self.ser
    ToSend = 'ResetSlave'
    ser.write(ToSend.encode('UTF-8'))    
    ser.close

  def CloseSerial(self):
    ser=self.ser
    ser.close

def SlaveList(self, AquariumNumber):
  #Contain a list of i2c addresses and return the appropriate address when provided with an Aquarium number
  #TO WRITE
  ListedValue = 0x10
  return ListedValue


def SendEmail(recipient, subject, body):
    import smtplib

    user = "craighissett@gmail.com"

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
