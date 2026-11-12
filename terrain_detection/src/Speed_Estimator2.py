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

# Instantiate CvBridge
bridge = CvBridge()
first_frame=0
prevgray=0
val=np.array([])
ang=np.array([])
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
val=np.array([])
ang=np.array([])
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
    
def msg_callback(image_msg, imu_msg):
    global first_frame, prevgray,val,ang,color,lk_params,feature_params,p0
    #image section=============================
    cv2_img = bridge.imgmsg_to_cv2(image_msg, "bgr8")
    #cv2.imshow('image',cv2_img)
    #cv2.waitKey(3)
    
    #p1=

    gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    #gray = gray[0:200, 0:400]

    #fast = cv2.FastFeatureDetector_create()

    # find and draw the keypoints

    
    #gray=cv2.resize(gray, (500,400))
    mask = np.zeros_like(gray)

    if first_frame==0:
       prevgray=gray
       first_frame=1
       #cv2.waitKey(3)

       #p0 = cv2.goodFeaturesToTrack(prevgray, mask = None, **feature_params)
    else:
      #  p0 = fast.detect(prevgray,None)#cv2.goodFeaturesToTrack(prevgray, mask = None, **feature_params)
      #  LK_pts=np.empty((0,1,2), np.float32)
      #  for pts  in p0:
      #       x, y = pts.pt
      #       LK_pts=np.append(LK_pts,np.array([[[x,y]]],dtype=np.float32),axis=0)
      #  p0=LK_pts 
       p0 = cv2.goodFeaturesToTrack(prevgray, mask = None, **feature_params)    
       angle=0 
       mag=0
       dir=np.array([])
       frame=gray

       if p0 is not None:
          p1, st, err = cv2.calcOpticalFlowPyrLK(prevgray, gray, p0, None, **lk_params)
          good_new = p1[st==1]
          good_old = p0[st==1]
          dir=good_new-good_old

          if dir.size>0:
             dir=dir.sum(axis=0)
             angle=np.arctan2(dir[0],dir[1])*(180/np.pi) 
             X=dir[0]
             Y=dir[1]
             mag=np.sqrt(X*X+Y*Y)

          for i,(new,old) in enumerate(zip(good_new,good_old)):
             a,b = new.ravel()
             c,d = old.ravel()
             mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
             frame = cv2.circle(gray,(a,b),5,color[i].tolist(),-1)
          img = cv2.add(frame,mask)
          #img=gray
          gx=-angle
          gx=gx*math.pi/180
          arrow_length=int(min(50,mag))
          xx=int(math.sin(gx)*arrow_length)
          yy=int(math.cos(gx)*arrow_length)

          colors = {'blue': (255, 0, 0), 'green': (0, 255, 0), 'red': (0, 0, 255), 'yellow': (0, 255, 255), 'magenta': (255, 0, 255), 'cyan': (255, 255, 0), 'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (125, 125, 125), 'rand': np.random.randint(0, high=256, size=(3,)).tolist(), 'dark_gray': (50, 50, 50), 'light_gray': (220, 220, 220)}
          cv2.arrowedLine(img, (212, 120), (xx+212,120-yy), colors['red'], 3, 8, 0, 0.1)
          
          pub = rospy.Publisher('image', Image, queue_size=10)
          imgMsg = bridge.cv2_to_imgmsg(img, "mono8")
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
       print(mag)
       val=np.append(val,mag)
       ang=np.append(ang,angle)
       mag_ang=np.array([val,ang])
       mag_ang=np.transpose(mag_ang)
       savetxt('fw_sp_sh.csv', mag_ang, delimiter=',')
       


        # Now update the previous frame and previous points
       prevgray = gray
       #p0 = good_new.reshape(-1,1,2)



      
        
  
def main():
    rospy.init_node('Speed_Estimator')
    
    imu="/camera/imu" # /camera/imu or /imu/data
    image="/camera/color/image_raw"# /camera/depth/image_rect_raw
    image_msg=message_filters.Subscriber(image, Image)
    imu_msg=message_filters.Subscriber(imu,Imu)
    # Set up your subscriber and define its callback
    ts = message_filters.ApproximateTimeSynchronizer([image_msg, imu_msg], 5, 0.1, allow_headerless=True)
    ts.registerCallback(msg_callback)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
    #out.release()
    #cv2.destroyAllWindows()



