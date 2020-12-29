import threading
import Pyro5.api
import RPi.GPIO as GPIO
import time

#Klaarmaken van de GPIO's
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

#NEOpixel GPIO (ledstrip)
neo_clock_pin = 19
neo_data_pin = 26
GPIO.setup(neo_clock_pin, GPIO.OUT)
GPIO.setup(neo_data_pin, GPIO.OUT)

#Servo GPIO (zwaaien)
servo = 25
GPIO.setup(servo, GPIO.OUT)

#Switches GPIO (knoppen)
switch = 23
switch2 = 24
GPIO.setup( switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
GPIO.setup( switch2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

#Beeper GPIO (geluidssignaal)
speaker = 18
GPIO.setup( speaker, GPIO.OUT )

#Schuifregister (aantal users)
register_shift_clock_pin = 5
register_latch_clock_pin = 6
register_data_pin = 13
GPIO.setup( register_shift_clock_pin, GPIO.OUT )
GPIO.setup( register_latch_clock_pin, GPIO.OUT )
GPIO.setup( register_data_pin, GPIO.OUT )

#SR04 GPIO (afstandsmeter)
sr04_trig = 20
sr04_echo = 21
GPIO.setup(sr04_trig, GPIO.OUT)
GPIO.setup(sr04_echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


#Zet de gegeven waarde om in een binair getal
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

#Zet de gegeven bytes om in code voor de neopixel (ledstrip)
def neo_send_bytes(clock_pin, data_pin, bytes):
    for byte in bytes:
        for bit in byte:
            if bit % 2 == 1:
                GPIO.output(data_pin, GPIO.HIGH)
            else:
                GPIO.output(data_pin, GPIO.LOW)
            GPIO.output(clock_pin, GPIO.HIGH)
            GPIO.output(clock_pin, GPIO.LOW)

#Voor het aansturen van de NEO-Pixel
def neo(color):

    # Begin pakket
    neo_send_bytes(neo_clock_pin, neo_data_pin, [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])

    # Stuur de kleuren
    counter = 0
    for i in color:
        binary = to_binary(i)
        if counter == 0:
            blue = binary
        elif counter == 1:
            green = binary
        elif counter == 2:
            red = binary
        else:
            counter = 0
        counter += 1
    for x in range(0, 8):
        neo_send_bytes(neo_clock_pin, neo_data_pin, [[1, 1, 1, 1, 1, 1, 1, 1], blue, green, red])

    # Stuur het eindpakket
    neo_send_bytes(neo_clock_pin, neo_data_pin, [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]])

#Bepaald de positie van de servo (zwaai)
def position(position):
    position = round(((10 / 100) * position) + 2, 2)
    pwm = GPIO.PWM(servo, 50)  # 50 Hz (20 ms PWM period)
    pwm.start(position)
    time.sleep(0.02)

#Stuurt de posities voor een zwaai (servo)
def wave():
    for x in range(0, 5):
        position(20)
        time.sleep(0.4)
        position(80)
        time.sleep(0.4)

#Kijkt of de switch ingedrukt is. Zo ja stuurt deze een zwaai (servo) naar de friend
def wave_toggle():
    while True:
        if (GPIO.input(switch)):
            #Send zwaai naar andere machine
            pass

#Kijkt of de switch ingedrukt is. Zo ja stuurt deze een geluidssignaal (beeper) naar de friend
def signal():
    while True:
        if (GPIO.input(switch2)):
            #Stuur beep naar andere machine
            pass

#Stuurt de gegeven byte naar het schuifregister
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

#Kijkt naar het aantal gebruikers en stuurt de juiste waarde naar de show_users functie
def users(stop):
    users = 0
    while True:
        if stop == True:
            return
        users_old = users
        #Lees het aantal gebruikers uit een file
        try:
            with open("users.txt") as file:
                users = int(file.readline())
            if users != users_old:
                    #Zet het aantal users om naar bytes voor het schuifregister
                    bytes = []
                    for i in range(0, 8):
                        bytes.append(0)
                    for i in range(0, users):
                        bytes[i] = 1
                    show_users(bytes)
        except:
            print("An error has occord")
        time.sleep(1)

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

#Kijkt of de gebruiker te ver weg is (dus niet aanwezig op stoel)
def sr04_distance(distance):
    while True:
        if sr04 < distance:
            #Neopixel actie
            pass

#Stuurt de beeper aan
def beep():
    GPIO.output(speaker, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(speaker, GPIO.LOW)

@Pyro5.api.expose
class functions(): #object?

    def change_neo(rgb):
        thread_neo = threading.Thread(target = neo, args = (lambda: rgb,), daemon = True)
        thread_neo.start()

    #STUUR THREAD WAVE
    def recieve_wave(self):
        thread_wave = threading.Thread(target = wave, daemon = True)
        thread_wave.start()

    #STUUR THREAD BEEPER
    def recieve_beep(self):
        thread_beep = threading.Thread(target = beep, daemon = True)
        thread_beep.start()

sr04_thread = False

#Kijkt naar de gewenste status (GUI) van de sr04 (afstandssensor)
def check_sr04(state, distance): #state: True = on, False = off
    if state:
        if not sr04_thread:
            #Thread voor de sr04 (afstandssensor)
            stop_thread_sr04 = False
            thread_sr04 = threading.Thread(target=sr04_distance, args=(lambda: stop_thread_sr04, distance))
            thread_sr04.start()
    else:
        try:
            stop_thread_sr04 = True
            #thread_sr04.stop()
        except:
            pass


#THREADING
stop_thread_users = False

#Thread voor het sturen van een signaal (switch)
thread_signal = threading.Thread(target = signal, daemon = True)
thread_signal.start()

#Thread voor het laten zien van het aantal users (schuifregister)
thread_users = threading.Thread(target = users, args = (lambda: stop_thread_users,))
thread_users.start()

#NETWORKING
func = functions()
daemon = Pyro5.api.Daemon(host="192.168.192.24", port=9090)
Pyro5.api.Daemon.serveSimple(
    { func: "steam.functions" },
    ns=False,
    daemon=daemon,
    verbose = True
)

print("done")