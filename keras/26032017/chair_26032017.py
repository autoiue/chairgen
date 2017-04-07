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

INPUT_DIR = "../../data/preprocessed_low"
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

def loadData(folder):

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

    max_dim -= max_dim % 2 
    out_dim = 6444

    print("Reshaping X...")
    X = [reshape(v,max_dim) for v in X]

    print("Reshaping Y...")
    Y = [reshape(v,out_dim) for v in X]

    train, test = getsplit(len(X), TESTTRAIN_RATIO)

    print("Splitting "+str(train)+"/"+str(test))

    return np.stack(X[:train]), np.stack(X[-test:]), np.stack(Y[:train]), np.stack(Y[-test:])

print("Loading "+INPUT_DIR)

X, XT, Y, YT = loadData(INPUT_DIR) 

print("TRAIN : " + str(X.shape)+" " + str(Y.shape))
print("TEST :  " + str(XT.shape)+" " + str(YT.shape))

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
x = Conv1D(X.shape[2], 3, activation='linear', padding='same')(x)
decoded = BatchNormalization(axis=2)(x)


autoencoder = Model(input_pc, decoded)
print(autoencoder.summary())
print("Compiling model...")
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

print("Begining fitting.")
autoencoder.fit(X, Y,
                epochs=50,
                batch_size=XT.shape[0],
                shuffle=True,
                validation_data=(XT, YT))

autoencoder.save('trained_'+time.strftime("%Y%m%d-%H")+str(X.shape)+'.h5')

def save_coordinates_xyz(coords):
    files = {}
    timestr = time.strftime("%Y%m%d-%H%M%S")

    if len(coords.shape) == 3:
        index = 0
        for f in coords: 
            files[timestr+"."+str(index)] = f
            index+=1
    elif len(coords.shape) == 2:
        files[timestr] = coords

    for file, data in files.items():
        with open(file+".xyz", 'w') as outfile:
            for coord in data:
                d = ' '.join(['%.10f' % v for v in coord])
                outfile.write(d+'\n')
        

chairs = autoencoder.predict(XT)

print(str(chairs.shape))

save_coordinates_xyz(chairs)