#Source: https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/
#source: https://makersportal.com/blog/2020/3/21/raspberry-pi-servo-panning-camera
import RPi.GPIO as GPIO
import time
import threading

#GPIO opzetten
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

#Pinnen
zwaai_knop = 23
servo = 25

#Thread variable
stop_threads = False

#GPIO opzetten
GPIO.setup(servo, GPIO.OUT)
GPIO.setup( zwaai_knop, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

#Vertaalt het zwaaicommando naar bewegingen van de servo
def zwaaien(pin_nr, position):
    #Bepaald de positie die de servo aannemen gaat
    position = round(((10 / 100) * position) + 2, 2)
    #Maakt de servo klaar voor gebruik
    pwm = GPIO.PWM(pin_nr, 50)  # 50 Hz (20 ms PWM period)
    print(position)
    #Verplaatst de servo
    pwm.start(position)
    #De wachttijd voordat er weer aan commando gestuurd worden kan
    time.sleep(0.02)

#Startpositie van de servo
zwaaien(servo, 80)

def zwaai_toggle():
    while True:
        if (GPIO.input(zwaai_knop)):
            for x in range(0, 5):
                zwaaien(servo, 20)
                time.sleep(0.4)
                zwaaien(servo, 80)
                time.sleep(0.4)

#Defineer de thread
t1 = threading.Thread(target=zwaai_toggle, daemon = True)
#Start de thread
t1.start()

while True:
    time.sleep(100)

GPIO.cleanup() # good practice when finished using a pin