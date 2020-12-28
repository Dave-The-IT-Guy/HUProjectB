import RPi.GPIO as GPIO
import time
import threading

#Thread variable
stop_threads = False

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

sr04_trig = 20
sr04_echo = 21

GPIO.setup(sr04_trig, GPIO.OUT)
GPIO.setup(sr04_echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def sr04():
    # send trigger pulse
    GPIO.output(sr04_trig, GPIO.HIGH)
    time.sleep(0.000001)
    GPIO.output(sr04_trig, GPIO.LOW)

    # wait for echo high and remember its start time
    while True:
        if (GPIO.input(sr04_echo)):
            begintijd = time.time()
            break
    # wait for echo low and remember its end time
    while True:
        if not (GPIO.input(sr04_echo)):
            eindtijd = time.time()
            break

    # calculate and return distance
    tijd = eindtijd - begintijd
    afstand = tijd * 34300
    return (afstand / 2)

def afstand(stop):
    while True:
        if not stop:
            afstand = sr04()
            if afstand < 20:
                return ("TRUE")
        else:
            return ("STOPPED")

#Defineer de thread
t1 = threading.Thread(target=afstand, args=(lambda: stop_threads,))
#Start de thread
t1.start()


try:
    while True:
        time.sleep(0.5)
except:
    print("expected")
    stop_threads = True
    t1.join()