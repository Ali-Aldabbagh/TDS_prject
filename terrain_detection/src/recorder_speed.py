#! /usr/bin/python
from turtle import distance
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
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Int32
distance=0.0
hz=2
speed_array=np.zeros([1,3])
time=0.0
def msg_callback_speed(msg,key_msg):
    global distance,hz,time,speed_array
    g=msg.data
    Speed=float(g[1:len(g)-6])
    distance=(Speed/2)+distance

    print("Recorded_Speed=",Speed)
    #Cadance=float(g[6:len(g)-1])
    #if Cadance>0:
    #   Step_size=Speed/Cadance
    #else:
    #   Step_size=0   
    #pub.publish(Step_size)
    #===================================================
    
    speed_vector=np.zeros([1,3])
    time=time+0.5
    speed_vector[0,0]=time
    speed_vector[0,1]=Speed
    speed_vector[0,2]=distance
    speed_array=np.vstack((speed_array,speed_vector))
    savetxt('Henri2_new.csv', speed_array, delimiter=',')



        
  
def main():
    rospy.init_node('Speed_recorder')
    speed_msg=message_filters.Subscriber('/Speed_Cadance', String)
    key_msg=message_filters.Subscriber("/chatter",Int32)
    # Set up your subscriber and define its callback
    ts = message_filters.ApproximateTimeSynchronizer([speed_msg, key_msg], 10, 0.1, allow_headerless=True)
    ts.registerCallback(msg_callback_speed)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
    #out.release()
    #cv2.destroyAllWindows()



