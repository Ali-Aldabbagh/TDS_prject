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
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from std_msgs.msg import Float32
# Instantiate CvBridge
bridge = CvBridge()
angle1=0
angle2=0   
angle=0 
wind_size=100
window=wind_size
def msg_callback(imu_msg,pub_ang): 
    global angle,angle1,angle2,window,wind_size
    orientation_q = imu_msg.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    yaw_angle=(yaw*180/3.14)#+180
    if(window==wind_size):
       angle1=yaw_angle
    elif(window==0):   
        angle2=yaw_angle
        angle=(angle1-angle2)#*3
        window=wind_size+1
        pub_ang.publish(angle)
    window=window-1
    #print(yaw_angle)

def image_callback(image_msg,pub):    
    global angle
    cv2_img = bridge.imgmsg_to_cv2(image_msg, "bgr8")
    gx=angle
    gx=gx*math.pi/180
    arrow_length=50#int(50)
    xx=int(math.sin(gx)*arrow_length)
    yy=int(math.cos(gx)*arrow_length)
    colors = {'blue': (255, 0, 0), 'green': (0, 255, 0), 'red': (0, 0, 255), 'yellow': (0, 255, 255), 'magenta': (255, 0, 255), 'cyan': (255, 255, 0), 'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (125, 125, 125), 'rand': np.random.randint(0, high=256, size=(3,)).tolist(), 'dark_gray': (50, 50, 50), 'light_gray': (220, 220, 220)}
    cv2.arrowedLine(cv2_img, (212, 120), (xx+212,120-yy), colors['red'], 3, 8, 0, 0.1)
    imgMsg = bridge.cv2_to_imgmsg(cv2_img, "bgr8")#
    #pub.publish(imgMsg)
      
        
  
def main():
    rospy.init_node('IMU_Angle')
    #imu1= "/camera/imu"# /camera/imu or /imu/data
    imu_topic= "/imu/data"
    image="/camera/color/image_raw"
    pub_ang = rospy.Publisher('Angle_imu', Float32, queue_size=10)
    rospy.Subscriber(imu_topic, Imu, msg_callback,callback_args=pub_ang)
    pub = rospy.Publisher('image', Image, queue_size=10)
    rospy.Subscriber(image, Image, image_callback,callback_args=pub)

    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
    #out.release()
    #cv2.destroyAllWindows()



