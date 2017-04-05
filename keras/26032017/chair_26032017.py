from keras.models import Sequential
from keras.models import Model
from keras.layers import *
from keras import backend as K
from keras.callbacks import TensorBoard

from scipy.stats import norm
import numpy as np
import os, readline, math, time, h5py

def choose(choices):
    index = 1
    for c in choices:
        print(str(index)+": "+str(c))
        index+=1
    ans=True
    while ans:
        ans=input("("+str(choices[0])+")> ")
        if ans == "" or int(ans) < 1 : ans = 0
        else: ans = int(ans)-1
        if ans < len(choices):
            break
    print(choices[ans])
    return choices[ans]

INPUT_DIR = "../../data/preprocessed_samples"
# INPUT_DIR = "../../data/preprocessed"
print("Include normals ?")
INCLUDE_NORMALS = choose((False, True))
TESTTRAIN_RATIO = 1/10

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

c = lambda s: float(str(s)[2:-1].replace(',', '.')) or 0
d = dict.fromkeys(range(6), c)

def reshape(x, max_dim):
    old = str(len(x))
    if max_dim >= len(x):
        for i in range(max_dim - len(x)):
           x = np.append(x, [x[np.random.randint(0, len(x))]], axis=0)
    else:
        for i in range(len(x) - max_dim):
           x = np.delete(x, np.random.randint(0, len(x)), axis=0)

    print("Reshaping from "+old+" to "+str(len(x))+"("+str(max_dim)+")")
    return x
    # return np.swapaxes(x, 0, 1)

def getsplit(number, ratio):
    test = math.floor(number*ratio)
    train = math.ceil(number*(1-ratio))-number%test

    return train, test

def loadX(folder):

    X = []
    max_dim = 0

    for root, subdirs, files in os.walk(folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            fname, ext = os.path.splitext(file_path)
            if(ext.lower() =='.xyz'):
                with open(file_path, 'r') as f:
                    print("Loading "+ filename +" ...")
                    x = np.loadtxt(f, converters=d, usecols=None if INCLUDE_NORMALS else (0,1,2)) 
                    max_dim = max(max_dim, len(x))     
                    X.append(x)

    max_dim -= max_dim % 2 + 4

    X = [reshape(x,max_dim) for x in X]

    train, test = getsplit(len(X), TESTTRAIN_RATIO)

    print("Splitting "+str(train)+"/"+str(test))

    return np.stack(X[:train]), np.stack(X[-test:])

print("Loading "+INPUT_DIR)

X, T = loadX(INPUT_DIR) 

print("TRAIN : " + str(X.shape))
print("TEST :  " + str(T.shape))

print("Defining model...")
input_pc = Input(shape=(X.shape[1], X.shape[2]))  # adapt this if using `channels_first` image data format

x = Conv1D(16, 3, activation='relu', padding='same')(input_pc)
x = MaxPooling1D(2, padding='same')(x)
x = Conv1D(8, 3, activation='relu', padding='same')(x)
x = MaxPooling1D(2, padding='same')(x)
x = Conv1D(8, 3, activation='relu', padding='same')(x)
encoded = MaxPooling1D(2, padding='same')(x)

# at this point the representation is (4, 4, 8) i.e. 128-dimensional

x = Conv1D(8, 3, activation='relu', padding='same')(encoded)
x = UpSampling1D(2)(x)
x = Conv1D(8, 3, activation='relu')(x)
x = UpSampling1D(2)(x)
x = Conv1D(16, 3, activation='relu')(x)
x = UpSampling1D(2)(x)
decoded = Conv1D(3, 1, activation='sigmoid', padding='same')(x)
# decoded  = ZeroPadding1D(3)(decoded)

autoencoder = Model(input_pc, decoded)
print("Compiling model...")
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

print("Begining fitting.")
autoencoder.fit(X, X,
                epochs=50,
                batch_size=T.shape[0],
                shuffle=True,
                validation_data=(T, T))

autoencoder.save('untrained_'+time.strftime("%Y%m%d-%H")+str(X.shape)+'.h5')