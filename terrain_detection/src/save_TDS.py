#! /usr/bin/python
import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
#import matplotlib as plt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np
from terrain_detection.msg import cent
#from numpy import savetxt
#====================================

#++++++++++++++++++++++++++++++++++==
    

# Instantiate CvBridge
bridge = CvBridge()
#global x

#global y
y=np.zeros((1,9))
x=np.zeros((1,1))
first_time=0
#y=[0,0,0,0,0,0]
#y=np.zeros((1,16))
#bool c
c=False

f = open("saved_data/namefile.txt", "r")
name=f.read() 

#print(f.read()) 


#I HAVE PROBLAM IN ASSGINING LOCAL GLOBAL VARIABLE CHECK YOUR CODES IN PYT3 GOOGLE DRIVE(SOLVED ;) )
def msg_callback(msg):

    global y,x,c,name,first_time
    data=np.zeros((1,9))
    data[0,0]=msg.TDL1
    data[0,1]=msg.tc1
    data[0,2]=msg.yc1
    data[0,3]=msg.TDL2
    data[0,4]=msg.tc2
    data[0,5]=msg.yc2
    data[0,6]=msg.TDL3
    data[0,7]=msg.tc3
    data[0,8]=msg.yc3
    seconds = rospy.get_time()
    
    
    
    if c==False:
        y[0,0]=data[0,0]
        y[0,1]=data[0,1]
        y[0,2]=data[0,2]
        y[0,3]=data[0,3]
        y[0,4]=data[0,4]
        y[0,5]=data[0,5]
        y[0,6]=data[0,6]
        y[0,7]=data[0,7]
        y[0,8]=data[0,8]
        
        first_time=seconds
        
        c=True
        name=name+'_A'
        f = open("saved_data/namefile.txt", "w") 
        f.write(name)
        print("Start recording in file:",name)
    else:
        y = np.vstack([y, data])
        seconds=seconds-first_time
        x  = np.vstack([x, seconds])

        #print(len(x),len(y1))


    #grd1=msg.data1[0]
    #slp1=msg.data1[1]
    #step1=msg.data1[2]
    #obst1=msg.data1[3]
    #dslp1=msg.data1[4]
    #dstep1=msg.data1[5]
     
    #x.append(seconds)
    #y.append(xm)
        
    #y = np.array([y1,y2,y3,y4])
    output=np.hstack((x,y))
    #print(y.shape)
    
    ex='.csv'
    filename=name+ex
    saved_data='saved_data/'
    save=saved_data+filename
    np.savetxt(save, output, delimiter=',')

      
        
  
def main():
    rospy.init_node('Data_Recorder')
    
    centroids_topic="/TPm"
    # Set up your subscriber and define its callback
    rospy.Subscriber(centroids_topic, cent, msg_callback)
    
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()





