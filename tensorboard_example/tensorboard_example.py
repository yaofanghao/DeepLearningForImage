import numpy as np
from keras.layers import Input, Dense, Dropout, Activation,Conv2D,MaxPool2D,Flatten
from keras.datasets import mnist
from keras.models import Model
from keras.utils import to_categorical
from keras.callbacks import TensorBoard

if __name__=="__main__":
    (x_train,y_train),(x_test,y_test) = mnist.load_data()

    x_train=np.expand_dims(x_train,axis=-1)
    x_test=np.expand_dims(x_test,axis=-1)
    y_train=to_categorical(y_train,num_classes=10)
    y_test=to_categorical(y_test,num_classes=10)
    batch_size=128
    epochs=10

    inputs = Input([28,28,1])
    x = Conv2D(32, (5,5), activation='relu')(inputs)
    x = Conv2D(64, (5,5), activation='relu')(x)
    x = MaxPool2D(pool_size=(2,2))(x)
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(10, activation='softmax')(x)

    model = Model(inputs,x)

    model.compile(loss='categorical_crossentropy', optimizer="adam",metrics=['acc'])

    #这里tensorboard的内容可以自己视情况设定
    Tensorboard= TensorBoard(log_dir="./model", histogram_freq=1,write_grads=True)

    history=model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, shuffle=True, validation_split=0.2,callbacks=[Tensorboard])
