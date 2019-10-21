For alpha realease, we have implemented two skeletal features running independantly each other. 
First of them is a program to return distance to the closest object using ultrasonic sesnor. You need to install all the dependancies to run the program. 
To run use the following command:

# python3 ultrasonic.py

Notice that it uses hardware such as ultrasonic senor and raspberry pi.


Second skeletal feature uses camera or webcam and uses trained model to detect differnet objects in each frame such as sofa, bottles, people etc.
To run use following command:

# python3 object_detection_v2.py -m model -p proto.txt

This also requires at least one video input device sucj as camera or webcam connected to the device it's runnnin on.
