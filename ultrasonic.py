import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 15
GPIO_ECHO = 14

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def test():
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
    print(start, stop, (stop - start) * 17150)
    return

    while True:
        current = GPIO.input(GPIO_ECHO)
        if current == 0:
            stop = time.time()
        if current != last:
            if period != 0 and last == 1:
                # print("Period: %f s" % period)
                print(start, stop, (stop - start) * 17500)
                return 0
                period = 0
        period += 1
        last = current

if __name__ == '__main__':
    try:
        while True:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
            GPIO.setup(GPIO_ECHO, GPIO.IN)
            test()
            GPIO.cleanup()
    except KeyboardInterrupt:
        print("Done!")
        GPIO.cleanup()
