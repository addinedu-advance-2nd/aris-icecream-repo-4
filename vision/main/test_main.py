import cv2
import cv2.aruco as aruco
from ultralytics import YOLO

import rclpy as rp
from rclpy.node import Node
from robot_msgs.msg import Vision

import numpy as np
import time

        
class VisionPublisher(Node):
    def __init__(self):
        super().__init__('vision_publisher_node')
        self.vision_publisher = self.create_publisher(Vision, '/vision', 10) ##
        self.timer_period = 0.05
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.model = YOLO('./vision/main/segmentation.pt')    # segmentation.pt 
        self.cap = cv2.VideoCapture(0)
        self.frame = None

    def timer_callback(self):
        self.jig_status = [0, 0, 0]
        self.hand_status = False
        self.hand_pose = []

#        if self.cap.isOpened():
#             success, self.frame = self.cap.read()
        success, self.frame = self.cap.read()

        if success:
            # Run YOLOv8 inference on the self.frame
            results = self.model(self.frame)
            
            # Extract bounding boxes, classes, names, and confidences
            boxes = results[0].boxes.xyxy.tolist()
            classes = results[0].boxes.cls.tolist()
            names = results[0].names
            confidences = results[0].boxes.conf.tolist()

            # Iterate through the results
            for box, cls, conf in zip(boxes, classes, confidences):
                x1, y1, x2, y2 = box 
                confidence = conf
                detected_class = cls
                name = names[int(cls)]
                """
                # Detect the center of the detected object
                self.ObjectCenter(x1, y1, x2, y2, name)
                
                # Identify the position of ice cream in the jig
                jig_pose = self.JigPosition(x1, y1, x2, y2, name, names)
                #print(jig_pose)
                if jig_pose is not None:
                    self.jig_status[jig_pose] = 'strawberry'    ###### [need to connect]
                """
                self.hand_position(x1, y1, x2, y2, name, names)


            copy_frame = self.frame.copy()

            self.jig_status = [0, 0, 0] #
            
            self.flavorDict = {1: 'chocolate', 2: 'vanilla', 3: 'strawberry', 4: 'mint chocolate', 5: 'grape', 6: 'apple'}
            #self.flavorDict = {'chocolate': 1, 'vanilla': 2, 'strawberry': 3, 'mint chocolate': 4, 'grape': 5, 'apple': 6}

            aruco_frame, corners, ids, centers = self.detect_aruco_markers(copy_frame)
            if ids is not None:
                for id, center in zip(ids, centers):
                    
                    aruco_position = self.ArucoPosition(center[0], center[1])
                    
                    # print('aruco_position:', aruco_position, 'id:',id)
                    if aruco_position is not None:
                        #self.jig_status[aruco_position] = self.flavorDict[id[0]]
                        self.jig_status[aruco_position] = int(id[0])    ### python 기본 int는 4bytes 아님 / 
                        #print(type(int(id[0])))
                        
                        # print(self.jig_status)            
            
            vision_msg = Vision()
            print('jig_status:', self.jig_status)
            # vision_msg.jig_icecream = np.array(self.jig_status, dtype=np.int32).tolist()  ###
            vision_msg.jig_icecream = self.jig_status   ###
            vision_msg.hand = self.hand_status
            vision_msg.hand_position = self.hand_pose
            self.vision_publisher.publish(vision_msg) ##

            # Visualize the results on the self.frame
            annotated_frame = results[0].plot()

            # Display the annotated self.frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)
            cv2.imshow("ArUco Marker Detection", aruco_frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.cap.release()
                cv2.destroyAllWindows()
    
    def ObjectCenter(self, x1, y1, x2, y2, name):
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        cv2.putText(self.frame, f"{name} Center: ({center_x:.0f}, {center_y:.0f})", 
                            (int(x1), int(y1) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)  
    
    def JigPosition(self, x1, y1, x2, y2, name, names):
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        jig = [0, 1, 2] # position of jig
        jig_position = None
        
        # webcam (pixel)
        if (name == names[1]) and (30 <= center_y <= 120):  # trash.pt : name[6] == 'ice cream'
            if (480 <= center_x <= 560): 
                jig_position = jig[0]
            elif (400 <= center_x <= 480):
                jig_position = jig[1]
            elif (320 <= center_x <= 480):
                jig_position = jig[2]
        
        return jig_position
    
    def ArucoPosition(self, x, y):
        center_x = x
        center_y = y

        jig = [0, 1, 2] 
        jig_position = None
        
        # webcam (pixel)
        if 30 <= center_y <= 120:  
            if (480 <= center_x <= 560): 
                jig_position = jig[0]
            elif (400 <= center_x <= 480):
                jig_position = jig[1]
            elif (320 <= center_x <= 480):
                jig_position = jig[2]
        
        return jig_position

    def hand_position(self, x1, y1, x2, y2, name, names):
        if name == 'hand':
            self.hand_pose = [int((x1 + x2) / 2), int((y1 + y2) / 2)]
            
            if 35 <= self.hand_pose[0] <= 580 and 23 <= self.hand_pose[1]:
                self.hand_status = True
    
    def detect_aruco_markers(self, copy_frame):
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
        self.aruco_params = aruco.DetectorParameters()
        self.aruco_params.adaptiveThreshConstant = 3
        self.aruco_params.minMarkerPerimeterRate = 0.1
        self.aruco_params.maxMarkerPerimeterRate = 10.0
        self.aruco_params.polygonalApproxAccuracyRate = 0.03
        self.aruco_params.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX
        
        self.flavorDict = {1: 'chocolate', 2: 'vanilla', 3: 'strawberry', 4: 'mint chocolate', 5: 'grape', 6: 'apple'}
        # self.frame = None

        gray = cv2.cvtColor(copy_frame, cv2.COLOR_BGR2GRAY) ##
        corners, ids, _ = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)  # Attribute Error (venv) : pip install opencv-contrib 
        #corners, ids, _ = aruco.ArucoDetector.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)
        # print(corners, ids)
        
        centers = []

        if ids is not None:
            aruco.drawDetectedMarkers(copy_frame, corners, ids)
            for i in range(len(ids)):
                c = corners[i][0]
                x, y = int(c[:, 0].mean()), int(c[:, 1].mean())
                centers.append((x,y))
                cv2.putText(copy_frame, f"ID: {self.flavorDict[ids[i][0]] if ids[i][0] in self.flavorDict else [i][0]}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return copy_frame, corners, ids, centers


def main(args=None):
    rp.init()
    vision_publisher_node = VisionPublisher()
    try:
        rp.spin(vision_publisher_node)
    finally:
        vision_publisher_node.destroy_node()
        rp.shutdown()

if __name__ == '__main__':
    main()
