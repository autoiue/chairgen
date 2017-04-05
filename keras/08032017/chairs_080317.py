# Create first network with Keras
from keras.models import Sequential
from keras.layers import *
from keras import backend as K
from keras.engine.topology import Layer
import numpy as np
import codecs, json, math

with open('/tmp/test.json', 'w') as outfile:
    json.dump({'lol':2}, outfile)

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)


def jsonFrom3D(a, file):
    vx = []
    s = a.shape
    a0 = s[0]
    a1 = s[1]
    a2 = s[2]

    for x in range(a0):
        for y in range(a1):
            for z in range(a2):
                if a[x][y][z] > 0.5:
                    c = {'x':x,'y':y,'z':z}
                    vx.append(c)

    outdata = {  'dimension' : [{'width': 128, 'height': 128, 'depth': 256}], 'voxels' : vx }

    with open('/tmp/'+file, 'w') as outfile:
        json.dump(outdata, outfile)

class RepeatVector4D(Layer):

    def __init__(self, n, **kwargs):
        self.n = n
        self.input_spec = [InputSpec(ndim=3)]
        super(RepeatVector4D, self).__init__(**kwargs)

    def get_output_shape_for(self, input_shape):
        return (input_shape[0], self.n, input_shape[1], input_shape[2])

    def call(self, x, mask=None):
        x = K.expand_dims(x, 1)
        pattern = K.stack([1, self.n, 1, 1])
        out = K.tile(x, pattern)
        # jsonFrom3D(out[0], 'RV4in.json')
        return out

def jsonTo3D(file):

    file = '../models/'+str(file)[2:-1]
    with open(file) as data_file:    
        data = json.load(data_file)
        dims = [data['dimension'][0]['width'],data['dimension'][0]['height'],data['dimension'][0]['depth']];
        dims[:] = [int(x)+1 for x in dims]

        voxel = np.zeros((dims[0],dims[1],dims[2]))
        for vx in data['voxels']:
            voxel[int(vx['x'])][int(vx['y'])][int(vx['z'])] = 1.0
    return voxel

def findMax(a_list):
    maxShape = (128,128,256)
    for a in a_list:
        s = a.shape
        maxShape = max(maxShape[0], s[0]),max(maxShape[1], s[1]),max(maxShape[2], s[2])
    return maxShape

def reshapeOneUp(a, targetShape):
    s = a.shape
    t = targetShape
    if(s[0] < t[0]):
        a = np.concatenate((np.zeros((math.floor((t[0]-s[0])/2),
                                     s[1],
                                     s[2])),
                           a,
                           np.zeros((math.ceil((t[0]-s[0])/2),
                                     s[1],
                                     s[2]))),
                           axis = 0)
    if(s[1] < t[1]):
        a = np.concatenate((np.zeros((t[0],
                                     math.floor((t[1]-s[1])/2),
                                     s[2])),
                           a,
                           np.zeros((t[0],
                                     math.ceil((t[1]-s[1])/2),
                                     s[2]))),
                           axis = 1)
    if(s[2] < t[2]):
        a = np.concatenate((a,
                           np.zeros((t[0],
                                     t[1],
                                     t[2]-s[2]))),
                           axis = 2)
    return a

def reshapeUp(a_list):
    targetShape = findMax(a_list)
    a_list[:] = [reshapeOneUp(a, targetShape) for a in a_list]
    return a_list

def loadX(fileName):

    file = codecs.open("../index.tsv", encoding = 'utf-8')
    default_0 = lambda s: float(s.strip() or 0)
    default_5 = lambda s: float(s.strip() or 5)
    default_400 = lambda s: float(s.strip() or 400)
    X = np.loadtxt(file, 
                      delimiter="\t", 
                      usecols=(1,2,3,4,5,6,7,8,9),
                      converters={3: default_5, 5: default_400, 6: default_5}
                      )
    return X

def loadY(fileName):

    file = codecs.open("../index.tsv", encoding = 'utf-8')
    Yfiles = np.loadtxt(file, 
                      delimiter="\t", 
                      usecols=0,
                      dtype=str
                      )

    unshaped_Y = [jsonTo3D(f) for f in Yfiles]
    Y = reshapeUp(unshaped_Y)

    Y = np.stack(Y)
    return Y


X = loadX("../index.tsv") # I spare you the content of these
Y = loadY("../index.tsv") #
print("INPUTS:  " + str(X.shape))
print("OUTPUTS: " + str(Y.shape))

jsonFrom3D(Y[0], 'validation_0.json')


# create model
model = Sequential()
# input.shape = (*, 9)
model.add(Dense(128, input_dim=9, init='uniform', activation='relu')) # shape = (*, 181)
model.add(RepeatVector(128)) # shape = (*, 64, 181) 
model.add(RepeatVector4D(256)) # shape = (*, 64, 128, 181) 
model.add(Dense(128))
model.add(GaussianNoise(0.5))
model.add(Dense(128))
model.add(Dropout(0.2))
model.add(Dense(128))
model.add(Dense(128, activation='hard_sigmoid'))
model.add(Reshape((128,128,256)))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
# 
model.fit(X, Y, nb_epoch=150, batch_size=16,  verbose=2)

# calculate predictions (not yet there)
hopefully_a_chair = model.predict(np.array([[2015,40,3,9,400,6,4,1,0]]))[0]

jsonFrom3D(hopefully_a_chair, 'hopefully_a_chair.json')


