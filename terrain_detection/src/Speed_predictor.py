# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 11:05:04 2019

@author: aldabbagh
"""
from curses.ascii import SP
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import pandas as pd
#from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from numpy import savetxt
from sklearn.gaussian_process import GaussianProcessRegressor 
#from sklearn import gaussian_process
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
#from sklearn.neural_network import MLPClassifier
import roslibpy
import time
from rospy_tutorials.msg import Floats
from scipy.signal import butter,filtfilt
from scipy.signal import find_peaks
import time
#from sensor_msgs.msg import Imu

#Defining global variables
Speed=0.0
Cadance=0.0
counter=0
window_size=200
samples=np.zeros(window_size)
temp=np.zeros(int(window_size/2))
Msg_p=False
features_array=np.zeros([1,11])
saved_cad=1
# cc=0
# winscc=300
# samcc=np.zeros(winscc)
# temp=np.zeros(int(winscc/2))

def cadance_cal(data):
    global saved_cad
    #data=data-np.mean(data)
    #data=butter_lowpass_filter(data,5,200,2)
    cad=0.0
    peaks, _ = find_peaks((-1*data),height=2.5,distance=100)#find_peaks((-1*data), height=0.5,distance=70)
    peaks2, _ = find_peaks((1*data),height=2.5,distance=100)
   # print(peaks)
    if len(peaks)>1:
       period=abs(peaks[0]-peaks[1])
       time=period*(1/200)
       cad= 1/time
       saved_cad=cad
    elif len(peaks2)>1:  
       period=abs(peaks2[0]-peaks2[1])
       time=period*(1/200)
       cad= 1/time
       saved_cad=cad 
    #elif len(peaks2)==1 and len(peaks)==1:
    #   period=abs(peaks[0]-peaks2[0])
    #   time=period*(1/200)
    #   cad= 1/time
   #    saved_cad=cad
       #print("hear")
    else:
       cad=saved_cad
       #savetxt('data1.csv', data, delimiter=',')
       #print('saved')
    return cad


#Defining functions 
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
    feature_m=np.zeros([x,9])
    
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
        #feature_m[i,3] =sum(np.square(d)) # Energy
        spec =np.abs(np.fft.fft(d))**2
        freq  =np.fft.fftfreq(d.size,0.005)
        idx = np.argsort(freq)
        spec=spec[idx]
        freq=freq[idx]
        spec=spec[100:200]
        freq=freq[100:200]
        feature_m[i,3:7]=spec[1:5] # spectrum (f1....f4)
        #feature_m[i,8]=np.sum(spec[1:5]) # sum fft energy
        feature_m[i,7]=np.max(d)         # max
        feature_m[i,8]=np.min(d)        # min
    return feature_m

def receive_msg(msg):
    #print(msg)
    global counter,samples,Speed,Cadance,Msg_p,features_array,temp
    linear_acceleration=msg['linear_acceleration']
    x=linear_acceleration['x']
    y=linear_acceleration['y']
    z=linear_acceleration['z']
    
    if counter<window_size:
       samples[counter]=np.sqrt(x*x+y*y+z*z)
       counter=counter+1     
    elif counter==window_size:       
       exfeatures=features(samples,window_size)
       Cadance=cadance_cal(samples)  
       if(abs(exfeatures[0,7])>0.7 or abs(exfeatures[0,8])>0.7 ) :
          Speed=classifier(exfeatures)
          Speed=round(Speed[0], 2)
       else:
          Speed=0   
       Cadance = round(Cadance, 1) 
       Step_size=round((Speed/Cadance),2)
       #if(Step_size>1.1):
       #   Step_size=1
      

       print(Speed,Cadance,Step_size )#print(Speed,Cadance,round((Speed/Cadance)+0.1,1))
       Msg_p=True
       counter=100
       temp=samples[100:200]   
       samples=np.zeros(window_size)      
       samples[0:100]=temp

   #+========cadance==============
   #  global cc,samcc,tempcc
   #  if cc<winscc:
   #     samcc[cc]=np.sqrt(x*x+y*y+z*z)
   #     cc=cc+1     
   #  elif cc==winscc:       
   #     Cadance=cadance_cal(samcc)      
   #     Cadance = round(Cadance, 1) 
   #     cc=150
   #     tempcc=samcc[150:300]   
   #     samcc=np.zeros(winscc)      
   #     samcc[0:150]=tempcc
    
   #     #time.sleep(0.8) 
   #  print(samcc)
       #features_array=np.vstack((features_array,exfeatures))
       #print the features
       #savetxt('features.csv', features_array, delimiter=',')
       #Speed=Speed+cadance
       #cadance=0.0
 





def classifier(input_features):   
    # Load from file
    pkl_filename = "speed_model7.pkl"
    with open(pkl_filename, 'rb') as file:
     clf_load = pickle.load(file)
    y_pred=clf_load.predict(input_features) 
    return y_pred

    # global train,gpr
    # if not train:
    #    data=pd.read_csv("ind_V4.csv")#combined
    #    X_train = data[['zcross','mean','sigmag','energy','f1','f2','f3','f4','sumfft','max','min']].values #'zcross','mean','sigmag','energy','f1','f2','f3','f4'
    #    y_train = data[['y']].values
    #    kernel = DotProduct() + WhiteKernel()
    #    gpr = GaussianProcessRegressor(kernel=kernel, random_state=0).fit(X_train, y_train.ravel())
    #    print('trained')
    #    train==True
        
        

def main():
    global Speed,Cadance,Msg_p
    
    client = roslibpy.Ros(host='localhost', port=9090)
    #client.on_ready(lambda: print('Is ROS connected?', client.is_connected))
    client.run()
    
    talker = roslibpy.Topic(client, '/Speed_Cadance', 'std_msgs/String')
    listener = roslibpy.Topic(client, '/camera/imu', 'sensor_msgs/Imu')
    
    while client.is_connected:
      
       listener.subscribe(receive_msg)
      
       if Msg_p==True:
          talker.publish(roslibpy.Message({'data':str([Speed,Cadance])}))
          Speed=None
          Cadance=None
          Msg_p=False

       
       #listener.subscribe(lambda message: print('Heard talking: ' + message['data']))
       #talker.publish(roslibpy.Message({'data': 'Hello World!'}))
       #print('Sending message...')
    #talker.advertise()
    #talker.unadvertise()

    #client.terminate()

    
 

    
    # infinit = 1
    # while infinit < 6:
    #   name="features.csv"
    #   data=pd.read_csv(name)#combined
    #   Input = data.columns 
    #   #
    #   x=np.zeros(11)
    #   x=x.reshape(1, -1) 
    #   for i in range(np.size(x)):
    #       x[0,i]=Input[i]
    #   y_pred = gpr.predict(x)
    #   print(y_pred)
    
    
    
    #i = 1
    #while i < 6:  
    #  y_pred = gpr.predict(X_test)     

   
if __name__ == '__main__':
	main() 
