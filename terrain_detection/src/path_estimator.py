#! /usr/bin/python
import rospy
# ROS Image message
from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
#import matplotlib as plt
import matplotlib.pyplot as plt
from numpy import savetxt
import time
import numpy as np
import message_filters
import math
from scipy.signal import medfilt
from scipy.ndimage.interpolation import shift
from std_msgs.msg import Float32
from std_msgs.msg import String
from terrain_detection.msg import cent

bridge = CvBridge()

mapm = np.zeros((1000, 1000, 3), dtype = "uint8")
pyo=int(len(mapm)/2)
pxo=int(len(mapm)/2)
A=0.0
pub = rospy.Publisher('Path', Image, queue_size=1)
Angle=0.0
Speed=0.0
Cadance=0.0
color = (0, 255, 0)
factor=0.5

def msg_callback(angle_msg,speed_msg):
    global mapm,pyo,pxo,A,Speed,Cadance,color,factor   
    angle=(angle_msg.data)*factor
    g=speed_msg.data
    #print(g,len(g))
    speed=float(g[1:len(g)-6])
    Cadance=float(g[6:len(g)-1])
    #print(speed,angle)
    Speed=speed             
    start_point = (pyo,pxo)
  
    thickness = 2
    M=speed*10
    limt=20
    uplimt=40
    dlimt=-uplimt
    #angle=angle-7
    #if angle>=-limt and angle<=limt: 
    #   angle=0 
    #if angle>uplimt: 
    #   angle=90
    #if angle<dlimt:
    #   angle=-90
  
    #elif angle>20 and angle<60:
    #   angle=40
    #elif angle>60 and angle<100:
    #   angle=90
    #elif angle<-20 and angle>-60:
    #   angle=-40
    #elif angle<-60 and angle>-100:
    #   angle=-90
    
    A=angle+A
    if (A>360):
        A=A-360
    
    px=int(M*(math.cos(A*3.14/180)))
    py=int(M*(math.sin(A*3.14/180)))
    pyo=pyo-py
    pxo=pxo-px
    end_point = (pyo, pxo)
    mapm = cv2.arrowedLine(mapm, start_point, end_point,color, thickness)
    map_m = bridge.cv2_to_imgmsg(mapm, "bgr8")#
    pub.publish(map_m)
    start_point=end_point
    

def image_callback(image_msg,pub_image):
    global Angle, Speed,Cadance
    img = bridge.imgmsg_to_cv2(image_msg, "bgr8")
    gx=Angle
    gx=gx*math.pi/180
    #arrow_length=int(min(100,mag/50))
    arrow_length=int(min(100,Speed*70))
    xx=int(math.sin(gx)*arrow_length)
    yy=int(math.cos(gx)*arrow_length)
    colors = {'blue': (255, 0, 0), 'green': (0, 255, 0), 'red': (0, 0, 255), 'yellow': (0, 255, 255), 'magenta': (255, 0, 255), 'cyan': (255, 255, 0), 'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (125, 125, 125), 'rand': np.random.randint(0, high=256, size=(3,)).tolist(), 'dark_gray': (50, 50, 50), 'light_gray': (220, 220, 220)}
    cv2.arrowedLine(img, (212, 120), (xx+212,120-yy), (0, 0, 255), 3, 8, 0, 0.1)
    Displaytext='Speed='+str(Speed)+' '+'Cad='+str(Cadance)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,Displaytext, (20,20), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    imgMsg = bridge.cv2_to_imgmsg(img, "bgr8")
    pub_image.publish(imgMsg)

    

def angle_callback(angle_msg):
    global Angle,factor
    Angle=(angle_msg.data)*-1*factor
    
   
def angleimu_callback(angle_msg):
    global Angle
    Angle=angle_msg.data


def msg_callbackTerrain(msg):
    global color
    Terrain=msg.TDL1
    if Terrain==1:
       color=(0, 255, 255)
    elif Terrain==2:
       color=(255, 0, 255)
    elif Terrain==4:
       color=(0, 0, 255)
    elif Terrain==5:
       color=(255, 0, 0)
    else:
       color=(0, 255, 0)










def main():
    rospy.init_node('Path_estimator')  
    angle_topic="/Angle"
    angle_imu="/Angle_imu"
    speed_topic="/Speed_Cadance"

    angle=message_filters.Subscriber(angle_topic, Float32)
    speed=message_filters.Subscriber(speed_topic,String)
    # Set up your subscriber and define its callback
    ts = message_filters.ApproximateTimeSynchronizer([angle, speed], 10, 0.1, allow_headerless=True)
    ts.registerCallback(msg_callback)
    image="/camera/color/image_raw" 
    pub_image = rospy.Publisher('image', Image, queue_size=1)
    rospy.Subscriber(image, Image, image_callback,callback_args=pub_image)
    rospy.Subscriber(angle_topic, Float32, angle_callback)#angle_topic
    rospy.Subscriber(angle_imu, Float32, angleimu_callback)
    centroids_topic="/TP"
    rospy.Subscriber(centroids_topic, cent, msg_callbackTerrain)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
