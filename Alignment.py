
# coding: utf-8

# In[19]:

import numpy as np
np.random.seed(123)
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils




# In[2]:

from PIL import Image
X_train=[]
fo = open('temp/syms','r')
fodata = eval(fo.read())
y_train=[]
for it in range(20):
    f = 'temp/img'+str(it)+'.jpg'
    img = Image.open(f).convert('L')
    if not fodata[it][0] is None:
        y_train.append(fodata[it][0])
        X_train.append(np.array(img))
    
X_test=[]
fo = open('test/tsyms','r')
fodata = eval(fo.read())
y_test=[]
for it in range(5):
    f = 'test/img'+str(it)+'.jpg'
    img = Image.open(f).convert('L')
    if not fodata[it][0] is None:
        y_test.append(fodata[it][0])
        X_test.append(np.array(img))
    

    


# In[24]:

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


# In[25]:

print(X_train.shape)


# In[34]:

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=X_train.shape[1:]))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='relu'))

model.compile(loss='mean_squared_error',optimizer='adam')

model.fit(X_train, y_train,
          batch_size=32,
          epochs=10,
          verbose=1,
          validation_data=(X_test, y_test))
score = model.evaluate(X_test, y_test, verbose=1)
print('Test loss:', score)

#model.compile(loss='mean_squared_error',optimizer='sgd',metrics=['accuracy'])
#model.fit(X_train, y_train, batch_size=1, epochs=1000, verbose=1)


# In[ ]:



