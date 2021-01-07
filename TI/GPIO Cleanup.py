import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)
servo = 25
clock_pin = 19
data_pin = 26
shift_clock_pin = 5
latch_clock_pin = 6
data_pin = 13

GPIO.setup(servo, GPIO.OUT)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(data_pin, GPIO.OUT)
GPIO.setup( shift_clock_pin, GPIO.OUT )
GPIO.setup( latch_clock_pin, GPIO.OUT )
GPIO.setup( data_pin, GPIO.OUT )


def apa102_send_bytes(clock_pin, data_pin, bytes):
    """
    zend de bytes naar de APA102 LED strip die is aangesloten op de clock_pin en data_pin
    """

    # implementeer deze functie:

    # zend iedere byte in bytes:
    #    zend ieder bit in byte:
    #       maak de data pin hoog als het bit 1 is, laag als het 0 is
    #       maak de clock pin hoog
    #       maak de clock pin laag
    for byte in bytes:
        for bit in byte:
            if bit % 2 == 1:
                GPIO.output(data_pin, GPIO.HIGH)
            else:
                GPIO.output(data_pin, GPIO.LOW)
            GPIO.output(clock_pin, GPIO.HIGH)
            GPIO.output(clock_pin, GPIO.LOW)

apa102_send_bytes(clock_pin, data_pin, [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
for i in range(0, 8):
    apa102_send_bytes(clock_pin, data_pin, [[1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
apa102_send_bytes(clock_pin, data_pin, [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]])


def hc595( shift_clock_pin, latch_clock_pin, data_pin, value, delay ):
    GPIO.output(latch_clock_pin, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(latch_clock_pin, GPIO.LOW)

    if value % 2 == 1:
       GPIO.output( data_pin, GPIO.HIGH )
    else:
       GPIO.output( data_pin, GPIO.LOW )
    value = value // 2

    GPIO.output(shift_clock_pin, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(shift_clock_pin, GPIO.LOW)

delay = 0.03
for i in range(0, 8):
   hc595( shift_clock_pin, latch_clock_pin, data_pin,   0, delay )



pwm = GPIO.PWM(servo, 50)  # 50 Hz (20 ms PWM period)
pwm.start(2)

time.sleep(0.2)

for i in range(1, 30):
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.LOW)
GPIO.cleanup()