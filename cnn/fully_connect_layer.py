#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
from cnn_utils import *


class fc_layer(object):
    """
    fully connect layer
    action:action function
    action_derive:action derive
    layers:layer list
    input_array:input array
    alpha:learning rate
    """

    def __init__(self, action, action_derive, layers):
        '''
        Parameters
        ----------
        action:action function
        action_derive:action derive
        layers:layer list
        input_array:input array

        '''
        self.action = action
        self.action_derive = action_derive
        self.layers = layers
        self.input_shape = (layers[0], 1)
        std = 1.0 / np.sqrt(layers[1] * layers[0])
        self.weights = np.random.normal(loc=0.0,
                                        scale=std,
                                        size=(layers[1], layers[0]))
        self.bias = np.zeros((layers[1], 1))
        self.weights_grad = np.zeros(self.weights.shape)
        self.bias_grad = np.zeros(self.bias.shape)

    def forward(self, input_array):
        '''
        Parameters
        ----------
        action:action function
        action_derive:action derive
        layers:layer list
        input_array:input array like np.zeros((n,1))
        alpha:learning rate

        '''
        debug('fully_connect:\n', input_array)
        self.input_array = input_array.reshape(self.input_shape)
        weighted_sum = np.dot(self.weights, self.input_array) + self.bias
        self.out_put = self.action(weighted_sum)
        return self.out_put

    def backward(self, delta_map):
        debug('fclayer :', np.sum(delta_map), self.layers)
        self.delta_map = np.multiply(np.dot(self.weights.T, delta_map),
                                     self.action_derive(self.input_array))
        self.clac_gradient(delta_map)
        return self.delta_map

    def clac_gradient(self, delta_map):
        # print('fully--clac_gradient:', self.input_shape, np.sum(delta_map))
        self.weights_grad += np.dot(delta_map, self.input_array.T)
        self.bias_grad += delta_map

    def update(self, alpha, batch_size):
        """

        Args:
          batch_size:batch size
          learning_rate: learning rate
        Returns:

        """
        # print('fully--:', self.input_shape,
        #       np.sum(self.weights_grad), alpha, batch_size)
        self.weights -= alpha * self.weights_grad / batch_size
        self.bias -= alpha * self.bias_grad / batch_size
        self.weights_grad[...] = 0.0
        self.bias_grad[...] = 0.0
