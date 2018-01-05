# coding:utf-8

import tensorflow as tf
from tensorflow.python.ops import rnn
# define lstm model and reture related features


# return n outputs of the n lstm cells
def biLSTM(x, hidden_size):
	# biLSTM：
	# 功能：添加bidirectional_lstm操作
	# 参数：
	# 	x: [batch, height, width]   / [batch, step, embedding_size]
	# 	hidden_size: lstm隐藏层节点个数
	# 输出：
	# 	output: [batch, height, 2*hidden_size]  / [batch, step, 2*hidden_size]

	# input transformation
	input_x = tf.transpose(x, [1, 0, 2])
	# input_x = tf.reshape(input_x, [-1, w])
	# input_x = tf.split(0, h, input_x)
	input_x = tf.unstack(input_x) # [tf.pack] 和 [tf.unpack] 弃用，改为 [tf.stack] 和 [tf.unstack]。

	# define the forward and backward lstm cells
	lstm_fw_cell = rnn.BasicLSTMCell(hidden_size, forget_bias=1.0, state_is_tuple=True)
	lstm_bw_cell = rnn.BasicLSTMCell(hidden_size, forget_bias=1.0, state_is_tuple=True)
	# rnn.bidirectional_dynamic_rnn()
	# bidirectional_rnn 过期 考虑使用静动态 bidirectional_dynamic_rnn
	output, _, _ = rnn.static_bidirectional_rnn (lstm_fw_cell, lstm_bw_cell, input_x, dtype=tf.float32)

	# output transformation to the original tensor type
	output = tf.stack(output)
	output = tf.transpose(output, [1, 0, 2])
	return output

