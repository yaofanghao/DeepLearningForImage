from tensorflow.keras import layers



# def squeeze(inputs):
#     input_channels = int(inputs.shape[-1])
#     x = GlobalAveragePooling2D()(inputs)
#     x = Dense(int(input_channels / 4))(x)
#     x = Activation(relu6)(x)
#     x = Dense(input_channels)(x)
#     x = Activation(hard_swish)(x)
#     x = Reshape((1, 1, input_channels))(x)
#     x = Multiply()([inputs, x])
#     return x

def VGG16(img_input):
    # Block 1
    x = layers.Conv2D(64, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block1_conv1')(img_input)
    x = layers.Conv2D(64, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block1_conv2')(x)
    feat1 = x
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = layers.Conv2D(128, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block2_conv1')(x)
    x = layers.Conv2D(128, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block2_conv2')(x)
    feat2 = x
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = layers.Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      dilation_rate=(3, 3),
                      name='block3_conv1')(x)
    x = layers.Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      dilation_rate=(3, 3),
                      name='block3_conv2')(x)
    # x = squeeze(x)
    x = layers.Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      dilation_rate=(3, 3),
                      name='block3_conv3')(x)
    feat3 = x
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      dilation_rate=(3, 3),
                      name='block4_conv1')(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      dilation_rate=(3, 3),
                      name='block4_conv2')(x)
    # x = squeeze(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      dilation_rate=(3, 3),
                      name='block4_conv3')(x)

    feat4 = x

    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv1')(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv2')(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv3')(x)

    # x = Dropout(0.5)(x)
    feat5 = x
    return feat1, feat2, feat3, feat4, feat5
