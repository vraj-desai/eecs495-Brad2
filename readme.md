Back Me Up - BRAD 2

Independently determining obstacles and avoiding collisions behind a wheelchair is difficult without physically turning around; additionally, the weight and expense of a motorized wheelchair amplifies the risk of damage to others and itself. This project is intended to improve the safety of using a motorized wheelchair via a back-up system that would allow users to visualize where their wheelchair is in the camera’s field of view and allow them to navigate appropriately. In addition to the camera, ultrasonic sensors will provide additional warning in case of an unexpected obstacle.

For the omega release, the system is enclosed in a water resistant case and runs using a portable power supply. It can be turned on and off using the button.

The camera displays a live video feed with boxes around the objects. The object detection program is trained to detect different objects in each frame such as sofa, bottles, people, etc. There are also three distance readings on the screen, which is from the ultrasonic sensors calculating the distances of the closest objects. Both visual and audio warnings are provided when obstacles are within 100 centimeters.

To run our program, use the following command:

 python3 button.py

Our program requires at least one video input device (ex. camera or webcam) and one audio output device (ex. headphones or speaker) connected to the device it's running on.
