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
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('fxw.avi', fourcc, 20.0, (240, 424))

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = np.arctan2(fy, fx) #+ np.pi 
    v = np.sqrt(fx*fx+fy*fy)
    hsv = np.zeros((h, w, 3), np.uint8)
    #print(ang[0,0]*(180/np.pi))
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v, 255)# np.minimum(v*6, 255)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    #print np.mean(ang*180/np.pi)
    #np.median(ang*180/np.pi)
    #print np.mean(v)
    

    X=np.sum(fx)
    Y=np.sum(fy)
    angle=np.arctan2(X,Y)*(180/np.pi)
    mag = np.sqrt(X*X+Y*Y)
    print(mag)
    
    return bgr, angle, mag

def warp_flow(img, flow):
    h, w = flow.shape[:2]
    flow = -flow
    flow[:,:,0] += np.arange(w)
    flow[:,:,1] += np.arange(h)[:,np.newaxis]
    res = cv2.remap(img, flow, None, cv2.INTER_LINEAR)
    return res

def feature_numbers(frame):
    fast = cv2.FastFeatureDetector_create()
    # find and draw the keypoints
    kp = fast.detect(frame,None)
    img2 = cv2.drawKeypoints(frame, kp,outImage = None, color=(255,0,0))
    #print "Keypoints ", len(kp)
    #cv2.imshow('frame',img2)
    return len(kp)
    
def msg_callback(image_msg, imu_msg):
    global first_frame, prevgray,val,ang
    #image section=============================
    cv2_img = bridge.imgmsg_to_cv2(image_msg, "bgr8")
    #cv2.imshow('image',cv2_img)
    #cv2.waitKey(3)
    
    

    gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    gray = gray[300:900, 300:1500]
    #gray=cv2.resize(gray, (500,400))
    if first_frame==0:
       prevgray=gray
       first_frame=1
    else:
       flow_mat = None
       image_scale = 0.5
       nb_images = 1
       win_size = 15
       nb_iterations = 2
       deg_expansion = 5
       STD = 1.3
       extra = 0# obtain dense optical flow paramters
       flow = cv2.calcOpticalFlowFarneback(prevgray, gray,  
                                        flow_mat, 
                                        image_scale, 
                                        nb_images, 
                                        win_size, 
                                        nb_iterations, 
                                        deg_expansion, 
                                        STD, 
                                        0)                                                   
       prevgray = gray
       a, angle,mag= draw_hsv(flow)
       b= draw_flow(gray, flow)
       #grs = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
       #out.write(b)
        
       #kp=feature_numbers(gray)
       #kp=kp/9
       #if kp>0:
       #   d=np.sum(grs)/kp#(kp+10000)
       #else:
          #d=np.sum(grs)
       val=np.append(val,mag)
       ang=np.append(ang,angle)
       mag_ang=np.array([val,ang])
       mag_ang=np.transpose(mag_ang)
       savetxt('fw_dans.csv', mag_ang, delimiter=',')
       #val=np.append(val,d)
       #print(np.sum(grs))   
       #savetxt('out1.csv', val, delimiter=',')
       # Dictionary containing some colors
       gx=-angle
       gx=gx*math.pi/180
       xx=int(math.sin(gx)*50)
       yy=int(math.cos(gx)*50)
       colors = {'blue': (255, 0, 0), 'green': (0, 255, 0), 'red': (0, 0, 255), 'yellow': (0, 255, 255), 'magenta': (255, 0, 255), 'cyan': (255, 255, 0), 'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (125, 125, 125), 'rand': np.random.randint(0, high=256, size=(3,)).tolist(), 'dark_gray': (50, 50, 50), 'light_gray': (220, 220, 220)}
       cv2.arrowedLine(b, (212, 120), (xx+212,120-yy), colors['red'], 3, 8, 0, 0.1)
       pub = rospy.Publisher('image', Image, queue_size=10)
       imgMsg = bridge.cv2_to_imgmsg(b, "bgr8")
       pub.publish(imgMsg)
          
       #cv2.imshow('flow', b)
       #cv2.imshow('flow HSV', grs)
       #cv2.imshow('gray', gray)
       #cv2.waitKey(3)
       #plt.plot(val,color='green')
       #plt.show()
       
       ch = 0xFF & cv2.waitKey(1)



      
        
  
def main():
    rospy.init_node('Speed_Estimator')
    #pub = rospy.Publisher('image', Image, queue_size=10)
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
    #cv2.destroyAllWindows()




