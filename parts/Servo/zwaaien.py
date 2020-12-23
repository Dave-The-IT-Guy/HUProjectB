#Source: https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/
#source: https://makersportal.com/blog/2020/3/21/raspberry-pi-servo-panning-camera
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

#Pinnen
switch = 23
servo = 25

GPIO.setup(servo, GPIO.OUT)
GPIO.setup( switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )


def zwaaien(pin_nr, position):
    position = round(((10 / 100) * position) + 2, 2)
    pwm = GPIO.PWM(pin_nr, 50)  # 50 Hz (20 ms PWM period)
    print(position)
    pwm.start(position)
    time.sleep(0.02)

#Initaliseren
zwaaien(servo, 80)

def zwaai_toggle():
    while True:
        if (GPIO.input(switch)):
            for x in range(0, 5):
                zwaaien(servo, 20)
                time.sleep(0.4)
                zwaaien(servo, 80)
                time.sleep(0.4)

zwaai_toggle()

GPIO.cleanup() # good practice when finished using a pin