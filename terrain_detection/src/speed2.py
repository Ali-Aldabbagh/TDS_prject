#! /usr/bin/python
import rospy
# ROS Image message
from sensor_msgs.msg import Image
from std_msgs.msg import String
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
import pickle
from scipy.signal import butter,filtfilt
import pandas as pd
from rospy_tutorials.msg import Floats


Speed=0.0
Cadance=0

  
def msg_callback(msg):
    global Speed,Cadance
    g=msg.data
    Speed=float(g[1:len(g)-4])
    Cadance=int(g[len(g)-2])
    print(Speed,Cadance)
    
       
    


    

    

      
        
  
def main():
    rospy.init_node('Speed_EstimatorIMU')
    #imu1= "/camera/imu"# /camera/imu or /imu/data
    #imu2= "/imu/data"
    #image="/camera/color/image_raw"# /camera/depth/image_rect_raw
    #image_msg=message_filters.Subscriber(image, Image)
    #imu_msg1=message_filters.Subscriber(imu1,Imu)
    #imu_msg2=message_filters.Subscriber(imu2,Imu)
    # Set up your subscriber and define its callback
    #ts = message_filters.ApproximateTimeSynchronizer([imu_msg1, imu_msg2], 5, 0.1, allow_headerless=True)
    #ts.registerCallback(msg_callback)
    #pub = rospy.Publisher('image', Image, queue_size=100)
    #pub=rospy.Publisher('features_val',Floats,queue_size = 10)
    rospy.Subscriber('/Speed_Cadance', String, msg_callback)
    
    #rospy.Subscriber('clock', Clock, msg_callback2)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
    #out.release()
    #cv2.destroyAllWindows()



