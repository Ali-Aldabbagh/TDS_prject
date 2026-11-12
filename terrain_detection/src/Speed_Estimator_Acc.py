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
from rosgraph_msgs.msg import Clock



features_array=np.zeros([1,5])
c=False
counter=0.0

timer=0.0
Ct=False
timer_first=0.0

    
def msg_callback(imu_msg1):
    global  features_array, first_time, c,counter,nano_first
    features=np.zeros([1,5])

    seconds = rospy.get_time()

    if c==False:
       first_time=seconds
       c=True
    

    #print(imu_msg1.linear_acceleration.x)

    #orientation_q = imu_msg2.orientation
    #orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    #(roll, pitch, yaw) = euler_from_quaternion (orientation_list)

    x=imu_msg1.linear_acceleration.x
    y=imu_msg1.linear_acceleration.y
    z=imu_msg1.linear_acceleration.z
    counter=counter+1
    #t=seconds-first_time
    time=counter/200.0
    features[0,0]=time
    features[0,1]=x
    features[0,2]=y
    features[0,3]=z
    features[0,4]=np.sqrt(x*x+y*y+z*z)
    
    features_array=np.vstack((features_array,features))
    savetxt('test.csv', features_array, delimiter=',')
    #print(time)
    print(timer, time)

def msg_callback2(clock_msg):
    global timer_first,timer,Ct,nano_first
    if Ct==False:
       timer_first=float(clock_msg.clock.secs)
       nano_first=float(clock_msg.clock.nsecs)
       Ct=True
    timer=float(clock_msg.clock.secs-timer_first)
    nano=float((clock_msg.clock.nsecs-nano_first)/1000000000)
    timer=timer+nano
    #print(timer)

    

    

      
        
  
def main():
    rospy.init_node('Speed_EstimatorIMU')
    imu1= "/camera/imu"# /camera/imu or /imu/data
    #imu2= "/imu/data"
    #image="/camera/color/image_raw"# /camera/depth/image_rect_raw
    #image_msg=message_filters.Subscriber(image, Image)
    #imu_msg1=message_filters.Subscriber(imu1,Imu)
    #imu_msg2=message_filters.Subscriber(imu2,Imu)
    # Set up your subscriber and define its callback
    #ts = message_filters.ApproximateTimeSynchronizer([imu_msg1, imu_msg2], 5, 0.1, allow_headerless=True)
    #ts.registerCallback(msg_callback)
    #pub = rospy.Publisher('image', Image, queue_size=100)
    rospy.Subscriber(imu1, Imu, msg_callback)
    rospy.Subscriber('clock', Clock, msg_callback2)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
    #out.release()
    #cv2.destroyAllWindows()



