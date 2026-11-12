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



features_array=np.zeros([1,6])

    
def msg_callback(imu_msg): 

    orientation_q = imu_msg.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    angle=(roll*180/3.14)+180
    angle_cal = (angle - 90) * -1
    print(angle_cal)

    

    

      
        
  
def main():
    rospy.init_node('Calb_IMU')
    #imu1= "/camera/imu"# /camera/imu or /imu/data
    imu_topic= "/imu/data"
    #image="/camera/color/image_raw"# /camera/depth/image_rect_raw
    #image_msg=message_filters.Subscriber(image, Image)
    #imu_msg1=message_filters.Subscriber(imu1,Imu)
    #imu_msg2=message_filters.Subscriber(imu2,Imu)
    # Set up your subscriber and define its callback
    #ts = message_filters.ApproximateTimeSynchronizer([imu_msg1, imu_msg2], 5, 0.1, allow_headerless=True)
    #ts.registerCallback(msg_callback)
    #pub = rospy.Publisher('image', Image, queue_size=100)
    rospy.Subscriber(imu_topic, Imu, msg_callback)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
    #out.release()
    #cv2.destroyAllWindows()



