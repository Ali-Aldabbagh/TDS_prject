# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 11:05:04 2019

@author: aldabbagh
"""
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

def main():
    
    dataset=pd.read_csv("slowv3.csv")#combined
    #shuffle randomly
    data=dataset.sample(frac=1)
    X = data[['xc', 'yc', 'zc', 't','nop']].values
    Y = data[['Y']].values
    #print(Y)
    #X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
    
    ###########################ADAVANCED
    c=4#feautures
    nop_t=50
    X_train2=X[0,0:c]
    y_train2=Y[0]
    #y_train2=numpy.empty([])
    #X_train=[]
    print(len(X)) 
    for i in range(len(Y)):
         if X[i,4]>=nop_t:
            #X_train.extend(X[i])
            #c=c+1
            #print(X_train[c])
            #del X[i]
            X_train2=np.vstack((X_train2,X[i,0:c]))
            y_train2=np.vstack((y_train2,Y[i]))
            #X.pop(i)
            #X.size
            #X=np.delete(X,i,0)
    print((X_train2.shape))
    print(len(y_train2))        
    ###################################
           
         

    X_train=X[:,0:c]#X_train2#X, X_train2
    y_train=Y#Y#y_train2#Y,
    
    dataset=pd.read_csv("ind1_clear.csv")#combined
    #shuffle randomly
    data=dataset.sample(frac=1)
    X = data[['xc', 'yc', 'zc', 't','nop']].values
    Y = data[['Y']].values

    ###########################ADAVANCED
    print('test set...')
    
    X_test2=X[0,0:c]
    y_test2=Y[0]
    #y_train2=numpy.empty([])
    #X_train=[]
    print(len(X)) 
    for i in range(len(Y)):
         if X[i,4]>=nop_t:
            #X_train.extend(X[i])
            #c=c+1
            #print(X_train[c])
            #del X[i]
            X_test2=np.vstack((X_test2,X[i,0:c]))
            y_test2=np.vstack((y_test2,Y[i]))
            #X.pop(i)
            #X.size
            #X=np.delete(X,i,0)
    print((X_test2.shape))
    print(len(y_test2))        
    ###################################


    X_test=X[:,0:c]# X_test2# X
    y_test=Y#y_test2# Y
    
    #y_train=column_or_1d(y_train, warn=True)
    clf = SVC(kernel='rbf',gamma=0.15)
    clf = clf.fit(X_train,y_train.ravel())
    
    #load your model
    #with open('svm_c7.pkl', 'rb') as f:
    #    clf = pickle.load(f)

    output_predicted=clf.predict(X_test)
    #output=np.array()
    output=output_predicted.ravel()-y_test.ravel()
    g=0.0
    g1=0.0
    for i in range(len(output)):
        if output[i]==0:
            g=g+1

    g1=g/len(output)        
    print(g1,g,len(output))
    
    #output=np.vstack((output_predicted,y_test))
    #output=output.transpose
    #print(output)
    savetxt('data_out.csv', output, delimiter=',')
    
    ds=0.0
    dsp=0.0
    dr=0.0
    drp=0.0
    gr=0.0
    grp=0.0
    ur=0.0
    urp=0.0
    us=0.0
    usp=0.0
    for i in range(len(output)):
       if y_test[i]==1:
          ds=ds+1
          if output[i]==0:
             dsp=dsp+1
       elif y_test[i]==2:
          dr=dr+1
          if output[i]==0:
             drp=drp+1
       elif y_test[i]==3:
          gr=gr+1
          if output[i]==0:
             grp=grp+1
       elif y_test[i]==4:
          ur=ur+1
          if output[i]==0:
             urp=urp+1
       elif y_test[i]==5:
          us=us+1
          if output[i]==0:
             usp=usp+1

    print('Resutls are:')         
    print('ground=',grp,gr,grp/gr)
    print("upstairs=",usp,us,usp/us)
    print("downstairs=",dsp,ds,dsp/ds)
    print("upramp=",urp,ur,urp/ur)
    print("downramp=",drp,dr,drp/dr)
    
    #Xlsvm=["G","US","DS","UR","DR"]      
    #Ylsvm=[grp/gr*100,usp/us*100,dsp/ds*100,urp/ur*100,drp/dr*100]
    #plt.bar(Xlsvm,Ylsvm,color = 'r', width = 0.5)
    #########################################################################
    

if __name__ == '__main__':
	main() 
