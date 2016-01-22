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

def Gmail(recipient, subject, body):
    import smtplib

    gmail_user = "aquariumatic@gmail.com"
    gmail_pwd = "Craigisprettyclever"
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
  
