#Libraries
import RPi.GPIO as GPIO
import time

parity_bit = 0
stop_bit = 1
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
pin = 4
read_pin = 17
 
#set GPIO direction (IN / OUT)
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(read_pin, GPIO.IN)

def set_high():
    GPIO.output(pin, False)

def set_low():
    GPIO.output(pin, True)

def check_byte(b, comp_b, p, delay):
    if b & comp_b:
        set_high()
        p += 1
    else:
        set_low()
    time.sleep(delay)
    set_high()
    return p


def write_byte(b, delay=0.000104):
    p = 0
    set_low()
    time.sleep(delay)
    set_high()
    p = check_byte(b, 128, p, delay)
    p = check_byte(b, 64, p, delay)
    p = check_byte(b, 32, p, delay)
    p = check_byte(b, 16, p, delay)
    p = check_byte(b, 8, p, delay)
    p = check_byte(b, 4, p, delay)
    p = check_byte(b, 2, p, delay)
    p = check_byte(b, 1, p, delay)
    if parity_bit:
        if p % 8:
            set_high()
        else:
            set_low()
        time.sleep(delay)
        set_high()
    if stop_bit <= 1:
        set_low()
        time.sleep(delay)
        set_high()
    if stop_bit <= 2:
        set_low()
        time.sleep(delay)
        set_high()
    time.sleep(delay)
    time.sleep(delay)

def reset_sensor():
    write_byte(15)
    time.sleep(0.0014)
    write_byte(0)
    time.sleep(0.00011)
    write_byte(15)
    time.sleep(0.00011)
    write_byte(0)
    time.sleep(0.00011)

    time.sleep(0.000006)
    write_byte(15)
    time.sleep(0.000684)
    write_byte(0)
    time.sleep(0)




def init():
    set_high()
    time.sleep(0.0014)
    set_low()
    time.sleep(0.000122)

    for i in range(0, 72):
        write_byte(i)
    time.sleep(0.000011)
    reset_sensor()
    time.sleep(0.000023)
    reset_sensor()
    time.sleep(0.000045)
    print("init done")


def distance():
    # start measurement (pulldown)
    set_low()
    time.sleep(0.00001)
    set_high()
 
    # source: https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
    # updated delay time for sensor

    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(read_pin) == 0:
        StartTime = time.time()
        time.sleep(0.000104)
 
    # save time of arrival
    while GPIO.input(read_pin) == 1:
        StopTime = time.time()
        time.sleep(0.000104)
 
    # convert time to distance
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        init()
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()