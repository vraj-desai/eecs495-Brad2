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
            test()
            GPIO.cleanup()
    except KeyboardInterrupt:
        print("Done!")
        GPIO.cleanup()
