from keras.layers import Dense, Embeding, Input
from keras. models import Model



def get_basic_model():

	#without any embedding
	input_shape =  (120)

	inpu = Input(shape=input_shape)
	x = Dense(units=200, activation='relu')(inpu)
	x = Dense(units=200, activation='relu')(x)
	x = Dense(units=400, activation='relu')(x)
	x = Dense(units=400, activation='relu')(x)
    x = Dense(units=2, activation='softmax')(x)

    return Model(inpu, x)
	
	