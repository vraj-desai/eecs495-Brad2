from imageai.Detection import VideoObjectDetection
import sys, os, cv2
from cv2 import cv2

class objectDetector:
    def __init__(self):
        """Constructor for the class"""
        self.cam = cv2.VideoCapture()
        return

    def forFrame(self, frame_number, output_array, output_count, detected_frame):
        """Forframe processing"""
        print("FOR FRAME " , frame_number)
        # print("Output for each object : ", output_array)
        # print("Output count for unique objects : ", output_count)
        # print("------------END OF A FRAME --------------")
        cv2.imshow("Object Detector", detected_frame)
        return

    def detectObjects(self):
        detector = VideoObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath("yolo.h5")
        detector.loadModel()
        video_path = detector.detectObjectsFromVideo(camera_input=self.cam, save_detected_video = True,
                                                    per_frame_function = self.forFrame, output_file_path = "temp.avi" , log_progress=True,
                                                    return_detected_frame= True)
        return


def main():
    """Main function"""
    detector = objectDetector()
    detector.detectObjects()
    return

if __name__=="__main__":
    """Main driver"""
    main()