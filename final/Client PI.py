import threading
import Pyro5.api
import RPi.GPIO as GPIO
import time

#Klaarmaken van de GPIO's
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

#Switches GPIO (knoppen)
switch = 23
switch2 = 24
GPIO.setup( switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
GPIO.setup( switch2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

#Beeper GPIO (normaal geluidssignaal maar in dit geval led)
speaker = 18
GPIO.setup( speaker, GPIO.OUT )

#SR04 GPIO (afstandsmeter)
sr04_trig = 20
sr04_echo = 21
GPIO.setup(sr04_trig, GPIO.OUT)
GPIO.setup(sr04_echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Maak verbinding met de server
rem = Pyro5.api.Proxy("PYRO:steam.functions@192.168.192.24:9090")

while True:
    if (GPIO.input(switch)):
        rem.recieve_wave()
        time.sleep(4.18)