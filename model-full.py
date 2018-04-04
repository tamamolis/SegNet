from keras.models import Model
from keras.layers import Input, merge, core, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D, UpSampling2D
import json

from keras import backend as K
K.set_image_dim_ordering('th')


def Unet (nClasses, optimizer, input_width, input_height, nChannels):

    inputs = Input((nChannels, input_height, input_width))

    conv1 = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(inputs)
    conv1 = Dropout(0.2)(conv1)
    conv1 = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(pool1)
    conv2 = Dropout(0.2)(conv2)
    conv2 = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Convolution2D(128, 3, 3, activation='relu', border_mode='same')(pool2)
    conv3 = Dropout(0.2)(conv3)
    conv3 = Convolution2D(128, 3, 3, activation='relu', border_mode='same')(conv3)

    up1 = merge([UpSampling2D(size=(2, 2))(conv3), conv2], mode='concat', concat_axis=1)
    conv4 = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(up1)
    conv4 = Dropout(0.2)(conv4)
    conv4 = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(conv4)

    up2 = merge([UpSampling2D(size=(2, 2))(conv4), conv1], mode='concat', concat_axis=1)
    conv5 = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(up2)
    conv5 = Dropout(0.2)(conv5)
    conv5 = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(conv5)

    conv6 = Convolution2D(nClasses, 1, 1, activation='relu' ,border_mode='same')(conv5)
    conv6 = core.Reshape((nClasses, input_height * input_width))(conv6)
    conv6 = core.Permute((2 ,1))(conv6)

    conv7 = core.Activation('softmax')(conv6)
    model = Model(input=inputs, output=conv7)

    if not optimizer is None:
        model.compile(loss="categorical_crossentropy", optimizer= optimizer , metrics=['accuracy'] )

    return model


if __name__ == '__main__':
    model = Unet(7, None, 360, 480, nChannels=3)
    with open('segNet_basic_model.json', 'w') as outfile:
        outfile.write(json.dumps(json.loads(model.to_json()), indent=2))
