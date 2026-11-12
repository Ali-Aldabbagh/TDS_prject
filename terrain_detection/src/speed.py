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
import pickle
from scipy.signal import butter,filtfilt
import pandas as pd
from rospy_tutorials.msg import Floats


counter=0
window_size=200
samples=np.zeros(window_size)

def z_cross(data):
    zc=0
    for i in range (len(data)-1):
        x0=data[i]
        x1=data[i+1]
        if x0>0 and x1<0:
           zc=zc+1
        elif x0<0 and x1>0: 
           zc=zc+1
        elif (x0==0 and x1<0) or (x0==0 and x1>0):
           zc=zc+1
        elif (x0>0 and x1==0) or (x0<0 and x1==0) :
           zc=zc+1
    return zc

def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = 0.5 * fs  # Nyquist Frequency
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

    

def features(data,winsize):
    overlap=int(0.0*winsize)
    x=int(len(data)/(winsize))
    feature_m=np.zeros([x,11])
    
    for i in range(x):
        if(i==0):
           d = data[(i*winsize):((i+1)*winsize)]
        else:
           d = data[(i*winsize)-overlap:((i+1)*winsize)-overlap]
        
        m=np.mean(d)
        d=d-m
        d=butter_lowpass_filter(d,5,200,2)
        z=z_cross(d)
        feature_m[i,0] =z  # Zeros-crossing
        feature_m[i,1] =m  # Mean          
        feature_m[i,2] =sum(abs(d))  #Signal magnitude area
        feature_m[i,3] =sum(np.square(d)) # Energy
        spec =np.abs(np.fft.fft(d))**2
        freq  =np.fft.fftfreq(d.size,0.005)
        idx = np.argsort(freq)
        spec=spec[idx]
        freq=freq[idx]
        spec=spec[100:200]
        freq=freq[100:200]
        feature_m[i,4:8]=spec[1:5] # spectrum (f1....f4)
        feature_m[i,8]=np.sum(spec[1:5]) # sum fft energy
        feature_m[i,9]=np.max(d)        # max
        feature_m[i,10]=np.min(d)       # min
    return feature_m


  
def msg_callback(imu_msg1,pub):
    global counter,samples
    #pkl_filename = "speed_model2.pkl"
    #new=open(pkl_filename,'rb')
    #clf_load=pickle.load(new)
    #new.close()

    x=imu_msg1.linear_acceleration.x
    y=imu_msg1.linear_acceleration.y
    z=imu_msg1.linear_acceleration.z
  
    
    if counter<window_size:

       samples[counter]=np.sqrt(x*x+y*y+z*z)
       counter=counter+1

    elif counter==window_size:
  
       counter=0
       exfeatures=features(samples,window_size)
       freqs=exfeatures[0,4:8]
       result = np.where(freqs == np.max(freqs))
       index=result[0]
       
       index=index[0]
       cadance=index+1
       save_features=[]
       for i in range(11):
           save_features.append(exfeatures[0,i])
       

       
       print(exfeatures)
       pub.publish(save_features)
       
    
    

#def msg_callback2(clock_msg):
    # global timer_first,timer,Ct,nano_first
    # if Ct==False:
    #    timer_first=float(clock_msg.clock.secs)
    #    nano_first=float(clock_msg.clock.nsecs)
    #    Ct=True
    # timer=float(clock_msg.clock.secs-timer_first)
    # nano=float((clock_msg.clock.nsecs-nano_first)/1000000000)
    # timer=timer+nano
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
    pub=rospy.Publisher('features_val',Floats,queue_size = 10)
    rospy.Subscriber(imu1, Imu, msg_callback,callback_args=pub)
    
    #rospy.Subscriber('clock', Clock, msg_callback2)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
    #out.release()
    #cv2.destroyAllWindows()



