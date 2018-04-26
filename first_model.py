import time
import sys 
import os

import numpy as np

from keras.layers import Dense, Embedding, Input, Lambda
from keras.models import Model
from keras.losses import binary_crossentropy
from keras.metrics import binary_accuracy
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.optimizers import Adam
import keras.backend  as K

from util import save_object


def get_basic_model():

    #without any embedding
    input_shape =  (121,)

    inpu = Input(shape=input_shape)
    x = Dense(units=100, activation='relu')(inpu)    
    x = Dense(units=100, activation='relu')(x)    
    x = Dense(units=100, activation='relu')(x)    
    x = Dense(units=200, activation='relu')(x)    
    x = Dense(units=200, activation='relu')(x)
    x = Dense(units=200, activation='relu')(x)
    x = Dense(units=200, activation='relu')(x)
    x = Dense(units=1, activation='sigmoid')(x)

    return Model(inpu, x)    

def get_embedded_basic_model(embedded_size):


    # without embedding
    input_shape =  (121,)
    inpu = Input(shape=input_shape)

    embe = Embedding(243, embedded_size, input_length=121, mask_zero=True)(inpu)
    embe = Lambda(lambda x : K.sum(x, axis=1))(embe)
    x = Dense(units=100, activation='relu')(embe)    
    x = Dense(units=100, activation='relu')(x)    
    x = Dense(units=100, activation='relu')(x)    
    x = Dense(units=200, activation='relu')(x)    
    x = Dense(units=200, activation='relu')(x)
    x = Dense(units=200, activation='relu')(x)
    x = Dense(units=200, activation='relu')(x)
    x = Dense(units=1, activation='sigmoid')(x)

    return Model(inpu, x)    



def get_moderate_model():

    #without any embedding
    input_shape =  (121,)

    inpu = Input(shape=input_shape)
    x = Dense(units=200, activation='relu')(inpu)    
    x = Dense(units=200, activation='relu')(x)    
    x = Dense(units=200, activation='relu')(x)    
    x = Dense(units=200, activation='relu')(x)    
    x = Dense(units=400, activation='relu')(x)    
    x = Dense(units=400, activation='relu')(x)
    x = Dense(units=400, activation='relu')(x)
    x = Dense(units=400, activation='relu')(x)
    x = Dense(units=800, activation='relu')(x)
    x = Dense(units=1, activation='sigmoid')(x)

    return Model(inpu, x)    
    

def get_embedded_moderate_model(embedded_size):

    input_shape =  (121,)
    inpu = Input(shape=input_shape)

    embe = Embedding(243, embedded_size, input_length=121, mask_zero=True)(inpu)
    embe = Lambda(lambda x : K.sum(x, axis=1))(embe)
    x = Dense(units=200, activation='relu')(embe)    
    x = Dense(units=200, activation='relu')(x)    
    x = Dense(units=200, activation='relu')(x)    
    x = Dense(units=200, activation='relu')(x)    
    x = Dense(units=400, activation='relu')(x)    
    x = Dense(units=400, activation='relu')(x)
    x = Dense(units=400, activation='relu')(x)
    x = Dense(units=400, activation='relu')(x)
    x = Dense(units=800, activation='relu')(x)
    x = Dense(units=1, activation='sigmoid')(x)

    return Model(inpu, x)    
    

# from [0 0 0 1 1 0 -1 0 -1 0 1]
# to [[0 0 0 4 5 0 -7 0 -9 0 11]
#     [0 0 0 -4 -5 0 7 0 9 0 -11]]
# shifted such as min(res) = 0
def to_hero_index_and_augmentation(heroes, victories):
    indices = np.arange(121)
    real_game = heroes * indices + 122
    simulated_game = - heroes * indices + 122
    # print(real_game[0])
    # print(simulated_game[0])
    # res = np.concatenate([heroes*indices + 122, heroes*indices*-1 + 122])
    res = np.concatenate([real_game, simulated_game])
    res[res == 122] = 0
    return  res, np.concatenate([victories, victories])



def preprocess_data():
    l = sorted(os.listdir('data/'))
    l_h = ['data/' + f for f in l if 'picks' in f]
    l_r = ['data/' + f for f in l if 'results' in f]
    heroes = [np.load(l) for l in l_h]
    victories = [np.load(l) for l in l_r]

    heroes = np.concatenate(heroes)    
    victories = np.concatenate(victories)    
    return heroes, victories


def train_basic(model_name):
    # loads data

    heroes, victories = preprocess_data()
    print("data shape : ", heroes.shape, victories.shape)

    picks, victories = to_hero_index_and_augmentation(heroes, victories)


    embedded_size = 1000
    m = get_embedded_moderate_model(embedded_size)
    m.summary()

    opt = Adam(lr=0.00001)
    metrics = ['binary_accuracy']

    t = time.time()
    tb = TensorBoard(
            log_dir=f"./logs/{t}_" + model_name,
            write_graph=True,
            write_images=True)

    callbacks = [ModelCheckpoint(filepath='models/' + model_name, period=100), tb]

    m.compile(optimizer=opt, loss='binary_crossentropy', metrics=metrics)
    history = None
    try:
        history = m.fit(x=picks, y=victories, batch_size=128, callbacks=callbacks, verbose=1, epochs=50, validation_split=0.15)

    except KeyboardInterrupt:
        print('\n Saving history of training to : ' + model_name + '_history')
        save_object(history, model_name + '_history')


if __name__ == '__main__':

    model_name = sys.argv[1]
    train_basic(model_name)
