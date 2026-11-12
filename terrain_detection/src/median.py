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

from scipy.signal import medfilt

from terrain_detection.msg import cent
#from numpy import savetxt

# Instantiate CvBridge
bridge = CvBridge()
#global x
x=[]
#global y
y1=np.zeros((9))
y2=np.zeros((9))
y3=np.zeros((9))
#y4=np.zeros((1,6))
#y5=np.zeros((1,6))
#x=np.zeros((1,1))
#first_time=0
#y=[0,0,0,0,0,0]
#y=np.zeros((1,16))
#bool c
count=0


#print(f.read()) 
msgm=cent()

#I HAVE PROBLAM IN ASSGINING LOCAL GLOBAL VARIABLE CHECK YOUR CODES IN PYT3 GOOGLE DRIVE(SOLVED ;) )
def msg_callback(msg,pub):
    #print("recieving data")
    
    global y1,y2,y3,count,msgm
    count=count+1
    if(count>3):
      count=3
    if(count==1):
      y1[0]=msg.TDL1
      y1[1]=msg.tc1
      y1[2]=msg.yc1
      y1[3]=msg.TDL2
      y1[4]=msg.tc2
      y1[5]=msg.yc2
      y1[6]=msg.TDL3
      y1[7]=msg.tc3
      y1[8]=msg.yc3
    elif(count==2):
      y2[0]=msg.TDL1
      y2[1]=msg.tc1
      y2[2]=msg.yc1
      y2[3]=msg.TDL2
      y2[4]=msg.tc2
      y2[5]=msg.yc2
      y2[6]=msg.TDL3
      y2[7]=msg.tc3
      y2[8]=msg.yc3
    elif(count>=3):
      y3[0]=msg.TDL1
      y3[1]=msg.tc1
      y3[2]=msg.yc1
      y3[3]=msg.TDL2
      y3[4]=msg.tc2
      y3[5]=msg.yc2
      y3[6]=msg.TDL3
      y3[7]=msg.tc3
      y3[8]=msg.yc3
      y=ms_filter(y1,y2,y3)
      msgm.TDL1=int(y[0])
      msgm.tc1 =y[1]
      msgm.yc1 =y[2]
      msgm.TDL2=int(y[3])
      msgm.tc2 =y[4]
      msgm.yc2 =y[5]
      msgm.TDL3=int(y[6])
      msgm.tc3 =y[7]
      msgm.yc3 =y[8]
      
      msgm.step1=False
      msgm.step2=False
      msgm.step3=False

      if(int(y[0])>0):
         msgm.step1=True
      if(int(y[3])>0):
         msgm.step2=True   
      if(int(y[6])>0):
         msgm.step3=True

      y1[0]=y2[0]
      y1[1]=y2[1]
      y1[2]=y2[2]
      y1[3]=y2[3]
      y1[4]=y2[4]
      y1[5]=y2[5]
      y1[6]=y2[6]
      y1[7]=y2[7]
      y1[8]=y2[8]
      ###########
      y2[0]=y3[0]
      y2[1]=y3[1]
      y2[2]=y3[2]
      y2[3]=y3[3]
      y2[4]=y3[4]
      y2[5]=y3[5]
      y2[6]=y3[6]
      y2[7]=y3[7]
      y2[8]=y3[8]
      #y2=y3
      # y1[0]=y[0,1]
      # y1[1]=y[1,1]
      # y1[2]=y[2,1]
      # y1[3]=y[3,1]
      # y1[4]=y[4,1]
      # y1[5]=y[5,1]
      # y1[6]=y[6,1]
      # y1[7]=y[7,1]
      # y1[8]=y[8,1]
      count=3      
      pub.publish(msgm)
    
    #if(count<3):
    #  pub.publish(msg)
    #else:
      

    


    
def ms_filter(y1,y2,y3):
    y=np.zeros((9,3))
    for i in range(9): 
      y[i,:]=medfilt([y1[i],y2[i],y3[i]],3)  
    if y[0,1]==y1[0]: #and y[3,1]==y1[3]: #and y[6,1]==y1[6]:  
       return y1 
    elif y[0,1]==y2[0]: #and y[3,1]==y2[3]: #and y[6,1]==y2[6]:
       return y2
    else:# y[0,1]==y3[0]: #and y[3,1]==y3[3]: #and y[6,1]==y3[6]:
       return y3 
   #  else:
   #     yx=[0,0,0,0,0,0,0,0,0]
   #     for i in range(9): 
   #         yx[i]=y[i,1]
   #     return yx
      
        
  
def main():
    rospy.init_node('Median_Filter')
    
    centroids_topic="/TP"
    # Set up your subscriber and define its callback
    pub = rospy.Publisher('/TPm', cent, queue_size=1)
    rospy.Subscriber(centroids_topic, cent, msg_callback,callback_args=pub)
    rate = rospy.Rate(10) # 10hz
    
    
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()





