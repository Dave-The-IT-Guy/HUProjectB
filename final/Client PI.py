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
GPIO.setup(switch, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(switch2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#Beeper GPIO (normaal geluidssignaal maar in dit geval led)
speaker = 18
GPIO.setup(speaker, GPIO.OUT)

#Led GPIO (vriend niet aanwezig)
led = 4
GPIO.setup(led, GPIO.OUT)

#SR04 GPIO (afstandsmeter)
sr04_trig = 20
sr04_echo = 21
GPIO.setup(sr04_trig, GPIO.OUT)
GPIO.setup(sr04_echo, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#Stuurt de beeper aan
def beep():
    GPIO.output(speaker, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(speaker, GPIO.LOW)

#Stuurt de led aan
def light():
    GPIO.output(led, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led, GPIO.LOW)
    time.sleep(1)


#REMOTE FUNCTIONS

#Voor de verbinding met de server
con = "PYRO:steam.functions@192.168.192.24:9090"

def send_wave():
    rem = Pyro5.api.Proxy(con)
    while True:
        if (GPIO.input(switch)):
            try:
                rem.recieve_wave()
                time.sleep(4)
            except:
                time.sleep(2)

def send_beep():
    rem = Pyro5.api.Proxy(con)
    while True:
        if (GPIO.input(switch2)):
            try:
                rem.recieve_beep()
            except:
                time.sleep(2)

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
        if sr04() > 20:
            try:
                rem.recieve_led()
                time.sleep(1.99)
            except:
                time.sleep(2)
        else:
            time.sleep(1)

@Pyro5.api.expose
class functions():

    # STUUR THREAD BEEPER
    def recieve_beep(self):
        threading.Thread(target=beep, daemon=True).start()

    # STUUR THREAD BEEPER
    def recieve_led(self):
        threading.Thread(target=light, daemon=True).start()


#THREADING
threading.Thread(target = send_wave, daemon = True).start()
threading.Thread(target = send_beep, daemon = True).start()
threading.Thread(target = send_sr04, daemon = True).start()

#NETWORKING
func = functions()
daemon = Pyro5.api.Daemon(host = "192.168.192.64", port = 9091)
Pyro5.api.Daemon.serveSimple(
    { func: "steam2.functions" },
    ns = False,
    daemon = daemon,
    verbose = True
)