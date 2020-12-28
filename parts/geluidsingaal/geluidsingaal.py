import RPi.GPIO as GPIO
import time

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( 0 )

speaker = 18
switch2 = 24
GPIO.setup( switch2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
GPIO.setup( speaker, GPIO.OUT )


def signaal():
    while True:
        if (GPIO.input(switch2)):
            #Stuur beep naar andere machine.
            pass

def beep():
    GPIO.output(speaker, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(speaker, GPIO.LOW)

signaal()