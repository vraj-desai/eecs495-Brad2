import RPi.GPIO as GPIO
import object_detection_v2

class Button:
    def __init__(self, pin):
        """Initialize the button with the GPIO pin."""
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    button = Button(14)
    GPIO.wait_for_edge(button.pin, GPIO.RISING)
    object_detection_v2.object_detect(button.pin)
    GPIO.cleanup()
