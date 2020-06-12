import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator

html_model = tf.keras.models.load_model('/content/model/')