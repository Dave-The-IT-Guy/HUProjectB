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
GPIO.setup(switch, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(switch2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#Beeper GPIO (geluidssignaal)
speaker = 18
GPIO.setup(speaker, GPIO.OUT)

#Led GPIO (vriend niet aanwezig)
led = 4
GPIO.setup(led, GPIO.OUT)

#Schuifregister (aantal users)
register_shift_clock_pin = 5
register_latch_clock_pin = 6
register_data_pin = 13
GPIO.setup(register_shift_clock_pin, GPIO.OUT)
GPIO.setup(register_latch_clock_pin, GPIO.OUT)
GPIO.setup(register_data_pin, GPIO.OUT)

#SR04 GPIO (afstandsmeter)
sr04_trig = 20
sr04_echo = 21
GPIO.setup(sr04_trig, GPIO.OUT)
GPIO.setup(sr04_echo, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


#FUNCTIONS
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

def reverseTuple(tuples):
    new_tuple = tuples[::-1]
    return new_tuple

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
    #De neopixel ziet de waardes als bgr ipv rgb dus de tuple moet omgedraaid worden
    color = reverseTuple(color)

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
        time.sleep(0.29)
        position(80)
        time.sleep(0.29)

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
def users():
    users = 0
    while True:
        users_old = users
        #Lees het aantal gebruikers uit een file
        try:
            with open("users.txt") as file:
                users = int(file.readline())
                print("go")
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
        time.sleep(5)

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

def client():
    con = "PYRO:steam2.functions@192.168.192.64:9091"

    def send_wave():
        rem = Pyro5.api.Proxy(con)
        while True:
            if (GPIO.input(switch)):
                rem.recieve_led()
                time.sleep(1)

    def send_beep():
        rem = Pyro5.api.Proxy(con)
        while True:
            if (GPIO.input(switch2)):
                rem.recieve_beep()

    # Meet de afstand tussen gebruiker en sensor
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
        afstand = tijd * 34300  # Snelheid van geluid in seconden
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

    threading.Thread(target=send_wave, daemon=True).start()
    threading.Thread(target=send_beep, daemon=True).start()
    threading.Thread(target=send_sr04, daemon=True).start()

def send_beep_to_friend():
    con = "PYRO:steam2.functions@192.168.192.64:9091"
    rem = Pyro5.api.Proxy(con)
    rem.recieve_beep()

@Pyro5.api.expose
class functions():

    def change_neo(self, rgb):
        threading.Thread(target = neo, args = (rgb), daemon = True).start()

    #STUUR THREAD WAVE
    def recieve_wave(self):
        threading.Thread(target = wave, daemon = True).start()

    #STUUR THREAD BEEPER
    def recieve_beep(self):
        threading.Thread(target = beep, daemon = True).start()

    def send_beep(self):
        threading.Thread(target=send_beep_to_friend, daemon=True).start()

    # STUUR THREAD BEEPER
    def recieve_led(self):
        threading.Thread(target=light, daemon=True).start()

#THREADING
stop_thread_users = False

#Thread voor het laten zien van het aantal users (schuifregister)
threading.Thread(target = users, daemon = True).start()

#Start de thread die de server ook client maakt van de vriend zijn server
threading.Thread(target = client, daemon = True).start()

#NETWORKING
func = functions()
daemon = Pyro5.api.Daemon(host = "192.168.192.24", port = 9090)
Pyro5.api.Daemon.serveSimple(
    { func: "steam.functions" },
    ns = False,
    daemon = daemon,
    verbose = True
)