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
from std_msgs.msg import Int32



features_array=np.zeros([1,5])
c=False
counter=0.0
timer=0.0
Ct=False
timer_first=0.0
j=0
    
def cb_one(imu_msg1):
    global  features_array, first_time, c,counter,nano_first,j
    features=np.zeros([1,5])
    seconds = rospy.get_time()
    if c==False:
       first_time=seconds
       c=True
    x=imu_msg1.linear_acceleration.x
    y=imu_msg1.linear_acceleration.y
    z=imu_msg1.linear_acceleration.z
    counter=counter+1
    #t=seconds-first_time
    print(j)
    if(j==1):
       time=counter/200.0
       features[0,0]=time
       features[0,1]=x
       features[0,2]=y
       features[0,3]=z
       features[0,4]=np.sqrt(x*x+y*y+z*z) 
       features_array=np.vstack((features_array,features))
       savetxt('trial_raw.csv', features_array, delimiter=',')
       print(j) 
       j=100 

def cb_two(key):
    j=key.data
   

    

      
        
  
def main():
    rospy.init_node('IMU_recorder')
    imu1= "/camera/imu"# /camera/imu or /imu/data
    key="/chatter"

    # Set up your subscriber and define its callback
    rospy.Subscriber(imu1, Imu, cb_one)
    rospy.Subscriber(key, Int32, cb_two)
    #pub = rospy.Publisher('image', Image, queue_size=100)
    #rospy.Subscriber(imu, Imu, msg_callback,callback_args=pub)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
    #out.release()
    #cv2.destroyAllWindows()



