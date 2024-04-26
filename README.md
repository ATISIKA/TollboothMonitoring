Overview:
This project aims to develop a system for vehicle counting and monitoring using computer vision techniques. The system utilizes video processing to detect and track vehicles in a given scene, allowing for the analysis of traffic flow, congestion, and other related metrics.

Features:

Vehicle detection: The system detects vehicles in a video stream using the YOLO (You Only Look Once) object detection algorithm.
Vehicle tracking: Detected vehicles are tracked using the dlib correlation tracker, enabling continuous monitoring of their movement.
Counting: The system counts the number of vehicles entering and exiting a predefined region of interest (ROI) within the video frame.
Visualization: The project provides real-time visualization of vehicle counts and movement patterns, enhancing situational awareness for traffic management.
Technologies Used:

OpenCV: Utilized for video processing, including vehicle detection, tracking, and ROI manipulation.
dlib: Employed for object tracking, specifically tracking vehicles across frames.
YOLO (You Only Look Once): Implemented for vehicle detection within video frames.
Python: Programming language used for the development of the project.
Instructions:

Setup:
Ensure Python is installed on your system.
Install required libraries using pip install -r requirements.txt.
Download the YOLO configuration and weights files (yolov4-tiny.cfg and yolov4-tiny.weights) from the official source and place them in the project directory.
Execution:
Run the VehicleCounter.py script using Python.
Provide the path to the input video file (highway.mp4 or similar) when prompted.
Usage:
Upon execution, the system will process the input video, detecting and tracking vehicles in real-time.
Vehicle counts (inbound and outbound) will be displayed on the screen.
Press 'q' to exit the application.
Customization:
Adjust parameters such as confidence threshold (confThreshold), non-maximum suppression threshold (nmsThreshold), and ROI dimensions to suit specific requirements.
Modify the code to incorporate additional features or integrate with external systems as needed.
Contributing:
Contributions to this project are welcome! Feel free to fork the repository, make modifications, and submit pull requests for review.


Authors:

Atisika Kwadwo Daniel - Initial development and contributions.

Disclaimer:
This project is for educational and demonstration purposes only. Use at your own risk. The authors and contributors are not liable for any damages or misuse of the software.

References:

Link to YOLO documentation:  https://opencv-tutorial.readthedocs.io/en/latest/yolo/yolo.html
