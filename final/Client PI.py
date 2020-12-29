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

#Voor de verbinding met de server
con = "PYRO:steam.functions@192.168.192.24:9090"

def send_wave():
    rem = Pyro5.api.Proxy(con)
    while True:
        if (GPIO.input(switch)):
            rem.recieve_wave()
            time.sleep(4.18)

def send_beep():
    rem = Pyro5.api.Proxy(con)
    while True:
        if (GPIO.input(switch2)):
            rem.recieve_beep()
            time.sleep(0.1)

#Meet de afstand tussen gebruiker en sensor
def sr04():
    # send trigger pulse
    GPIO.output(sr04_trig, GPIO.HIGH)
    time.sleep(0.000001)
    GPIO.output(sr04_trig, GPIO.LOW)

    # wait for echo high and remember its start time
    while True:
        if (GPIO.input(sr04_echo)):
            starttime = time.time()
            break
    # wait for echo low and remember its end time
    while True:
        if not (GPIO.input(sr04_echo)):
            endtime = time.time()
            break

    # calculate and return distance
    tijd = endtime - starttime
    afstand = tijd * 34300 #Snelheid van geluid in seconden
    return (afstand / 2)

def send_sr04():
    rem = Pyro5.api.Proxy(con)
    while True:
        if sr04() < 20:
            for i in range(1, 6):
                time.sleep(1)
                dis = sr04()
                if i == 5:

                    for i in range(0, 5):
                        rem.change_neo(0, 0, 255)


#Thread voor het laten zien van het aantal users (schuifregister)
thread_send_wave = threading.Thread(target = send_wave, daemon = True).start()

thread_send_beep = threading.Thread(target = send_beep, daemon = True).start()

while True:
    time.sleep(10)