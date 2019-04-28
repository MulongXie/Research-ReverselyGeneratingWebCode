import tensorflow as tf
import numpy as np


def weight(shape):
    init = tf.random_normal(shape)
    return tf.Variable(init, dtype=tf.float32)


def bias(shape):
    init = tf.constant(0.01, shape=shape)
    return tf.Variable(init, dtype=tf.float32)


def init_parameters():
    w1 = weight((5, 5, 3, 8))
    b1 = bias([8])