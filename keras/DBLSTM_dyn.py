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
x_train = np.load('tmp/train_source.dtw.dyn.npy')#Source mcep
y_train = np.load('tmp/train_target.dtw.npy')[:,:-2,:]#Target mcep

print('Loading acoustic validation data...')
x_valid = np.load('tmp/test_source.dtw.dyn.npy')#Source mcep
y_valid = np.load('tmp/test_target.dtw.npy')[:,:-2,:]#Target mcep

# Hyper-parameter settings
batch_size = 32
epcho_times = 800
### LSTM settings
DBLSTM_cells = 512

# initialize the input of network
input = Input(shape=x_train.shape[1:], name = 'mcep_input')
maksed_input = Masking(mask_value=0.)(input)

# # apply DBLSTM
DBLSTM_layer_1 = Bidirectional(LSTM(DBLSTM_cells,return_sequences=True))(maksed_input)
output_DBLSTM = Bidirectional(LSTM(DBLSTM_cells,return_sequences=True))(DBLSTM_layer_1)
output = TimeDistributed(Dense(y_train.shape[2], activation= 'linear'),name ='mcep_output')(output_DBLSTM)

model = Model(inputs = input, outputs = output)
model.compile(optimizer = 'adam',
        loss={'mcep_output': 'MSE'},
        metrics=[])

saveName = 'models/DBLSTM_dyn'
open(saveName + '_model.json', 'w').write(model.to_json())
print('Saving the model...')
checkPointer = ModelCheckpoint(saveName + '_weights.hdf5', save_best_only = True)
earlyStopper = EarlyStopping(monitor='val_loss', patience= 5)

print('Compiling the model...')
model.fit({'mcep_input': x_train},
        {'mcep_output': y_train},
        batch_size=batch_size,
        epochs=epcho_times,
        validation_data=[{'mcep_input': x_valid},
            {'mcep_output': y_valid}],
        callbacks=[checkPointer, earlyStopper])
