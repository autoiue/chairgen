from keras.models import Model
from keras.layers import *
from keras import backend as K
from keras import metrics

import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import os, readline, math

def choose(choices):
    index = 1
    for c in choices:
        print(str(index)+": "+(">" if index == 1 else "")+str(c))
        index+=1
    ans=True
    while ans:
        ans=input("> ")
        if ans == "" or ans < 1 : ans = 0
        else: ans = int(ans)-1
        if ans < len(choices):
            break

    return choices[ans]

#INPUT_DIR = "../../data/preprocessed_samples"
INPUT_DIR = "../../data/preprocessed_"
#INCLUDE_NORMALS = True
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
    for i in range(max_dim - len(x)):
       x = np.append(x, [x[np.random.randint(0, len(x))]], axis=0)
    print("Reshaping from "+old+" to "+str(len(x))+"("+str(max_dim)+")")
    return np.swapaxes(x, 0, 1)

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

    X = [reshape(x,max_dim) for x in X]

    train, test = getsplit(len(X), TESTTRAIN_RATIO)

    print("Splitting "+str(train)+"/"+str(test))

    return np.stack(X[:train]), np.stack(X[-test:])

X_train, X_test = loadX(INPUT_DIR) 

print("TRAIN : " + str(X_train.shape))
print("TEST :  " + str(X_test.shape))

batch_size = X_test.shape[0]
original_dim = X_train.shape[2]
latent_dim = 3
channels = 6 if INCLUDE_NORMALS else 3
intermediate_dim = 1024
epochs = 5
epsilon_std = .001

# encoder : X > encodedX
x = Input(batch_shape=(batch_size, channels, original_dim))
h = Dense(intermediate_dim, activation='relu')(x)
z_mean = Dense(latent_dim)(h)
z_log_var = Dense(latent_dim)(h)

def sampling(args):
    z_mean, z_log_var = args
    epsilon = K.random_normal(shape=(batch_size, channels, latent_dim), mean=0.,
                              stddev=epsilon_std)
    r = z_mean + K.exp(z_log_var / 2) * epsilon
    print(args, r)
    return r

# note that "output_shape" isn't necessary with the TensorFlow backend
z = Lambda(sampling)([z_mean, z_log_var])

# we instantiate these layers separately so as to reuse them later
decoder_h = Dense(intermediate_dim, activation='relu')
decoder_mean = Dense(original_dim, activation='sigmoid')
h_decoded = decoder_h(z)
x_decoded_mean = decoder_mean(h_decoded)


def vae_loss(x, x_decoded_mean):
    xent_loss = original_dim * metrics.binary_crossentropy(x, x_decoded_mean)
    kl_loss = - 0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)
    return xent_loss + kl_loss

# end-to-end model autoencoder
vae = Model(x, x_decoded_mean)
#vae.compile(optimizer='rmsprop', loss=vae_loss)
vae.compile(optimizer='rmsprop', loss='mean_squared_error')

# train the VAE on data

# x_train = X_train.astype('float32')
# x_test = X_test.astype('float32')

vae.fit(X_train, X_train,
        shuffle=True,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_test, X_test), verbose=1)

print(vae.predict(X_test))

# build a model to project inputs on the latent space
# encoder, from inputs to latent space
encoder = Model(x, z_mean)

# display a 2D plot of the digit classes in the latent space
# shows relations between character forms
x_test_encoded = encoder.predict(X_train, batch_size=batch_size)
print(x_test_encoded)
plt.figure(figsize=(6, 6))
plt.scatter(x_test_encoded[:, 1], x_test_encoded[:, 2], c='red')
plt.show()

# # build a digit generator that can sample from the learned distribution
# decoder_input = Input(shape=(latent_dim,))
# _h_decoded = decoder_h(decoder_input)
# _x_decoded_mean = decoder_mean(_h_decoded)
# generator = Model(decoder_input, _x_decoded_mean)

# # display a 2D manifold of the digits
# n = 15  # figure with 15x15 digits
# digit_size = 28
# figure = np.zeros((digit_size * n, digit_size * n))
# # linearly spaced coordinates on the unit square were transformed through the inverse CDF (ppf) of the Gaussian
# # to produce values of the latent variables z, since the prior of the latent space is Gaussian
# grid_x = norm.ppf(np.linspace(0.05, 0.95, n))
# grid_y = norm.ppf(np.linspace(0.05, 0.95, n))

# for i, yi in enumerate(grid_x):
#     for j, xi in enumerate(grid_y):
#         z_sample = np.array([[xi, yi]])
#         x_decoded = generator.predict(z_sample)
#         digit = x_decoded[0].reshape(digit_size, digit_size)
#         figure[i * digit_size: (i + 1) * digit_size,
#                j * digit_size: (j + 1) * digit_size] = digit

# plt.figure(figsize=(10, 10))
# plt.imshow(figure, cmap='Greys_r')
# plt.show()