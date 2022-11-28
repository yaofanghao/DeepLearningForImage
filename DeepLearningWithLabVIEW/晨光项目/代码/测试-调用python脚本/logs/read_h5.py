import deepdish as dd
import tensorflow as tf

file_path1 = "ep050-loss0.038-val_loss0.119.h5"
file_path2 = "freeze17_epoch0_5_15_batchsize_2_2/Epoch10-Total_Loss0.2388-Val_Loss0.1218.h5"

def load_h5(file_path):
    mean_val = dd.io.load(file_path)
    print(mean_val)
    # mean_var 是一个字典，两个key  pose和shape
load_h5(file_path2)

# new_model = tf.keras.models.load_model(file_path1)
# new_model.summary()
