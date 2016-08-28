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