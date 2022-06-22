import tensorflow as tf
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['sparse_categorical_accuracy'])

from utils.callbacks import (ExponentDecayScheduler, LossHistory,
                             ModelCheckpoint)

loss_history    = LossHistory('logs/')

history = model.fit(x_train, y_train, batch_size=32, epochs=50,
                    validation_data=(x_test, y_test), validation_freq=1,
                    callbacks=[loss_history])

#model.summary()

acc = history.history['sparse_categorical_accuracy']
val_acc = history.history['val_sparse_categorical_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize = (8,8))
plt.subplot(1,2,1)
plt.plot(acc, label='training accuracy')
plt.plot(val_acc, label='validation accuracy')
plt.legend()
plt.subplot(1,2,2)
plt.plot(loss, label='training loss')
plt.plot(val_loss, label='validation loss')
plt.legend()
plt.show()