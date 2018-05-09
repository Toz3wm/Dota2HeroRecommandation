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
import gensim_modeling


def get_basic_model(voc_size):

    #without any embedding
    input_shape =  (2 * voc_size,)

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



def get_moderate_model(voc_size):

    #without any embedding
    input_shape =  (2 * voc_size,)

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
    

def get_big_model(voc_size):

    #without any embedding
    input_shape =  (2 * voc_size,)

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
    x = Dense(units=800, activation='relu')(x)
    x = Dense(units=800, activation='relu')(x)
    x = Dense(units=1600, activation='relu')(x)
    x = Dense(units=1, activation='sigmoid')(x)

    return Model(inpu, x) 


def preprocess_data(nb_matches):
    l = sorted(os.listdir('data/'))
    l_h = ['data/' + f for f in l if 'picks' in f]
    l_r = ['data/' + f for f in l if 'results' in f]
    heroes = [np.load(l) for l in l_h]
    victories = [np.load(l) for l in l_r]

    heroes = np.concatenate(heroes)    
    victories = np.concatenate(victories)    
    return heroes[:nb_matches], victories[:nb_matches]


def train_gensim_basic(model_name, nb_matches):
    # loads data

    heroes, victories = preprocess_data(nb_matches)
    print("data shape : ", heroes.shape, victories.shape)

    model, sentences = gensim_modeling.preprocess_for_keras(heroes, victories)
    picks, victories = gensim_modeling.add_heroes_to_get_team(model, sentences, victories)
    victories = np.concatenate([victories, victories])

    embedded_size = 1000
    print(picks.shape, victories.shape)

    m = model_name(embedded_size)
    model_name = str(model_name)
    m.summary()

    opt = Adam(lr=0.0001)
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
        history = m.fit(x=picks, y=victories, batch_size=64, callbacks=callbacks, verbose=1, epochs=500, validation_split=0.15)

    except KeyboardInterrupt:
        print('\n Saving history of training to : ' + model_name + '_history')
        save_object(history, model_name + '_history')


def train_with_gensim(model_name, nb_matches):
    model_name += 'GENSIM' 
    heroes, victories = preprocess_data(nb_matches)
    print("data shape : ", heroes.shape, victories.shape)

    heroes, heroes_indexes =gensim_modeling.preprocess_for_keras(heroes, victories)

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
        history = m.fit(x=picks, y=victories, batch_size=128, callbacks=callbacks, verbose=1, epochs=500, validation_split=0.15)

    except KeyboardInterrupt:
        print('\n Saving history of training to : ' + model_name + '_history')
        save_object(history, model_name + '_history')




if __name__ == '__main__':

    model_name = sys.argv[1]
    nb_matches = int(sys.argv[2])
    train_gensim_basic(model_name, nb_matches)
