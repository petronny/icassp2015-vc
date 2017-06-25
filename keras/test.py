#!/bin/python3
from __future__ import print_function
import os
import sys
os.environ["KERAS_BACKEND"] = "theano"
os.environ["THEANO_FLAGS"] = "device=cuda"+sys.argv[1]
import numpy as np
from keras.layers import *
from keras.models import Model, model_from_json
import sklearn.preprocessing
from sklearn.externals import joblib

model_names = ['DNN', 'DNN_dyn', 'DBLSTM', 'DBLSTM_dyn']
testlist=open('tmp/testlist.txt').readlines()
scaler=joblib.load('tmp/train_target.scaler.pkl')

for name in model_names:

    print('Loading VC models: ' + name)
    saveName = 'models/' + name
    weightsPath = saveName + '_weights.hdf5'
    modelString = open(saveName + '_model.json', 'r').read()
    model = model_from_json(modelString)
    model.load_weights(weightsPath)
    model.predict_function = None
    model._function_kwargs = dict()

    print('Loading source speaker valid acoustic data...')
    if name.find('dyn')>=0:
        x_valid = np.load('tmp/test_source.dyn.npy')
    else:
        x_valid = np.load('tmp/test_source.npy')

    print('Generating acoustic features ...')
    Pred = model.predict(x_valid, batch_size=32, verbose=0)

    for i in range(0,len(testlist)):
        filename=testlist[i].strip('\n')
        print('Saving',filename[:-3]+'mcep.'+name+'.csv', end='\r')
        mcep=np.genfromtxt(filename[:-3]+'mcep.csv')
        length=mcep.shape[0]
        energy=mcep[:,0]
        energy=np.reshape(energy,energy.shape+(1,))
        if name.find('dyn')>=0:
            pred_mcep=Pred[i,:length,:Pred.shape[2]//3]
            #pred_d=Pred[i,:length,Pred.shape[2]//3:Pred.shape[2]//3*2]
            #pred_dd=Pred[i,:length,Pred.shape[2]//3*2:]
            #np.savetxt(filename[:-3]+'mcep.'+name+'.csv', pred_mcep)
            #np.savetxt(filename[:-3]+'d.'+name+'.csv', pred_d)
            #np.savetxt(filename[:-3]+'dd.'+name+'.csv', pred_dd)
            #os.system('x2x +af '+filename[:-3]+'mcep.'+name+'.csv'+' > '+filename[:-3]+'mcep.'+name+'.f')
            #os.system('x2x +af '+filename[:-3]+'d.'+name+'.csv'+' > '+filename[:-3]+'d.'+name+'.f')
            #os.system('x2x +af '+filename[:-3]+'dd.'+name+'.csv'+' > '+filename[:-3]+'dd.'+name+'.f')

            pred_mcep=scaler.inverse_transform(pred_mcep)
            pred_mcep=np.concatenate((energy,pred_mcep),axis=1)
            np.savetxt(filename[:-3]+'mcep.'+name+'.csv', pred_mcep)

            #os.system('mlpg -l49 -d '+filename[:-3]+'d.'+name+'.f'+
            #        ' -d '+filename[:-3]+'d.'+name+'.f '+
            #        filename[:-3]+'mcep.'+name+'.f'+
            #        ' | x2x +fa'+str(pred_mcep.shape[1])+' > '+filename[:-3]+'mcep.mlpg.'+name+'.csv')
            #pred_mcep=np.genfromtxt(filename[:-3]+'mcep.mlpg.'+name+'.csv')
            #pred_mcep=np.concatenate((energy,pred_mcep),axis=1)
            #np.savetxt(filename[:-3]+'mcep.mlpg'+name+'.csv', pred_mcep)
        else:
            pred_mcep=scaler.inverse_transform(pred_mcep)
            pred_mcep=np.concatenate((energy,Pred[i,:length,:]),axis=1)
            np.savetxt(filename[:-3]+'mcep.'+name+'.csv', pred_mcep)
    print()
