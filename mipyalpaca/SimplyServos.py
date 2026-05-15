# Pico Kitronik Simply Servos 
# Uses the PIO state machines to drive a servo.
# This is the Micro Python version. 
from machine import Pin, PWM

class KitronikSimplyServos:
    #simply stops and starts the servo PIO, so the pin could be used for something else.
    def registerServo(self, servo):
        servo -= 1
        self.servos[servo] = PWM(Pin(self.servoPins[servo]))
        self.servos[servo].freq(50)
        self.goToPosition(servo, self.maxDegrees // 2)

    def deregisterServo(self, servo):
        servo -= 1
        self.servos[servo].deinit()
 
    def scale(self, value, fromMin, fromMax, toMin, toMax):
        return toMin + ((value - fromMin) * ((toMax - toMin) / (fromMax - fromMin)))

    # goToPosition takes a degree position for the servo to goto. 
    # 0degrees->maxDegrees degrees is 0->2000us, plus offset of 500uS
    # This function does the sum then calls goToPeriod to actually poke the PIO 
    def goToPosition(self, servo, degrees):
        if degrees < 0:
            degrees = 0
        if degrees > self.maxDegrees:
            degrees = self.maxDegrees
        scaledValue = self.scale(degrees, 0, self.maxDegrees, 1638, 8192)
        servo -= 1
        self.servos[servo].duty_u16(int(scaledValue))
    
    def goToPeriod(self, servo, period):
        if period < 500:
            period = 500
        if period > 2500:
            period = 2500
        scaledValue = self.scale(period, 500, 2500, 1638, 8192)
        servo -= 1
        self.servos[servo].duty_u16(int(scaledValue))

    #Class initialisation
    #defaults to the standard pins and freq for the kitronik board, but could be overridden
    def __init__(self, numberOfServos=8, maxDegrees=180):
        self.maxDegrees = maxDegrees
        self.servoPins = [2,3,4,5,6,7,8,9]
        self.servos = [PWM(Pin(pin)) for pin in range(numberOfServos)]
        #connect the servos by default on construction - advanced uses can disconnect them if required.
        for i in range(numberOfServos):
            self.registerServo(i + 1)
