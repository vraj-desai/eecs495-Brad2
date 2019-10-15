import sys, os, json, cv2


class video_processor:

    def __init__(self):
        """Constructor for the class"""

        #Variable to select button status
        #TODO: Turn close webcam when button is off
        self.buttonStatus = False
    
    def button_pressed():
        """Changes the status of button after pressed"""
        #TODO: Handle the webcam close and open as well
        self.buttonStatus != self.buttonStatus

        if self.buttonStatus:
            cv2.destroyAllWindows()
            self.cam.release()
            self.cam = None
        else:
            # CV2 video capture object
            self.cam = cv2.VideoCapture()

            #---Set webcam size for screen---
            self.cam.set(3, 1080)
            self.cam.set(4, 900)

    def process_frame():
        """Reads in the frame and processes it and display it"""
        #TODO: Read in the frame and process it
        if self.cam != None:
            readStatus, frame = self.cam.read()
            label = object_detect()
            #TODO: Process frame
            #cv2.imshow("attentionChecker", frame)
            image = cv2.putTest(frame, label, (105,105), cv2.FONT_HERSHEY_PLAIN,1,(255, 0, 0), 2)
            cv2.imshow("attentionChecker", image)

    def object_detect():
        """return label"""
        pass


def main():
    """Main function"""
    processor = video_processor()

    # Button press will be the signal from hardware
    # While button is on button_press will be True
    # For now it is always true since there is no hardware signal
    button_press = True

    while True:
        if button_press:
            if not processor.buttonStatus:
                processor.button_pressed()
            processor.process_frame()
        else:
            processor.button_pressed()


    return

if __name__=="__main__":
    """Main function driver"""
    main()
