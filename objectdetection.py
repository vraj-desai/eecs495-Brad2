from imageai.Detection import VideoObjectDetection
import sys, os, cv2
from cv2 import cv2

def main():
    """Main function"""
    cam = cv2.VideoCapture(0)
    detector = VideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.loadModel()
    video_path = detector.detectObjectsFromVideo(camera_input=cam,
                                output_file_path=os.getcwd()
                                , frames_per_second=29, log_progress=True)
    print(video_path)
    return

if __name__=="__main__":
    """Main driver"""
    main()