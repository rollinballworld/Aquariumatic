import RPi.GPIO as GPIO

class PiRelay:
    def __init__(self, PinNo):
        self.PinNo = PinNo
        #setup GPIO using Board numbering
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PinNo, GPIO.OUT)
        GPIO.output(PinNo, False)

    def On(self):
        #self.PinNo = PinNo
        GPIO.output(self.PinNo, True)
        print("Relay " + str(self.PinNo) + " On")

    def Off(self):
        #self.PinNo = PinNo
        GPIO.output(self.PinNo, False)
        print("Relay " + str(self.PinNo) + " Off")

    def Finish(self):
        GPIO.cleanup()
        print "GPIO exited cleanly"


class i2c:
    def __init__(self):
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

    def getValues(self, address):
        # request values from i2c address provided and write it to csv file
        return values
  
    def RetrieveData(self, address):
        #read last line of [address].csv
        #use this data to populate the web page
