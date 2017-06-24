#!/bin/python3
from __future__ import print_function
import os
import sys
os.environ["KERAS_BACKEND"] = "theano"
os.environ["THEANO_FLAGS"] = "device=cuda"+sys.argv[1]
import numpy as np
np.random.seed(1337)
from keras.layers import *
from keras.optimizers import *
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import Model, model_from_json

# Read source speaker acoustic features and target speaker acoustic features from prepared database
print('Loading acoustic train data...')
x_train = np.load('tmp/train_source.dtw.npy')#Source mcep
y_train = np.load('tmp/train_target.dtw.npy')#Target mcep

print('Loading acoustic validation data...')
x_valid = np.load('tmp/test_source.dtw.npy')#Source mcep
y_valid = np.load('tmp/test_target.dtw.npy')#Target mcep

# Hyper-parameter settings
batch_size = 32
epcho_times = 800
### DNN settings
DNN_cells = 512

# initialize the input of network
input = Input(shape=x_train.shape[1:], name = 'mcep_input')
maksed_input = Masking(mask_value=0.)(input)

# # apply DNN
DNN_layer_1 = TimeDistributed(Dense(DNN_cells,activation= 'tanh'))(maksed_input)
DNN_layer_2 = TimeDistributed(Dense(DNN_cells,activation= 'tanh'))(DNN_layer_1)
DNN_layer_3 = TimeDistributed(Dense(DNN_cells,activation= 'tanh'))(DNN_layer_2)
DNN_layer_4 = TimeDistributed(Dense(DNN_cells,activation= 'tanh'))(DNN_layer_3)
DNN_layer_5 = TimeDistributed(Dense(DNN_cells,activation= 'tanh'))(DNN_layer_4)
DNN_layer_6 = TimeDistributed(Dense(DNN_cells,activation= 'tanh'))(DNN_layer_5)
output = TimeDistributed(Dense(x_train.shape[2], activation= 'linear'),name ='mcep_output')(DNN_layer_6)

model = Model(inputs = input, outputs = output)
model.compile(optimizer = 'adam',
              loss={'mcep_output': 'MSE'},
              metrics=[])

saveName = 'models/DNN'
open(saveName + '_model.json', 'w').write(model.to_json())
print('Saving the model...')
checkPointer = ModelCheckpoint(saveName + '_weights.hdf5', save_best_only = True)
earlyStopper = EarlyStopping(monitor='val_loss', patience= 20)

print('Compiling the model...')
model.fit({'mcep_input': x_train},
          {'mcep_output': y_train},
          batch_size=batch_size,
          epochs=epcho_times,
          validation_data=[{'mcep_input': x_valid},
                           {'mcep_output': y_valid}],
          callbacks=[checkPointer, earlyStopper])
