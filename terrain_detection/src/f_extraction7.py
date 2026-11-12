import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import stats, optimize, interpolate
# load numpy array from csv file
from numpy import loadtxt
import pywt
from collections import Counter
import statistics
#from  scipy.fft import fft, ifft
from numpy import savetxt
from scipy.signal import butter,filtfilt

window_size=200


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
        #power_spectrum=np.square(np.abs(np.fft.rfft(d)))# Power spectrum
        #print(len(power_spectrum))
        #feature_m[i,4:(int(winsize/2)+5)]=power_spectrum
        spec =np.abs(np.fft.fft(d))**2
        freq  =np.fft.fftfreq(d.size,1/200)
        idx = np.argsort(freq)
        spec=spec[idx]
        freq=freq[idx]
        spec=spec[100:200]
        freq=freq[100:200]
        feature_m[i,4:8]=spec[1:5]
        feature_m[i,8]=np.sum(spec[1:5])
        feature_m[i,9]=np.max(d)
        feature_m[i,10]=np.min(d)
       




        
        

    #print(len(f2),f2) 
    #frequency=np.linspace(0, 60/2, len(f2))
    #plt.figure(4)
    #plt.plot(frequency, f2)
    #da=np.array([d[0:19],d[20:39]])    
    #print(da.shape)
    return feature_m,x,freq,spec

def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = 0.5 * fs  # Nyquist Frequency
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y
    


     

     
    
    

def main():
    
    print("Hello World!")

    data1 = loadtxt('datasetALL/ind1_Ar_1_08.csv', delimiter=',')
    data2 = loadtxt('datasetALL/ind1_Ed-1_44.csv', delimiter=',')
    data3 = loadtxt('datasetALL/ind1_Gm-1_44.csv', delimiter=',')
    data4 = loadtxt('datasetALL/ind1_Jn_1_3.csv', delimiter=',')
    data5 = loadtxt('datasetALL/ind1_Rn-1_55.csv', delimiter=',')
    data6 = loadtxt('datasetALL/ind1_Rul-1_4.csv', delimiter=',')
    data7 = loadtxt('datasetALL/ind1_Sb-1_16.csv', delimiter=',')
    data8 = loadtxt('datasetALL/ind1_Vr-1_76.csv', delimiter=',')
    data9 = loadtxt('datasetALL/ind2_Ar_1_4.csv', delimiter=',')
    data10 = loadtxt('datasetALL/ind2_Ed-1_26.csv', delimiter=',')
    data11 = loadtxt('datasetALL/ind2_Gm-1_25.csv', delimiter=',')
    data12 = loadtxt('datasetALL/ind2_Jn_1_11.csv', delimiter=',')
    data13 = loadtxt('datasetALL/ind2_Rn-1_34.csv', delimiter=',')
    data14 = loadtxt('datasetALL/ind2_Rul-1_44.csv', delimiter=',')
    data15 = loadtxt('datasetALL/ind2_Sb-1_17.csv', delimiter=',')
    data16 = loadtxt('datasetALL/ind2_Vr-1_47.csv', delimiter=',')  
    data17 = loadtxt('datasetALL/out1_Ar_1_27.csv', delimiter=',')
    data18 = loadtxt('datasetALL/out1_Ed-1_35.csv', delimiter=',')
    data19 = loadtxt('datasetALL/out1_Gm-1_26.csv', delimiter=',')
    data20 = loadtxt('datasetALL/out1_Jn_1_37.csv', delimiter=',')
    data21 = loadtxt('datasetALL/out1_Rn-1_5.csv', delimiter=',')
    data22 = loadtxt('datasetALL/out1_Rul-1_34.csv', delimiter=',')
    data23 = loadtxt('datasetALL/out1_Sb-1_38.csv', delimiter=',')
    data24 = loadtxt('datasetALL/out1_Vr-1_48.csv', delimiter=',')
    data25 = loadtxt('datasetALL/out2_Ar_1_35.csv.csv', delimiter=',')
    data26 = loadtxt('datasetALL/out2_Ed-1_11.csv', delimiter=',')
    data27 = loadtxt('datasetALL/out2_Gm-1_26.csv.csv', delimiter=',')
    data28 = loadtxt('datasetALL/out2_Jn_1_35.csv', delimiter=',')
    data29 = loadtxt('datasetALL/out2_Rn-1_42.csv', delimiter=',')
    data30 = loadtxt('datasetALL/out2_Rul-1_46.csv', delimiter=',')
    data31 = loadtxt('datasetALL/out2_Sb-1_33.csv', delimiter=',')
    data32 = loadtxt('datasetALL/out2_Vr-1_44.csv', delimiter=',')  
    
    data33 = loadtxt('datasetALL/ALI_trails/Ali-1_25.csv', delimiter=',') 
    data34 = loadtxt('datasetALL/ALI_trails/Ali-1_28.csv', delimiter=',') 
    data35 = loadtxt('datasetALL/ALI_trails/Ali-1_37.csv', delimiter=',') 
    data36 = loadtxt('datasetALL/ALI_trails/Ali-1_55.csv', delimiter=',') 
    data37 = loadtxt('datasetALL/ALI_trails/Ali-1_56.csv', delimiter=',') 
    data38 = loadtxt('datasetALL/ALI_trails/Ali-1_61.csv', delimiter=',') 
    data39 = loadtxt('datasetALL/ALI_trails/Ali-1_69.csv', delimiter=',') 

 



    f1,x1,freq1,spec1=features(data1[:,4],window_size)   
    f2,x2,freq,spec2=features(data2[:,4],window_size)
    f3,x3,freq3,spec3=features(data3[:,4],window_size)
    f4,x4,freq,spec=features(data4[:,4],window_size)
    f5,x5,freq,spec=features(data5[:,4],window_size)
    f6,x6,freq,spec=features(data6[:,4],window_size)
    f7,x7,freq7,spec7=features(data7[:,4],window_size)  
    f8,x8,freq8,spec8=features(data8[:,4],window_size)   
    f9,x9,freq9,spec9=features(data9[:,4],window_size)
    f10,x10,freq10,spe10=features(data10[:,4],window_size)
    f11,x11,freq11,spec11=features(data11[:,4],window_size)
    f12,x12,freq12,spec12=features(data12[:,4],window_size)
    f13,x13,freq,spec=features(data13[:,4],window_size)
    f14,x14,freq7,spec7=features(data14[:,4],window_size)  
    f15,x15,freq,spec=features(data15[:,4],window_size)
    f16,x6,freq7,spec7=features(data16[:,4],window_size)  
    f17,x1,freq1,spec1=features(data17[:,4],window_size)   
    f18,x2,freq,spec2=features(data18[:,4],window_size)
    f19,x3,freq3,spec3=features(data19[:,4],window_size)
    f20,x4,freq,spec=features(data20[:,4],window_size)
    f21,x5,freq,spec=features(data21[:,4],window_size)
    f22,x6,freq,spec=features(data22[:,4],window_size)
    f23,x7,freq7,spec7=features(data23[:,4],window_size)  
    f24,x8,freq8,spec8=features(data24[:,4],window_size)   
    f25,x9,freq9,spec9=features(data25[:,4],window_size)
    f26,x10,freq10,spe10=features(data26[:,4],window_size)
    f27,x11,freq11,spec11=features(data27[:,4],window_size)
    f28,x12,freq12,spec12=features(data28[:,4],window_size)
    f29,x13,freq,spec=features(data29[:,4],window_size)
    f30,x14,freq7,spec7=features(data30[:,4],window_size)  
    f31,x15,freq,spec=features(data31[:,4],window_size)
    f32,x6,freq7,spec7=features(data32[:,4],window_size)  

    f33,x6,freq7,spec7=features(data33[:,4],window_size)  
    f34,x6,freq7,spec7=features(data34[:,4],window_size)
    f35,x6,freq7,spec7=features(data35[:,4],window_size)  
    f36,x6,freq7,spec7=features(data36[:,4],window_size) 
    f37,x6,freq7,spec7=features(data37[:,4],window_size)  
    f38,x6,freq7,spec7=features(data38[:,4],window_size) 
    f39,x6,freq7,spec7=features(data39[:,4],window_size)  
    

    
    savetxt('out/ind1_Ar_1_08.csv',f1, delimiter=',')
    savetxt('out/ind1_Ed-1_44.csv',f2, delimiter=',')
    savetxt('out/ind1_Gm-1_44.csv',f3, delimiter=',')
    savetxt('out/ind1_Jn_1_3.csv',f4, delimiter=',')
    savetxt('out/ind1_Rn-1_55.csv',f5, delimiter=',')
    savetxt('out/ind1_Rul-1_4.csv',f6, delimiter=',')
    savetxt('out/ind1_Sb-1_16.csv',f7, delimiter=',')
    savetxt('out/ind1_Vr-1_76.csv',f8, delimiter=',')
    savetxt('out/ind2_Ar_1_4.csv',f9, delimiter=',')
    savetxt('out/ind2_Ed-1_26.csv',f10, delimiter=',')
    savetxt('out/ind2_Gm-1_25.csv',f11, delimiter=',')
    savetxt('out/ind2_Jn_1_11.csv',f12, delimiter=',')
    savetxt('out/ind2_Rn-1_34.csv',f13, delimiter=',')
    savetxt('out/ind2_Rul-1_44.csv',f14, delimiter=',')
    savetxt('out/ind2_Sb-1_17.csv',f15, delimiter=',')
    savetxt('out/ind2_Vr-1_47.csv',f16, delimiter=',') 
    savetxt('out/out1_Ar_1_27.csv',f17, delimiter=',')
    savetxt('out/out1_Ed-1_35.csv',f18, delimiter=',')
    savetxt('out/out1_Gm-1_26.csv',f19, delimiter=',')
    savetxt('out/out1_Jn_1_37.csv',f20, delimiter=',')
    savetxt('out/out1_Rn-1_5.csv',f21, delimiter=',')
    savetxt('out/out1_Rul-1_34.csv',f22, delimiter=',')
    savetxt('out/out1_Sb-1_38.csv',f23, delimiter=',')
    savetxt('out/out1_Vr-1_48.csv',f24, delimiter=',')
    savetxt('out/out2_Ar_1_35.csv',f25, delimiter=',')
    savetxt('out/out2_Ed-1_11.csv',f26, delimiter=',')
    savetxt('out/out2_Gm-1_26.csv',f27, delimiter=',')
    savetxt('out/out2_Jn_1_35.csv',f28, delimiter=',')
    savetxt('out/out2_Rn-1_42.csv',f29, delimiter=',')
    savetxt('out/out2_Rul-1_46.csv',f30, delimiter=',')
    savetxt('out/out2_Sb-1_33.csv',f31, delimiter=',')
    savetxt('out/out2_Vr-1_44.csv',f32, delimiter=',') 

    savetxt('out/Ali-1_25.csv',f33, delimiter=',')
    savetxt('out/Ali-1_28.csv',f34, delimiter=',')
    savetxt('out/Ali-1_37.csv',f35, delimiter=',')
    savetxt('out/Ali-1_55.csv',f36, delimiter=',') 
    savetxt('out/Ali-1_56.csv',f37, delimiter=',')
    savetxt('out/Ali-1_61.csv',f38, delimiter=',')
    savetxt('out/Ali-1_69.csv',f39, delimiter=',')

    




    # f1,x1,freq1,spec1=features(data1[:,4],window_size)   
    # f2,x2,freq,spec2=features(data2[:,4],window_size)
    # f3,x3,freq3,spec3=features(data3[:,4],window_size)
    # f4,x4,freq,spec=features(data4[:,4],window_size)
    # f5,x5,freq,spec=features(data5[:,4],window_size)
    # f6,x6,freq,spec=features(data6[:,4],window_size)
    # f7,x7,freq7,spec7=features(data7[:,4],window_size)  
    # f8,x8,freq8,spec8=features(data8[:,4],window_size)   
    # f9,x9,freq9,spec9=features(data9[:,4],window_size)
    # f10,x10,freq10,spe10=features(data10[:,4],window_size)
    # f11,x11,freq11,spec11=features(data11[:,4],window_size)
    # f12,x12,freq12,spec12=features(data12[:,4],window_size)
    # f13,x13,freq,spec=features(data13[:,4],window_size)
    # f14,x14,freq14,spec14=features(data14[:,4],window_size)  
    # f15,x15,freq,spec=features(data15[:,4],window_size)
    # f16,x16,freq16,spec7=features(data16[:,4],window_size)  


    
    # savetxt('out/out1_Ar_1_3.csv',f1, delimiter=',')
    # savetxt('out/out1_Ed_1_38.csv',f2, delimiter=',')
    # savetxt('out/out1_Gm_1_32.csv',f3, delimiter=',')
    # savetxt('out/out1_Jn_1_4.csv',f4, delimiter=',')
    # savetxt('out/out1_Rn_1_58.csv',f5, delimiter=',')
    # savetxt('out/out1_Rul_1_3.csv',f6, delimiter=',')
    # savetxt('out/out1_Sb_1_4.csv',f7, delimiter=',')
    # savetxt('out/out1_Vr_1_56.csv',f8, delimiter=',')
    # savetxt('out/out2_Ar_1_42.csv',f9, delimiter=',')
    # savetxt('out/out2_Ed_1_22.csv',f10, delimiter=',')
    # savetxt('out/out2_Gm_1_34.csv',f11, delimiter=',')
    # savetxt('out/out2_Jn_1_38.csv',f12, delimiter=',')
    # savetxt('out/out2_Rn_1_46.csv',f13, delimiter=',')
    # savetxt('out/out2_Rul_1_65.csv',f14, delimiter=',')
    # savetxt('out/out2_Sb_1_44.csv',f15, delimiter=',')
    # savetxt('out/out2_Vr_1_57.csv',f16, delimiter=',') 
    #savetxt('1_25ImufA.csv', f1, delimiter=',')
    # savetxt('1_28ImufA.csv', f2, delimiter=',')
    # savetxt('1_43ImufA.csv', f3, delimiter=',')
    # savetxt('1_56ImufA.csv', f4, delimiter=',')
    # savetxt('1_62ImufA.csv', f5, delimiter=',')
    # savetxt('1_63ImufA.csv', f6, delimiter=',')
    # savetxt('1_7ImufA.csv',  f7, delimiter=',')
 

    




    #plotting part 
    # x1=np.linspace(0,x1,num=(x1))
    # x3=np.linspace(0,x3,num=(x3))
    # x7=np.linspace(0,x7,num=(x7))
    
    # t1=np.linspace(0,len(data1),num=(len(data1)))
    # t3=np.linspace(0,len(data3),num=(len(data3))) 
    # t7=np.linspace(0,len(data7),num=(len(data7)))

    
   

    # plt.figure(10)
    # plt.title('filter')
    # plt.plot(t1,butter_lowpass_filter(data1[:,4],5,200,2),color='blue')
    # plt.plot(t3,butter_lowpass_filter(data3[:,4],5,200,2),color='green')
    # plt.plot(t7,butter_lowpass_filter(data7[:,4],5,200,2),color='red')


    # print(len(x7),len(f7))
    # plt.figure(1)
    # plt.title('Zero crossing ')
    # plt.scatter(x1,f1[:,0],color='blue')
    # plt.scatter(x3,f3[:,0],color='green')
    # plt.scatter(x7,f7[:,0],color='red')
    

    # plt.figure(2)
    # plt.title('Mean ')
    # plt.scatter(x1,f1[:,1],color='blue')
    # plt.scatter(x3,f3[:,1],color='green')
    # plt.scatter(x7,f7[:,1],color='red')
   
    
    # plt.figure(3)
    # plt.title('Signal magnitude area ')
    # plt.scatter(x1,f1[:,2],color='blue')
    # plt.scatter(x3,f3[:,2],color='green')
    # plt.scatter(x7,f7[:,2],color='red')

    # plt.figure(4)
    # plt.title('Energy ')
    # plt.scatter(x1,f1[:,3],color='blue')
    # plt.scatter(x3,f3[:,3],color='green')
    # plt.scatter(x7,f7[:,3],color='red')

    # plt.figure(5)
    # plt.title('Power Spectrum (last window sample)')
    # plt.plot(freq1[1:5], f1[1,4:8],color='blue')
    # plt.plot(freq3[1:5], f3[1,4:8],color='green')
    # plt.plot(freq7[1:5], f7[1,4:8],color='red')


    # # plt.figure(6)
    # # plt.title('Power Spectrum New')
    # # idx1 = np.argsort(freq1)
    # # spec1=spec1[idx1]
    # # freq1=freq1[idx1]
    # # spec1=spec1[100:200]
    # # freq1=freq1[100:200]
    # # plt.plot(freq1, spec1)

    # # idx3 = np.argsort(freq3)
    # # spec3=spec3[idx3]
    # # freq3=freq3[idx3]
    # # spec3=spec3[100:200]
    # # freq3=freq3[100:200]
    # # plt.plot(freq3, spec3,color='green')

    # # idx7 = np.argsort(freq7)
    # # spec7=spec7[idx7]
    # # freq7=freq7[idx7]
    # # spec7=spec7[100:200]
    # # freq7=freq7[100:200]
    # # plt.plot(freq7, spec7,color='red')
    # #plt.figure(7)
    # #plt.plot(freq1,spec1)
    # #print(np.max(spec7))
    # #result = np.where(spec7[idx7] == np.amax(spec7[idx7]))
    # #print(idx7)

    # plt.show()

    


if __name__ == "__main__":
    main()
