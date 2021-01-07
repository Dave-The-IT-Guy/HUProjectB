import RPi.GPIO as GPIO
import time
GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( 0 )

register_shift_clock_pin = 5
register_latch_clock_pin = 6
register_data_pin = 13

GPIO.setup( register_shift_clock_pin, GPIO.OUT )
GPIO.setup( register_latch_clock_pin, GPIO.OUT )
GPIO.setup( register_data_pin, GPIO.OUT )

def show_users(byte):

    #Voer de nieuwe data in
    for bit in byte:
        GPIO.output(register_latch_clock_pin, GPIO.HIGH)
        GPIO.output(register_latch_clock_pin, GPIO.LOW)

        if bit == 1:
            GPIO.output(register_data_pin, GPIO.HIGH)
        else:
            GPIO.output(register_data_pin, GPIO.LOW)

        GPIO.output(register_shift_clock_pin, GPIO.HIGH)
        GPIO.output(register_shift_clock_pin, GPIO.LOW)

    #Hij moet eentje verder geduwd worden anders kloppen de ledjes niet
    GPIO.output(register_latch_clock_pin, GPIO.HIGH)
    GPIO.output(register_latch_clock_pin, GPIO.LOW)
    GPIO.output(register_data_pin, GPIO.LOW)
    GPIO.output(register_shift_clock_pin, GPIO.HIGH)
    GPIO.output(register_shift_clock_pin, GPIO.LOW)

def users():
    users = 0
    while True:
        users_old = users
        #Lees het aantal gebruikers uit een file
        with open("users.txt") as file:
            users = int(file.readline())
        if users != users_old:
            try:
                #Zet het aantal users om naar bytes voor het schuifregister
                bytes = []
                for i in range(0, 8):
                    bytes.append(0)
                for i in range(0, users):
                    bytes[i] = 1
                show_users(bytes)
            except:
                print("Out of range")
        time.sleep(1)

users()