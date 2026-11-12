#!/usr/bin/env python

from __future__ import print_function

from terrain_detection.srv import Classifier,ClassifierResponse
import rospy
#import sklearn

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
#from sklearn.neural_network import MLPClassifier

def handle_classifier(req):
    #print("Returning")
    pkl_filename = "modeltotal.pkl" #"svm_c2.pkl"
    #with open(pkl_filename, 'wb') as file:
    # pickle.dump(clf, file)
    # Load from file
    new=open(pkl_filename,'rb')
    #pickle.dump(clf_load,new, protocol=2)
    clf_load=pickle.load(new)
    new.close()
    #with open(pkl_filename, 'rb') as file:
    # clf_load = pickle.load(file)
    #x=numpy()[req.a,req.b,req.c,req.d] 
    x=np.zeros((1, 3))
    x[0,0]=req.b
    x[0,1]=req.c
    x[0,2]=req.d
    #x[0,3]=req.a
    #x[0,4]=req.e
    print("Receiving featurs....")
    y=clf_load.predict(x)

    #y=req.a + req.b + req.c+ req.d
    
    return ClassifierResponse(y)

def class_server():
    rospy.init_node('classifier_server')
    s = rospy.Service('classifier', Classifier, handle_classifier)
    print("Ready to classify...")
    rospy.spin()

if __name__ == "__main__":
    class_server()

