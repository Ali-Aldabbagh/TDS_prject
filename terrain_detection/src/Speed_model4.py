# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 11:05:04 2019

@author: aldabbagh
"""
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from numpy import savetxt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
#from sklearn.neural_network import MLPClassifier


        
        

def main():

    data=pd.read_csv("ind_V4.csv")#combined
    X_train = data[['zcross','mean','sigmag','energy','f1','f2','f3','f4','sumfft','max','min']].values #'zcross','mean','sigmag','energy','f1','f2','f3','f4'
    y_train = data[['y']].values

    data=pd.read_csv("out2_V4.csv")#combined
    X_test = data[['zcross','mean','sigmag','energy','f1','f2','f3','f4','sumfft','max','min']].values #'zcross','mean','sigmag','energy','f1','f2','f3','f4'
    y_test = data[['y']].values
    #data=data.values
    
    
    #X = data[:,0:4]
    #Y = data[:,5]

    #print(Y)
    #X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=0) 
    #X_train=X
    #y_train=Y
    
    # dataset=pd.read_csv("second.csv")#combined
    # # #shuffle randomly
    # data=dataset.sample(frac=1)
    # X = data[['xc', 'yc', 'zc', 't']].values
    # Y = data[['Y']].values
    # X_test= X
    # y_test= Y
    
    #Model selection 
    
    #clf = SVR(kernel='linear', C=100, gamma='auto')
    clf= SVR(kernel='rbf', C=10, gamma=0.1, epsilon=.1) 
    #clf= SVR(kernel='precomputed', C=100, gamma=0.01, epsilon=.1) 
    #clf= SVR(kernel='sigmoid', C=100, gamma=0.1, epsilon=.1) 
    #clf= SVR(kernel='poly', C=100, gamma='auto', degree=3, epsilon=.1,coef0=1)
    
    clf= clf.fit(X_train,y_train.ravel())
    
    kernel = DotProduct() + WhiteKernel()
    gpr = GaussianProcessRegressor(kernel=kernel, random_state=0).fit(X_train, y_train.ravel())
    output2=np.array([gpr.predict(X_test)])
    #dataset=pd.read_csv("traning_speed_f.csv")#combined
    # # #shuffle randomly
    #data=dataset.sample(frac=1)
    #X_test = dataset[['x1','x2']].values
    #y_test = dataset[['y']].values
    
    
    output=np.array([clf.predict(X_test)])
    # #y_train=column_or_1d(y_train, warn=True)
    #print(output.shape)
    output=np.transpose(output)
    output2=np.transpose(output2)
    print(output2.shape)
    print(y_test.shape)
 
    output_final=np.hstack((output2,y_test))
    #output_final=np.transpose(output_final)
    #output=output_predicted
    
    
    print('Mean Absolute Error SVR:', metrics.mean_absolute_error(y_test, output)) 
    print('Mean Absolute Error Gaussian:', metrics.mean_absolute_error(y_test, output2)) 
    savetxt('data_out_Gaussain.csv', output_final, delimiter=',')


    #savetxt('data_out_SVR.csv', output_final, delimiter=',')
    
    # #output=np.array()
    # output=output_predicted.ravel()-y_test.ravel()
    # g=0
    # for i in range(len(output)):
    #     if output[i]==0:
    #         g=g+1
    # g=g/len(output)        
    # print(g)
    
    # #output=np.vstack((output_predicted,y_test))
    # #output=output.transpose
    # #print(output)
    # savetxt('data_out.csv', output, delimiter=',')
    
    # ds=0
    # dsp=0
    # dr=0
    # drp=0
    # gr=0
    # grp=0
    # ur=0
    # urp=0
    # us=0
    # usp=0
    # for i in range(len(output)):
    #    if y_test[i]==1:
    #       ds=ds+1
    #       if output[i]==0:
    #          dsp=dsp+1
    #    elif y_test[i]==2:
    #       dr=dr+1
    #       if output[i]==0:
    #          drp=drp+1
    #    elif y_test[i]==3:
    #       gr=gr+1
    #       if output[i]==0:
    #          grp=grp+1
    #    elif y_test[i]==4:
    #       ur=ur+1
    #       if output[i]==0:
    #          urp=urp+1
    #    elif y_test[i]==5:
    #       us=us+1
    #       if output[i]==0:
    #          usp=usp+1
    # print("ground=",grp,gr,grp/gr)
    # print("upstairs=",usp,us,usp/us)
    # print("downstairs=",ds,dsp,dsp/ds)
    # print("upramp=",ur,urp,urp/ur)
    # print("downramp=",dr,drp,drp/dr)
    
    
    
    
    
    
    
    
"""     # ==========Model selection============================================
    select_model=3   
    # 0 for SVR_rbf
    # 1 for SVR_Linear 
    # 2 for SVR_poly 
    # 3 Load yout svr model (change the file name at pickle.load instruction)
    
    # Regression models
    svr_rbf = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
    svr_lin = SVR(kernel='linear', C=100, gamma='auto')
    svr_poly = SVR(kernel='poly', C=100, gamma='auto', degree=1, epsilon=.1,coef0=1)
    
    
    # =====================importing the data===============  
    dataset=pd.read_csv("X2.csv")
    X = dataset[['month', 'day', 'hour', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES','DEWP','wd','WSPM','station']].values
    z=X[:,10]
    for i in range(len(z)):
      s=z[i]
      d=[ord(c) for c in s]
      b=np.sum(d)
      X[i,10]=b
             
      
    # =====================sperating the data into training and test sets(80% training, 20% test )
    if select_model!=3:
      y = dataset['PM2'].values
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    else: 
      X_test=X
      
    # =============Traning the model===========================
    if select_model==0:
      print("Runing the SVR_RBF...")  
      model=svr_rbf.fit(X_train, y_train) 
      y_pred=svr_rbf.predict(X_test)
      filename = 'SVR_RBF.sav'
      pickle.dump(model, open(filename, 'wb'))
      
      
    elif select_model==1:
      print("Runing the SVR_linear...") 
      model=svr_lin.fit(X_train, y_train) 
      y_pred=svr_lin.predict(X_test)
      filename = 'SVR_Linear.sav'
      pickle.dump(model, open(filename, 'wb'))
    elif select_model==2:
      print("Runing the SVR_Poly...")     
      model=svr_poly.fit(X_train, y_train) 
      y_pred=svr_poly.predict(X_test)
      filename = 'SVR_Poly_1.sav'
      pickle.dump(model, open(filename, 'wb'))
    # ============OR Load the Model========================
    elif select_model==3   :
      # load the model from disk
      filename = 'SVR_Linear.sav'   # SVR_poly_1_degree.sva OR 'SVR_RBF.sav' 
      model_load = pickle.load(open(filename, 'rb'))
      y_pred = model_load.predict(X_test)
      # saving the output
      df = pd.DataFrame({'PM2.5 Predicted':y_pred})
      df.to_csv('output_SVR_Linear.csv') 
     # ======================================================   
    
    if select_model != 3:
       df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
       df1 = df.head(25)
       df1.plot(kind='bar',figsize=(10,8))
       plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
       plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
       plt.show()
  
       print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  """ 
    
  

if __name__ == '__main__':
	main() 
