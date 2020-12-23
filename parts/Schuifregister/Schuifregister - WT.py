import RPi.GPIO as GPIO
import time
import threading

#Thread variable
stop_threads = False

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( 0 )

shift_clock_pin = 5
latch_clock_pin = 6
data_pin = 13

GPIO.setup( shift_clock_pin, GPIO.OUT )
GPIO.setup( latch_clock_pin, GPIO.OUT )
GPIO.setup( data_pin, GPIO.OUT )

def users_tonen(byte):

    #Voer de nieuwe data in
    for bit in byte:
        GPIO.output(latch_clock_pin, GPIO.HIGH)
        GPIO.output(latch_clock_pin, GPIO.LOW)

        if bit == 1:
            GPIO.output(data_pin, GPIO.HIGH)
        else:
            GPIO.output(data_pin, GPIO.LOW)

        GPIO.output(shift_clock_pin, GPIO.HIGH)
        GPIO.output(shift_clock_pin, GPIO.LOW)

    #Hij moet eentje verder geduwd worden anders kloppen de ledjes niet
    GPIO.output(latch_clock_pin, GPIO.HIGH)
    GPIO.output(latch_clock_pin, GPIO.LOW)
    GPIO.output(data_pin, GPIO.LOW)
    GPIO.output(shift_clock_pin, GPIO.HIGH)
    GPIO.output(shift_clock_pin, GPIO.LOW)

def aantal_users(stop):
    users = 0
    while True:

            try:
                users_old = users
                # Lees het aantal gebruikers uit een file
                with open("users.txt") as file:
                    users = int(file.readline())
                if users != users_old:

                    #Zet het aantal users om naar bytes voor het schuifregister
                    bytes = []
                    for i in range(0, 8):
                        bytes.append(0)
                    for i in range(0, users):
                        bytes[i] = 1
                    users_tonen(bytes)

                elif stop():
                    for i in range(0, 8):
                        bytes.append(0)
                    users_tonen(bytes)
                    return
            except:
                print("Out of range")

            time.sleep(1)

#Defineer de thread
t1 = threading.Thread(target=aantal_users, args=(lambda: stop_threads,))
#Start de thread
t1.start()

try:
    while True:
        print("something")
        time.sleep(1)
except:
    print("expected")
    stop_threads = True
    t1.join()