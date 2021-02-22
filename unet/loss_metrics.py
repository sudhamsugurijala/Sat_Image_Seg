import os
import io
import gc
import cv2
import sys
import h5py
import pylab
import random
import numpy as np
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt

# Model Specific libraries
import tensorflow as tf
from tensorflow import keras
from keras import backend as K
from keras.models import model_from_json

def getCallbacks():
  return [
          tf.keras.callbacks.EarlyStopping(patience=5, monitor='val_loss'),
          tf.keras.callbacks.TensorBoard(log_dir='logs'),
          tf.keras.callbacks.ModelCheckpoint(
              MODEL_WEIGHTS,
              verbose=1,
              monitor='val_loss',
              save_weights_only=True,
              save_best_only=True
              ),
          tf.keras.callbacks.ReduceLROnPlateau(
              monitor='val_loss', factor=0.1, patience=4,
              verbose=1, min_delta=1e-4
              )
          ]


# LOSS FUNCTION
def getDiceLoss(y_true, y_pred, smooth = 1):
  yt = K.flatten(y_true)
  yt = tf.cast(yt, tf.float32)
  yp = K.flatten(y_pred)
  yp = tf.cast(yp, tf.float32)
  intersection = K.sum(yt * yp)
  dice_coef =((2* intersection) + smooth) / (K.sum(yt) + K.sum(yp) + smooth)
  return 1-dice_coef


# METRIC
def getIOU(y_true, y_pred, smooth=1):
  tf.cast(y_true, tf.float32)
  tf.cast(y_pred, tf.float32)
  intersection = K.sum(K.abs(y_true * y_pred), axis=[1,2,3])
  union = K.sum(y_true,[1,2,3])+K.sum(y_pred,[1,2,3])-intersection
  return K.mean((intersection + smooth) / (union + smooth), axis=0)

