from imageai.Detection import VideoObjectDetection
import sys, os, cv2
from cv2 import cv2

def forFrame(frame_number, output_array, output_count, detected_frame):
    """Forframe processing"""
    print("FOR FRAME " , frame_number)
    print("Output for each object : ", output_array)
    print("Output count for unique objects : ", output_count)
    print("------------END OF A FRAME --------------")

def main():
    """Main function"""
    cam = cv2.VideoCapture(0)
    detector = VideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("yolo.h5")
    detector.loadModel()
    video_path = detector.detectObjectsFromVideo(camera_input=cam, save_detected_video = True,
                                                per_frame_function = forFrame, output_file_path = "temp.avi" , log_progress=True,
                                                return_detected_frame= True)
    return

if __name__=="__main__":
    """Main driver"""
    main()