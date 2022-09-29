

import tensorflow.python.keras.backend as K
from tensorflow.python.keras.layers import *


def relu6(x):
	return K.relu(x, max_value=6)

def _conv_block(inputs, filters, alpha, kernel=(3, 3), strides=(1, 1)):
	filters = int(filters * alpha)
	x = ZeroPadding2D(padding=(1, 1), name='conv1_pad')(inputs)
	x = Conv2D(filters, kernel, padding='valid',
								use_bias=False,
								strides=strides,
								name='conv1')(x)
	x = BatchNormalization(name='conv1_bn')(x)
	return Activation(relu6, name='conv1_relu')(x)

def _depthwise_conv_block(inputs, pointwise_conv_filters, alpha, depth_multiplier=1, strides=(1, 1), block_id=1):
	pointwise_conv_filters = int(pointwise_conv_filters * alpha)

	x = ZeroPadding2D((1, 1), name='conv_pad_%d' % block_id)(inputs)
	x = DepthwiseConv2D((3, 3), padding='valid',
						depth_multiplier=depth_multiplier,
						strides=strides,
						use_bias=False,
						name='conv_dw_%d' % block_id)(x)
	x = BatchNormalization(name='conv_dw_%d_bn' % block_id)(x)
	x = Activation(relu6, name='conv_dw_%d_relu' % block_id)(x)

	x = Conv2D(pointwise_conv_filters, (1, 1),
						padding='same',
						use_bias=False,
						strides=(1, 1),
						name='conv_pw_%d' % block_id)(x)
	x = BatchNormalization(name='conv_pw_%d_bn' % block_id)(x)
	return Activation(relu6, name='conv_pw_%d_relu' % block_id)(x)

def get_mobilenet_encoder(inputs):
	alpha=1.0
	depth_multiplier=1

	#img_input = Input(inputs)

	# 416,416,3 -> 208,208,32 -> 208,208,64
	x = _conv_block(inputs, 32, alpha, strides=(2, 2))
	x = _depthwise_conv_block(x, 64, alpha, depth_multiplier, block_id=1) 
	f1 = x

	# 208,208,64 -> 104,104,128
	x = _depthwise_conv_block(x, 128, alpha, depth_multiplier, strides=(2, 2), block_id=2)  
	x = _depthwise_conv_block(x, 128, alpha, depth_multiplier, block_id=3) 
	f2 = x

	# 104,104,128 -> 52,52,256
	x = _depthwise_conv_block(x, 256, alpha, depth_multiplier, strides=(2, 2), block_id=4)  
	x = _depthwise_conv_block(x, 256, alpha, depth_multiplier, block_id=5) 
	f3 = x

	# 52,52,256 -> 26,26,512
	x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, strides=(2, 2), block_id=6) 
	x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=7) 
	x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=8) 
	x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=9) 
	x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=10) 
	x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=11) 
	f4 = x 

	# 26,26,512 -> 13,13,1024
	x = _depthwise_conv_block(x, 1024, alpha, depth_multiplier, strides=(2, 2), block_id=12)  
	x = _depthwise_conv_block(x, 1024, alpha, depth_multiplier, block_id=13) 
	f5 = x 

	return f1 , f2 , f3 , f4 , f5
