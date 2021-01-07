import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

clock_pin = 19
data_pin = 26

GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(data_pin, GPIO.OUT)


def apa102_send_bytes(clock_pin, data_pin, bytes):
    for byte in bytes:
        for bit in byte:
            if bit % 2 == 1:
                GPIO.output(data_pin, GPIO.HIGH)
            else:
                GPIO.output(data_pin, GPIO.LOW)
            GPIO.output(clock_pin, GPIO.HIGH)
            GPIO.output(clock_pin, GPIO.LOW)


def to_binary(value):
    # Colorcode to binary
    binair = []
    for x in range(0, 8):
        if value % 2 == 1:
            binair.append(1)
        else:
            binair.append(0)
        value = value // 2
    binair.reverse()
    return (binair)


def apa102(color):

    #Begin pakket
    apa102_send_bytes(clock_pin, data_pin, [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])

    #Stuur de kleuren
    counter = 0
    for i in color:
        binary = to_binary(i)
        if counter == 0:
            blue = binary
        elif counter == 1:
            green  = binary
        elif counter == 2:
            red = binary
        else:
            counter = 0
        counter += 1
    for x in range(0, 8):
        apa102_send_bytes(clock_pin, data_pin, [[1, 1, 1, 0, 0, 0, 0, 1], blue, green, red])
    #Stuur het eindpakket
    apa102_send_bytes(clock_pin, data_pin, [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]])

rgb = (1, 1, 1)
apa102((rgb))