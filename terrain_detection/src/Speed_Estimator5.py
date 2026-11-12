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

# Instantiate CvBridge
bridge = CvBridge()
first_frame=0
prevgray=0

p0=0
#fourcc = cv2.VideoWriter_fourcc(*'XVID')


# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.1,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))
f_size=21#9,15
x_arr=np.zeros(f_size)
y_arr=np.zeros(f_size)
val=np.array([])
ang=np.array([])
speed=np.array([])
speed_dir=np.array([])
count=0



#out = cv2.VideoWriter('go_slow.avi', fourcc, 20.0, (240, 424))

# def get_corners(frame_gray):
#     corner_track_params = dict(blockSize = 2, 
#                             ksize = 3, 
#                            k = 0.04)
#     dst = cv2.cornerHarris(frame_gray, **corner_track_params)
#     dst = cv2.dilate(dst, None)
#     ret, dst1 = cv2.threshold(dst,0.9*dst.max(),255,0)
#     dst1 = np.uint8(dst1)
#     ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst1)
#     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
#     corners = cv2.cornerSubPix(frame_gray, np.float32(centroids), (5,5), (-1,-1), criteria)
#     corners = corners.reshape(-1, 1, 2)
#     return corners
    
def msg_callback(image_msg, pub):
    global first_frame, prevgray,val,ang,color,lk_params,feature_params,p0,mag_ang,count,x_arr,y_arr,speed,speed_dir
    #image section=============================
    cv2_img = bridge.imgmsg_to_cv2(image_msg, "bgr8")
    #cv2.imshow('image',cv2_img)
    #cv2.waitKey(3)
    
    #p1=

    gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    gray = gray[0:180,:]
    #cv2.imshow('image',gray)
    #cv2.waitKey(1)

    fast = cv2.FastFeatureDetector_create()

    # find and draw the keypoints

    
    #gray=cv2.resize(gray, (500,400))
    mask = np.zeros_like(gray)

    if first_frame==0:
       prevgray=gray
       first_frame=1
       #cv2.waitKey(3)

       #p0 = cv2.goodFeaturesToTrack(prevgray, mask = None, **feature_params)
    else:
       kp = fast.detect(prevgray,None)#cv2.goodFeaturesToTrack(prevgray, mask = None, **feature_params)
       LK_pts=np.empty((0,1,2), np.float32)
       for pts  in kp:
            x, y = pts.pt
            LK_pts=np.append(LK_pts,np.array([[[x,y]]],dtype=np.float32),axis=0)
       p0=LK_pts 
       #p0 = cv2.goodFeaturesToTrack(prevgray, mask = None, **feature_params)    
       angle=0 
       mag=0
       dir=np.array([])
       img=cv2_img#gray
       #img = cv2.drawKeypoints(img, kp,outImage = None, color=(255,0,0))
       #print(p0)

       if p0 is not None:
          p1, st, err = cv2.calcOpticalFlowPyrLK(prevgray, gray, p0, None, **lk_params)
          if p1 is not None:
             good_new = p1[st==1]
             good_old = p0[st==1]
             dir=good_new-good_old
          else:
             dir=np.array([])
  


          if dir.size>0:
             dir=dir.sum(axis=0)
             
             X=dir[0]
             Y=dir[1]

             #print(mag,angle)
             speed_dir=np.append(speed_dir,np.sqrt(X*X+Y*Y)/len(kp))
             #savetxt('1_7_41ws.csv', speed_dir, delimiter=',')


             #print(speed_mag)
             if count==f_size:
                #mag=medfilt(mag_arr,f_size) 
                
                x_arr=shift(x_arr, 1, cval=X)
                y_arr=shift(y_arr, 1, cval=Y)

                x=medfilt(x_arr,f_size) 
                y=medfilt(y_arr,f_size) 

                x=x[int(f_size/2)]
                y=y[int(f_size/2)]


                angle=np.arctan2(x,y)*(180/np.pi) 
                mag=np.sqrt(x*x+y*y)

                

               
                gx=-angle
                gx=gx*math.pi/180
                arrow_length=int(min(100,mag/50))
                xx=int(math.sin(gx)*arrow_length)
                yy=int(math.cos(gx)*arrow_length)
                colors = {'blue': (255, 0, 0), 'green': (0, 255, 0), 'red': (0, 0, 255), 'yellow': (0, 255, 255), 'magenta': (255, 0, 255), 'cyan': (255, 255, 0), 'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (125, 125, 125), 'rand': np.random.randint(0, high=256, size=(3,)).tolist(), 'dark_gray': (50, 50, 50), 'light_gray': (220, 220, 220)}
                cv2.arrowedLine(img, (212, 120), (xx+212,120-yy), colors['red'], 3, 8, 0, 0.1)
                #count=0
                #print(mag,angle)
                val=np.append(val,mag)
                ang=np.append(ang,angle)
                speed=np.append(speed,mag/len(kp))
                mag_ang=np.array([val,ang,speed])
                mag_ang=np.transpose(mag_ang)
                savetxt('1_7_51.csv', mag_ang, delimiter=',')

             else:
                x_arr[count]=X
                y_arr[count]=Y
                count=count+1
          
         
          imgMsg = bridge.cv2_to_imgmsg(img, "bgr8")#
          pub.publish(imgMsg)

          #cv2.imshow('frame',img)
          #cv2.waitKey(3)
          #out.write(img)
      
          
          #for i,(new,old) in enumerate(zip(good_new,good_old)):
          #    a,b = new.ravel()
          #    c,d = old.ravel()
          #    mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
          #    frame = cv2.circle(gray,(a,b),5,color[i].tolist(),-1)
          #img = cv2.add(frame,mask)
          #cv2.imshow('frame',img)
          
         #cv2.waitKey(1)  
       #print("start")
    #    print(mag,angle)
    #    val=np.append(val,mag)
    #    ang=np.append(ang,angle)
    #    mag_ang=np.array([val,ang])
    #    mag_ang=np.transpose(mag_ang)
    #    savetxt('right_sp_fast.csv', mag_ang, delimiter=',')
       


        # Now update the previous frame and previous points
       prevgray = gray
       print("ok")
       #p0 = good_new.reshape(-1,1,2)



      
        
  
def main():
    rospy.init_node('Speed_Estimator')
    
    #imu="/camera/imu" # /camera/imu or /imu/data
    image="/camera/color/image_raw"# /camera/depth/image_rect_raw
    #image_msg=message_filters.Subscriber(image, Image)
    #imu_msg=message_filters.Subscriber(imu,Imu)
    # Set up your subscriber and define its callback
    #ts = message_filters.ApproximateTimeSynchronizer([image_msg, imu_msg], 5, 0.1, allow_headerless=True)
    #ts.registerCallback(msg_callback)
    pub = rospy.Publisher('image', Image, queue_size=1)
    rospy.Subscriber(image, Image, msg_callback,callback_args=pub)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
    #out.release()
    #cv2.destroyAllWindows()



