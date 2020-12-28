import RPi.GPIO as GPIO
import time

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

def afstand():
    afstand = sr04()
    if afstand < 20:
        return ("TRUE")


while True:
    print(afstand())
    time.sleep(0.5)