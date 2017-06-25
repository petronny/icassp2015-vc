#!/bin/python3
import sys
import numpy as np
import sklearn.preprocessing
from sklearn.externals import joblib

prefix=sys.argv[1]
filelist=sys.stdin.readlines()
features=[]
max_frame=1600

for i in filelist:
    i=i.strip('\n')
    print(i,end='\r')
    feature=np.genfromtxt(i)
    features.append(feature[:,1:])

if prefix.find('train')>=0 and prefix.find('dtw')<0:
    tmp=np.row_stack(features)
    scaler=sklearn.preprocessing.StandardScaler().fit(tmp)
    joblib.dump(scaler,prefix+'.scaler.pkl')
else:
    scaler=joblib.load(prefix.replace('test','train').replace('.dtw','')+'.scaler.pkl')

for i in range(0,len(features)):
    if features[i].shape[0] > max_frame:
        print('Max frame length', max_frame, 'is smaller than',feature.shape[0])
    else:
        features[i]=np.concatenate((scaler.transform(features[i]),np.zeros((max_frame-features[i].shape[0],features[i].shape[1]))))
features=np.stack(features)

print('\n'+prefix+'.npy')
print(features.shape)
np.save(prefix+'.npy',features)

d=features[:,1:,:]-features[:,:-1,:]
dd=d[:,1:,:]-d[:,:-1,:]
dyn_features=np.concatenate((features[:,:-2,:],d[:,:-1,:],dd),axis=2)
print(prefix+'.dyn.npy')
print(dyn_features.shape)
np.save(prefix+'.dyn.npy',dyn_features)
