import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Dense, Input, Subtract, BatchNormalization, InputLayer
from keras import backend as K, Model, regularizers, backend, optimizers
from keras import initializers

import os
import json
import traceback
import numpy as np

import skimage
from skimage import io, transform

from flask import Flask, jsonify, request


# Create the model
def create_model(conv_layers, dense_layers, height, width, channels):
    def ConvBlock(n_conv, filters, kernel_size, strides=(1, 1), padding='same', kernel_initializer='he_uniform',
                  activation='relu', is_last=False, bnorm=False, dropout=0.0):

        for i in range(n_conv):
            model.add(keras.layers.Conv2D(filters, kernel_size, strides=strides, padding=padding,
                                          kernel_initializer=kernel_initializer))
            if bnorm:
                model.add(keras.layers.BatchNormalization())
            model.add(keras.layers.Activation(activation))

        if is_last:
            model.add(keras.layers.GlobalMaxPooling2D())
        else:
            model.add(keras.layers.MaxPooling2D())
        ""
        if dropout > 0:
            model.add(keras.layers.Dropout(dropout))

        return

    def DenseBlock(size, kernel_initializer='glorot_uniform', activation='relu', is_last=False, bnorm=False,
                   dropout=0.0, bias_initializer=0):

        model.add(keras.layers.Dense(size, kernel_initializer=kernel_initializer,
                                     bias_initializer=keras.initializers.Constant(value=bias_initializer)))

        if not is_last:
            if bnorm:
                model.add(keras.layers.BatchNormalization())

            model.add(keras.layers.Activation(activation))

            if dropout > 0:
                model.add(keras.layers.Dropout(dropout))

        return

    model = keras.models.Sequential(name='Leaf Counter')

    model.add(
        keras.layers.InputLayer(
            input_shape=(height, width, channels),
            name='input'
        )
    )

    for i, params in enumerate(conv_layers):
        is_last = i == len(conv_layers) - 1
        ConvBlock(is_last=is_last, **params)

    for i, params in enumerate(dense_layers):
        is_last = i == len(dense_layers) - 1
        DenseBlock(is_last=is_last, **params)

    # Compile model
    model.compile(loss='mae',
                  optimizer=keras.optimizers.Adadelta(),  # Adam(),
                  metrics=[keras.metrics.mae, keras.metrics.mse])

    return model


class ImageGenerator(keras.utils.Sequence):
    'Generates data for Keras'

    def __init__(self, image_list, cropped_dim=(1800, 800), rescale=0.25, n_channels=3, batch_size=32):
        'Initialization'
        self.cropped_dim = cropped_dim
        self.rescale = rescale
        self.final_dim = (int(self.cropped_dim[0] * self.rescale), int(self.cropped_dim[1] * self.rescale))
        self.image_list = image_list
        self.n_channels = n_channels
        self.indexes = np.arange(len(self.image_list))
        self.batch_size = batch_size
        self.cur_idx = 0

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.ceil(len(self.image_list) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]

        if index == (len(self) - 1):
            indexes = indexes[:(len(self.image_list) % self.batch_size)]

        # Find list of URIs
        list_images_batch = self.image_list[indexes]

        X = self.__data_generation(list_images_batch)

        return X

    def __data_generation(self, list_images_batch):
        'Generates data containing batch_size samples'  # X : (n_samples, *dim, n_channels)
        new_h, new_w = self.cropped_dim[0], self.cropped_dim[1]

        # Initialization
        X = np.empty((len(list_images_batch), *self.final_dim, self.n_channels))

        # Generate data
        for i, image_path in enumerate(list_images_batch):

            try:
                img = skimage.io.imread(image_path)
                if self.n_channels == 3:
                    # remove alpha channel
                    img = img[:, :, :3]

                # Crop the image
                cropped_img = skimage.util.crop(img, (
                    (20, img.shape[0] - new_h - 20),
                    (int((img.shape[1] - new_w) / 2), int((img.shape[1] - new_w) / 2)),
                    (0, 0)
                ),
                                                copy=False)

                # Lower the resolution
                X[i, ] = skimage.img_as_ubyte(
                    skimage.transform.rescale(cropped_img, self.rescale, anti_aliasing=True, preserve_range=False,
                                              multichannel=True), force_copy=False)
            except:
                print("Unexpected error on index {} for image {}: {}".format(self.cur_idx, image_path,
                                                                             traceback.format_exc()))
                X[i, ] = np.zeros((*self.final_dim, self.n_channels), dtype=np.uint8)

        return X


WIDTH_IMAGES = 200
HEIGHT_IMAGES = 450
CHANNELS = 3

model = create_model(
    conv_layers=[
            {'n_conv':2, 'filters':4,   'kernel_size':(3,3), 'strides':(1, 1), 'bnorm':True, 'activation':'relu'},
            {'n_conv':2, 'filters':8,   'kernel_size':(3,3), 'strides':(1, 1), 'bnorm':True, 'activation':'relu'},
            {'n_conv':2, 'filters':16,  'kernel_size':(3,3), 'strides':(1, 1), 'bnorm':True, 'activation':'relu'},
            {'n_conv':2, 'filters':32,  'kernel_size':(3,3), 'strides':(1, 1), 'bnorm':True, 'activation':'relu'},
            {'n_conv':2, 'filters':64,  'kernel_size':(3,3), 'strides':(1, 1), 'bnorm':True, 'activation':'relu'},
            {'n_conv':2, 'filters':128, 'kernel_size':(3,3), 'strides':(1, 1), 'bnorm':True, 'activation':'relu'},
            {'n_conv':2, 'filters':256, 'kernel_size':(3,3), 'strides':(1, 1), 'bnorm':True, 'activation':'relu'},
            {'n_conv':2, 'filters':512, 'kernel_size':(3,3), 'strides':(1, 1), 'bnorm':True, 'activation':'relu'},
        ],
    dense_layers=[
        {'size':1024, 'bnorm':True,  'activation':'relu'},
        {'size':1024, 'bnorm':True,  'activation':'relu'},
        {'size':1024, 'bnorm':True,  'activation':'relu'},
        {'size':1,    'bnorm':False},
    ],
    width=WIDTH_IMAGES, height=HEIGHT_IMAGES, channels=CHANNELS,
)

# model.summary()

model.load_weights("./plant_splitting_big_model_0.87_valid.h5")


app = Flask(__name__)
app.config["DEBUG"] = False
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def api_root():
    return '''<h1>BigDataGrapes Leaf Counting API</h1>
    <p> Available resources: <br>
    /api/v1.0/predict_dataset/ <br>
    /api/v1.0/predict_image/ <br>
    </p>'''


@app.route('/api/v1.0/predict_dataset/', methods=['GET'])
def predict_dataset():
    # if key doesn't exist, returns None
    dataset_id = request.args.get('dataset_id')

    print("You are requesting the prediction of leaves of a dataset")

    generator = ImageGenerator(
        # HERE THERE IS THE NEED TO RETRIEVE THE IMAGE LIST
        # (PATH TO LOCAL IMAGES) FROM THE DATASET ID
        # e.g., image_list=datasets[dataset_id].image_list,
        image_list=[],
        batch_size=8
    )

    if len(generator) > 0:
        leaf_count = model.predict_generator(
            generator,
            use_multiprocessing=False,
            workers=8,
            max_queue_size=10,
            verbose=1
        ).ravel()
    else:
        leaf_count = []

    return jsonify({'predicted_leaves': leaf_count})


@app.route('/api/v1.0/predict_image/', methods=['GET'])
def predict_image():

    # if key doesn't exist, returns None
    dataset_id = request.args.get('dataset_id')
    image = request.args.get('image')

    print("You are requesting the prediction of leaves of a single image")

    if image is not None:

        generator = ImageGenerator(
            # HERE THERE IS THE NEED TO RETRIEVE THE IMAGE PATH
            # e.g., image_list=[datasets[dataset_id][image]],
            image_list=[image],
            batch_size=1
        )

        leaf_count = model.predict_generator(
            generator,
            use_multiprocessing=False,
            workers=1,
            max_queue_size=1,
            verbose=1
        ).ravel()
    else:
        leaf_count = []

    return jsonify({'predicted_leaves': leaf_count[0]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8325)
