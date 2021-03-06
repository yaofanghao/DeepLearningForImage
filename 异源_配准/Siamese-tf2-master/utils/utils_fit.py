import tensorflow as tf
import tensorflow.keras.backend as K
from tqdm import tqdm


# 防止bug
def get_train_step_fn():
    @tf.function
    def train_step(imgs1, imgs2, targets, net, optimizer):
        with tf.GradientTape() as tape:
            prediction = net([imgs1, imgs2], training=True)
            loss_value = tf.reduce_mean(K.binary_crossentropy(targets, prediction))

        grads = tape.gradient(loss_value, net.trainable_variables)
        optimizer.apply_gradients(zip(grads, net.trainable_variables))
        
        equal       = tf.equal(tf.round(prediction),targets)
        accuracy    = tf.reduce_mean(tf.cast(equal,tf.float32))
        return loss_value, accuracy
    return train_step

@tf.function
def val_step(imgs1, imgs2, targets, net, optimizer):
    prediction = net([imgs1, imgs2], training=False)
    loss_value = tf.reduce_mean(K.binary_crossentropy(targets, prediction))

    return loss_value

def fit_one_epoch(net, optimizer, epoch, epoch_step, epoch_step_val, gen, genval, Epoch):
    train_step      = get_train_step_fn()
    total_loss      = 0
    total_accuracy  = 0

    val_loss        = 0
    print('Start Train')
    with tqdm(total=epoch_step,desc=f'Epoch {epoch + 1}/{Epoch}',postfix=dict,mininterval=0.3) as pbar:
        for iteration, batch in enumerate(gen):
            if iteration >= epoch_step:
                break
            images, targets     = batch[0], batch[1]
            images0, images1    = images[0], images[1]
            targets = tf.cast(tf.convert_to_tensor(targets), tf.float32)

            loss_value, accuracy = train_step(images0, images1, targets, net, optimizer)
            total_loss      += loss_value.numpy()
            total_accuracy  += accuracy.numpy()

            pbar.set_postfix(**{'Total Loss'        : total_loss / (iteration + 1), 
                                'Total accuracy'    : total_accuracy / (iteration + 1),
                                'lr'                : optimizer._decayed_lr(tf.float32).numpy()})
            pbar.update(1)
    print('Finish Train')
        
    print('Start Validation')
    with tqdm(total=epoch_step_val, desc=f'Epoch {epoch + 1}/{Epoch}',postfix=dict,mininterval=0.3) as pbar:
        for iteration, batch in enumerate(genval):
            if iteration >= epoch_step_val:
                break
            images, targets     = batch[0], batch[1]
            images0, images1    = images[0], images[1]
            targets = tf.convert_to_tensor(targets)

            loss_value = val_step(images0, images1, targets, net, optimizer)
            val_loss = val_loss + loss_value.numpy()
            
            pbar.set_postfix(**{'Val Loss'  : val_loss / (iteration + 1)})
            pbar.update(1)
    print('Finish Validation')

    print('Epoch:'+ str(epoch+1) + '/' + str(Epoch))
    print('Total Loss: %.3f || Val Loss: %.3f ' % (total_loss / epoch_step, val_loss / epoch_step_val))
    net.save_weights('logs/ep%03d-loss%.3f-val_loss%.3f.h5' % (epoch + 1, total_loss / epoch_step, val_loss / epoch_step_val))
