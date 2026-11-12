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
    dataset=pd.read_csv("features/modelTotal.csv")#combined,new_set
    #shuffle randomly
    data=dataset.sample(frac=1)
    X = data[[ 'yc', 'zc', 't']].values
    Y = data[['Y']].values
    #print(Y)
    #X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0) 
    X_train=X
    y_train=Y
    
    # dataset=pd.read_csv("second.csv")#combined
    # # #shuffle randomly
    # data=dataset.sample(frac=1)
    # X = data[['xc', 'yc', 'zc', 't']].values
    # Y = data[['Y']].values
    # X_test= X
    # y_test= Y
    
    #y_train=column_or_1d(y_train, warn=True)
    clf = SVC(kernel='rbf',gamma=0.15)
    clf = clf.fit(X_train,y_train.ravel())
    
    
    pkl_filename = "modeltotal.pkl"
    with open(pkl_filename, 'wb',2) as file:
     pickle.dump(clf, file)
     

    
    
    
    
    
    
    
    
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
