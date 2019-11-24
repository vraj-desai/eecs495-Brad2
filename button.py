import RPi.GPIO as GPIO
import os
import object_detection_v2

class Button:
    def __init__(self, pin):
        """Initialize the button with the GPIO pin."""
        self.pin = pin
        

try:
    os.system("vcgencmd display_power 0")
    while True:
        button = Button(7)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.wait_for_edge(button.pin, GPIO.RISING)
        os.system("vcgencmd display_power 1")
        object_detection_v2.main()
        os.system("vcgencmd display_power 0")
except KeyboardInterrupt:
    pass
    # os.system("vcgencmd display_power 1")
