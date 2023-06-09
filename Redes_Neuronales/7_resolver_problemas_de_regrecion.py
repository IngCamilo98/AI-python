# -*- coding: utf-8 -*-
"""7_resolver problemas de regrecion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z3BfAY_HtWx9YG01NbcYEN557fjIg6bi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import boston_housing
from keras import layers, models, optimizers

(train_data, train_labels),(test_data, test_labels) = boston_housing.load_data()

train_data.shape

train_labels.shape

train_data[0]

train_labels[0]

mean = train_data.mean(axis=0)
train_data = train_data - mean
std = train_data.std(axis=0)
train_data = train_data / std

#siempre se debe hacer con la media de los datos de entrenamiento y la desviacion estandar de los datos de entrenamiento
test_data = test_data - mean
test_data = test_data / std

def build_model_regression(lr_var, input_data):
  model = models.Sequential()
  model.add(layers.Dense(64, activation='relu', input_shape=(input_data,)))
  model.add(layers.Dense(64, activation='relu'))
  #Como el valor resultante va a ser una valor numerico especifico
  #la ultima capa debe ser lineal
  model.add(layers.Dense(1))

  model.compile(optimizer= optimizers.RMSprop(lr=lr_var), loss='mse', metrics=['mae'])
  return model

# 4 iteraciones
k = 4
num_val_samples = len(train_data) // k
num_epochs = 60
all_history = []

valor = 2
(valor) * num_val_samples

for i in range(k):
  print("Fold:", i)
  val_data = train_data[i*num_val_samples : (i+1) * num_val_samples]
  val_targets = train_labels[i*num_val_samples : (i+1) * num_val_samples]

  partial_train_data = np.concatenate(
      [train_data[:i * num_val_samples],
       train_data[(i+1) * num_val_samples:]
       ],
       axis=0)
  
  partial_train_targets = np.concatenate(
      [train_labels[:i * num_val_samples],
       train_labels[(i+1) * num_val_samples:]
       ],
       axis=0)
  model = build_model_regression(0.001, 13)
  history = model.fit(partial_train_data, partial_train_targets,
                      epochs = num_epochs,
                      batch_size = 16,
                      validation_data = (val_data, val_targets),
                      verbose=0
                      )
  all_history.append(history.history['val_mae'])

len(all_history[0])

pd.DataFrame(all_history)

all_mean_avg = pd.DataFrame(all_history).mean(axis=0)
all_mean_avg

fig = plt.figure(figsize=(10,10))
plt.plot(range(1, len(all_mean_avg[15:])+1), all_mean_avg[15:])
plt.show

model.evaluate(test_data, test_labels)