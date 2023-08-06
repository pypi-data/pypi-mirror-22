#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
This example show you how to creat and train a model and make prediction.
"""
import numpy as np
import yadll
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# load the data
data = yadll.data.Data(yadll.data.mnist_loader())

# create the model
model = yadll.model.Model(name='mlp with dropout', data=data, file='best_model.ym')

# Hyperparameters
hp = yadll.hyperparameters.Hyperparameters()
hp('batch_size', 500)
hp('n_epochs', 1000)
hp('learning_rate', 0.9)
hp('momentum', 0.5)
hp('l1_reg', 0.00)
hp('l2_reg', 0.0000)
hp('patience', 10000)

# add the hyperparameters to the model
model.hp = hp

# Create connected layers
# Input layer
l_in = yadll.layers.InputLayer(input_shape=(None, 28 * 28), name='Input')
# Dropout Layer 1
l_dro1 = yadll.layers.Dropout(incoming=l_in, corruption_level=0.4, name='Dropout 1')
# Dense Layer 1
l_hid1 = yadll.layers.DenseLayer(incoming=l_dro1, n_units=100, W=yadll.init.glorot_uniform,
                                 l1=hp.l1_reg, l2=hp.l2_reg, activation=yadll.activations.relu,
                                 name='Hidden layer 1')
# Dropout Layer 2
l_dro2 = yadll.layers.Dropout(incoming=l_hid1, corruption_level=0.2, name='Dropout 2')
# Dense Layer 2
l_hid2 = yadll.layers.DenseLayer(incoming=l_dro2, n_units=100, W=yadll.init.glorot_uniform,
                                 l1=hp.l1_reg, l2=hp.l2_reg, activation=yadll.activations.relu,
                                 name='Hidden layer 2')
# Logistic regression Layer
l_out = yadll.layers.LogisticRegression(incoming=l_hid2, n_class=10, l1=hp.l1_reg,
                                        l2=hp.l2_reg, name='Logistic regression')

# Create network and add layers
net = yadll.network.Network('2 layers mlp with dropout')
net.add(l_in)
net.add(l_dro1)
net.add(l_hid1)
net.add(l_dro2)
net.add(l_hid2)
net.add(l_out)

# add the network to the model
model.network = net

# updates method
model.updates = yadll.updates.nesterov_momentum

# train the model and save it to file at each best
model.train()

# saving network paramters
net.save_params('net_params.yp')

# make prediction
# We can test it on some examples from test
test_set_x = data.test_set_x.get_value()
test_set_y = data.test_set_y.get_value()

predicted_values = [np.argmax(prediction) for prediction in model.predict(test_set_x[:30])]
true_values = [np.argmax(true_value) for true_value in test_set_y[:30]]

print ("Predicted & True values for the first 30 examples in test set:")
print predicted_values
print true_values
