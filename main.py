import os
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
import numpy as np
import tensorflow.python.keras as keras
from tensorflow.python.keras import layers
import cv2
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D

dir1 = 'Img'
sub_dir_and_files = os.listdir(dir1)
sub_dirs = []
#all files include from A-Z, a-z
for x in sub_dir_and_files:
    if os.path.isdir(dir1+'/'+x):
        sub_dirs.append(x)
print(sub_dirs)
#total image numbers
N = 0

#find out size of the datasets
for subdir in sub_dirs:
    N += len(os.listdir(dir1+'/'+subdir))

print(N)

#images
x = []

#labels
y = ['']*N

i = 0
#read every image to X
for subdir in sub_dirs:
    image_files = os.listdir(dir1+'/'+subdir)
    for image in image_files:
        filename = dir1+'/'+subdir+'/'+image
        #read image as a gray image
        img = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)

        #resize the image
        img = cv2.resize(img,(28,28),)
        x.append(img)
        #replace A-Z, a-z as 0-52
        if int(subdir) < 91:
            y[i] = int(subdir) - 65
        else:
            y[i] = int(subdir) - 71
        i += 1

#change the format of X,y from list to numpy.ndarray
X = np.array(x)
y = np.array(y)


#split the data to training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)



X_train = X_train / 255.0
X_test = X_test / 255.0
X_train = X_train.reshape((2002, 28, 28, 1))
X_test = X_test.reshape((858, 28, 28, 1))
#change the label to One-hot format(a matrix only include 0 and 1)
y_trainOnehot = to_categorical(y_train)
y_testOnehot = to_categorical(y_test)




#loading model
model = tf.keras.models.load_model('saved_model/my_model_28')


# training
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
model.fit(X_train, y_trainOnehot, epochs=40)


#save model
model.save('saved_model/my_model_28')



# return loss and accuracy
res = model.evaluate(X_test, y_testOnehot)
print(model.metrics_names)
print(res)



# choose first 15 pictures to test

def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array, y_test[i], X_test[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img, cmap = "gray")

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'
    if predicted_label < 26:
        predicted_label += 65
    else:
        predicted_label += 71
    if true_label <26:
        true_label += 65
    else:
        true_label += 71

    plt.xlabel("{} {:2.0f}% ({})".format(chr(predicted_label),
                                  100 * np.max(predictions_array),
                                  chr(true_label)),
                                  color=color)



num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
    img_random = X_test[i]
    img_random = (np.expand_dims(img_random, 0))
    prob = model.predict(img_random)
    plt.subplot(num_rows, num_cols, i+1)
    plot_image(i, prob, y_test[i], img_random)
plt.tight_layout()
plt.show()


