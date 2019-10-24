import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 15
GPIO_ECHO = 14

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

sensor_pins = {1: [15, 14], 2: [0, 0], 3: [0, 0], 4: [0, 0]}

def pin_setup():
    """Define input and output GPIO pins on the Raspberry Pi."""
    GPIO.setmode(GPIO.BCM)
    for sensor in sensor_pins:
        GPIO.setup(sensor[0], GPIO.OUT)
        GPIO.setup(sensor[1], GPIO.IN)


def thread_distance(trigger, echo, sensor_num, measurements):
    """Convert signals from sensor corresponding to sensor_num to a distance."""
    GPIO.output(trigger, False)
    time.sleep(2)
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    start = time.time()
    while GPIO.input(echo) == 0:
        start = time.time()

    stop = time.time()
    while GPIO.input(echo) == 1:
        stop = time.time()

    d = (stop - start) * 17150

    if d < 400:
        measurements[sensor_num] = d
    else:
        measurements[sensor_num] = -1
    return


def get_sensor_distances(sensors, measurements):
    """Get the current distance measurements from all sensors."""
    for sensor in sensors:
        sensor.start()
    for sensor in sensors:
        sensor.join()
    print(measurements)
    return


def main_test():
    try:
        pin_setup()
        while True:
            measurements = {}
            sensors = []
            for i in range(1, 5):
                sensors.append(threading.Thread(target=thread_distance, args=(sensor_pins[i][0], 
                                                sensor_pins[i][1], i, measurements), daemon=True))
            get_sensor_distances(sensors, m)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Done!")


def distance():
    GPIO.output(GPIO_TRIGGER,False)
    time.sleep(2)
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        start = time.time()

    stop = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        stop = time.time()
    d = (stop - start) * 17150
    if d < 400:
        print(d, "cm")
    else:
        print("No obstacle in range")
    return


if __name__ == '__main__':
    try:
        while True:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
            GPIO.setup(GPIO_ECHO, GPIO.IN)
            distance()
            GPIO.cleanup()
    except KeyboardInterrupt:
        print("Done!")
        GPIO.cleanup()
