import RPi.GPIO as GPIO
import threading
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
            GPIO.output(speaker, GPIO.HIGH)
            GPIO.output(speaker, GPIO.LOW)

#Defineer de thread
t1 = threading.Thread(target=signaal, daemon = True)
#Start de thread
t1.start()

while True:
    print("test")
    time.sleep(1)