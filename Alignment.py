
# coding: utf-8

# In[19]:

import numpy as np
np.random.seed(123)
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
import requests
import random
from PIL import Image
import os

# In[2]:
r = requests.get('https://agda-fyp.herokuapp.com/load')
data = r.json()
random.shuffle(data)
x=int(os.environ.get('X',5))
y=int(os.environ.get('Y',7))


X_train=[]
y_train=[]
it=0
for i in data:
    print(it)
    if it>=x:
        break
    check=False
    r = requests.get(i['url'],stream=True).raw
    try:
        img = Image.open(r).convert('L').resize((50, 50))
        check=True
    except IOError:
        print("Load Error")
        check=False
    if check:
        y_train.append(i['align'])
        X_train.append(np.array(img))
        it=it+1
    
X_test=[]
y_test=[]
x=it
it=0
for i in data[x:]:
    print(it)
    if it>=y-x:
        break
    check=False
    r = requests.get(i['url'],stream=True).raw
    try:
        img = Image.open(r).convert('L').resize((50, 50))
        check=True
    except IOError:
        print("Load Error")
        check=False
    if check:
        y_test.append(i['align'])
        X_test.append(np.array(img))
        it=it+1
print(y_test)
X_train = np.array(X_train)
y_train = np.array(y_train)
X_test = np.array(X_test)
y_test = np.array(y_test)

X_train = X_train.reshape(X_train.shape[0], 50, 50,1)
X_test = X_test.reshape(X_test.shape[0], 50, 50,1)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

print(X_train.shape)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=X_train.shape[1:]))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(1, activation='relu'))

model.compile(loss='mean_squared_error',optimizer='adam')

model.fit(X_train, y_train,
          batch_size=32,
          epochs=int(os.environ.get('EP',75)),
          verbose=1,
          validation_data=(X_test, y_test))
score = model.evaluate(X_test, y_test, verbose=1)
print('Test loss:', score)

