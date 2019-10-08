import sys, os, json, cv2


class video_processor:

    def __init__(self):
        """Constructor for the class"""

        #Variable to select button status
        #TODO: Turn close webcam when button is off
        self.buttonStatus = False
        self.currFrame = None

    
    def button_pressed():
        """Changes the status of button after pressed"""
        #TODO: Handle the webcam close and open as well
        self.buttonStatus != self.buttonStatus

        if self.buttonStatus:
            cv2.destroyAllWindows()
            self.cam.release()
        else:
            # CV2 video capture object
            self.cam = cv2.VideoCapture()

            #---Set webcam size for screen---
            self.cam.set(3, 1080)
            self.cam.set(4, 900)

    def process_frame():
        """Reads in the frame and processes it"""
        #TODO: Read in the frame and process it
        
    


def main():
    """Main function"""
    processor = video_processor()

    return

if __name__=="__main__":
    """Main function driver"""
    main()