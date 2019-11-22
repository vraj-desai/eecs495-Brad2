# USAGE
# python object_detection_v2.py --prototxt proto.txt --model model

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from cv2 import cv2
from cv2 import rectangle
import numpy as np
import argparse
import imutils
import time
import cv2
import random
import threading
import RPi.GPIO as GPIO

prototxt = "/home/pi/dev/EECS495-Brad2/proto.txt"
model = "/home/pi/dev/EECS495-Brad2/model"
confidence_threshold = 0.2

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

class UltrasonicSystem:
    def __init__(self, gpio, num_sensors):
        """Initialize ultrasonic system with sensors and GPIO pins."""
        self.gpio = gpio
        self.num_sensors = num_sensors
        self.sensors = []
        self.sensor_threads = []
        self.stop = False

    def add_sensors(self):
        """Initialize sensors with corresponding GPIO pins."""
        GPIO.setmode(GPIO.BCM)
        for i in range(0, self.num_sensors):
            self.sensors.append(Sensor(i + 1, self.gpio[i + 1][0], self.gpio[i + 1][1]))
            self.sensors[i].pin_setup()
        return

    def spawn_sensor_threads(self):
        """Create threads for simultaneous sensor polling."""
        while True:
            for i in range(0, self.num_sensors):
                self.sensor_threads.append(threading.Thread(target=self.sensors[i].distance, 
                                                            daemon = True))
            self.update_measurements()
            self.sensor_threads.clear()
            if self.stop:
                break
        return

    def update_measurements(self):
        """Synchronize and start sensor threads."""
        for sensor_thread in self.sensor_threads:
            sensor_thread.start()
        for sensor_thread in self.sensor_threads:
            sensor_thread.join()
        return

    def write_measurements_to_frame(self, frame):
        """Annotate the frame with sensor readings."""
        dist_flag = False
        for i in range(0, self.num_sensors):
            if self.sensors[i].measurement != -1:
                if self.sensors[i].measurement < 50:
                    dist_flag = True
                    cv2.putText(frame, "{:.2f} cm".format(self.sensors[i].measurement), (15 + (i * 190), 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "{:.2f} cm".format(self.sensors[i].measurement), (15 + (i * 190), 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        if dist_flag:
            cv2.putText(frame, "[!!]", (550,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        return frame


class Sensor:
    def __init__(self, num, trigger, echo):
        """Initialize sensor with GPIO pins."""
        self.num = num
        self.trigger = trigger
        self.echo = echo
        self.measurement = -1

    def pin_setup(self):
        """Setup GPIO pins for sensor."""
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        return

    def distance(self):
        """Calculate distance from sensor signal."""
        if self.trigger == 0:
            time.sleep(2)
            d = random.randrange(10, 200, 1)
            if d < 400:
                self.measurement = d
            else:
                self.measurement = -1
            return
        else:
            GPIO.output(self.trigger, False)
            time.sleep(2)
            GPIO.output(self.trigger, True)
            time.sleep(0.00001)
            GPIO.output(self.trigger, False)

            start = time.time()
            while GPIO.input(self.echo) == 0:
                start = time.time()

            stop = time.time()
            while GPIO.input(self.echo) == 1:
                stop = time.time()

            d = (stop - start) * 17150

            if d < 400:
                self.measurement = d
            else:
                self.measurement = -1
            return


def cleanup(fps, vs):
    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
    GPIO.cleanup()

def main():
    button_pin = 7
    GPIO.setmode(GPIO.BCM)
    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    # time.sleep(2.0)
    fps = FPS().start()

    ultrasonic = UltrasonicSystem({1: [15, 14], 2: [24, 23], 3: [8, 25]}, 3)
    ultrasonic.add_sensors()
    ultrasonic_spawn = threading.Thread(target=ultrasonic.spawn_sensor_threads, daemon=True)
    ultrasonic_spawn.start()
    GPIO.add_event_detect(button_pin, GPIO.RISING)
    try:
        # loop over the frames from the video stream
        while True:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 500 pixels
            frame = vs.read()
            # frame = imutils.resize(frame, width=600)

            # grab the frame dimensions and convert it to a blob
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                0.007843, (300, 300), 127.5)

            # pass the blob through the network and obtain the detections and
            # predictions
            net.setInput(blob)
            detections = net.forward()

            # loop over the detections
            for i in np.arange(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > confidence_threshold:
                    # extract the index of the class label from the
                    # `detections`, then compute the (x, y)-coordinates of
                    # the bounding box for the object
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # draw the prediction on the frame
                    label = "{}: {:.2f}%".format(CLASSES[idx],
                        confidence * 100)
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                        COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            frame = ultrasonic.write_measurements_to_frame(frame)
            # show the output frame
            cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            # cv2.resizeWindow("Frame", 640, 480)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                ultrasonic.stop = True
                time.sleep(2)
                break

            if GPIO.event_detected(button_pin):
                ultrasonic.stop = True
                time.sleep(2)
                break

            # update the FPS counter
            fps.update()
        cleanup(fps, vs)
    except KeyboardInterrupt:
        cleanup(fps, vs)

if __name__ == "__main__":
    main()
