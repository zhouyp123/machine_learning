#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
from conv_layer import conv_layer
from fully_connect_layer import fc_layer


def relu(array):
    negative_mask = array < 0.0
    array[negative_mask] = 0.0
    return array


def relu_derive(y):
    derive = np.zeros(y.shape)
    derive[y > 0.0] = 1.0
    return derive


def identify(x):
    return x


def identify_derv(y):
    return np.ones(y.shape)


def init_fc_test():
    input_array = np.array(
        [1., 2., 0., 2., 1., 2., 0., 1., 1., 0., 1., 0., 1., 2., 1., 2.])
    input_array = input_array.reshape(16, 1)
    weights = np.array([[-0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1,
                         0.1, 0.1, 0.1, -0.1, 0.1, 0.1, -0.1, -0.1, 0.1],
                        [0.1, -0.1, 0.1, 0.1, -0.1, 0.1, -0.1,
                         0.1, -0.1, 0.1, 0.1, -0.1, 0.1, - 0.1, -0.1, -0.1],
                        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                         0.1, -0.1, 0.1, -0.1, -0.1, 0.1, -0.1, 0.1, -0.1],
                        [0.1, -0.1, 0.1, -0.1, 0.1, 0.1, 0.1,
                         0.1, -0.1, 0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1],
                        [0.1, -0.1, 0.1, -0.1, 0.1, 0.1, 0.1,
                         0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1],
                        [0.1, 0.1, -0.1, 0.1, 0.1, 0.1, 0.1,
                         0.1, -0.1, 0.1, 0.1, -0.1, 0.1, -0.1, 0.1, 0.1],
                        [0.1, 0.1, -0.1, 0.1, 0.1, 0.1, 0.1,
                         0.1, 0.1, -0.1, -0.1, -0.1, -0.1, -0.1, 0.1, 0.1],
                        [0.1, 0.1, -0.1, 0.1, 0.1, 0.1, 0.1,
                         0.1, 0.1, 0.1, 0.1, -0.1, 0.1, -0.1, 0.1, 0.1],
                        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                         0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, 0.1, 0.1],
                        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                         0.1, -0.1, -0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1]])
    bias = np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]).reshape(10, 1)
    target = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                       0.1, 1., 0.1, 0.1]).reshape(10, 1)
    fc = fc_layer(action=relu, action_derive=relu_derive, layers=[16, 10])
    fc.weights = weights
    fc.bias = bias
    return fc, weights, bias, input_array, target


def init_conv_test():
    a = np.array(
        [[[0, 1, 1, 0, 2],
          [2, 2, 2, 2, 1],
          [1, 0, 0, 2, 0],
          [0, 1, 1, 0, 0],
          [1, 2, 0, 0, 2]],
         [[1, 0, 2, 2, 0],
          [0, 0, 0, 2, 0],
          [1, 2, 1, 2, 1],
          [1, 0, 0, 0, 0],
          [1, 2, 1, 1, 1]],
         [[2, 1, 2, 0, 0],
          [1, 0, 0, 1, 0],
          [0, 2, 1, 0, 1],
          [0, 1, 2, 2, 2],
          [2, 1, 0, 0, 1]]])
    b = np.array(
        [[[0, 1, 1],
          [2, 2, 2],
          [1, 0, 0]],
         [[1, 0, 2],
          [0, 0, 0],
          [1, 2, 1]]])
    cl = conv_layer(action=identify, zero_padding=1,
                    action_derive=identify_derv,
                    input_shape=(3, 5, 5), kernel_stride=2,
                    kernel_shape=(3, 3, 3), kernel_num=2)

    cl.kernels[0].weights = np.array(
        [[[-1, 1, 0],
          [0, 1, 0],
          [0, 1, 1]],
         [[-1, -1, 0],
          [0, 0, 0],
          [0, -1, 0]],
         [[0, 0, -1],
          [0, 1, 0],
          [1, -1, -1]]], dtype=np.float64)
    cl.kernels[0].bias = 1
    cl.kernels[1].weights = np.array(
        [[[1, 1, -1],
          [-1, -1, 1],
          [0, -1, 1]],
         [[0, 1, 0],
          [-1, 0, -1],
          [-1, 1, 0]],
         [[-1, 0, 0],
          [-1, 0, 1],
          [-1, 0, 0]]], dtype=np.float64)
    return a, b, cl


def conv_gradient_check():
    '''
    梯度检查
    '''
    # 设计一个误差函数，取所有节点输出项之和
    def error_function(o):
        return o.sum()
    # 计算forward值
    a, b, cl = init_conv_test()
    cl.forward(a)
    # 求取sensitivity map，是一个全1数组
    sensitivity_array = np.ones(cl.feature_map.shape,
                                dtype=np.float64)
    # 计算梯度
    cl.backward(sensitivity_array)
    # 检查梯度
    epsilon = 10e-4
    depth, heigth, width = cl.kernel_shape
    for d in range(depth):
        for i in range(heigth):
            for j in range(width):
                cl.kernels[0].weights[d, i, j] += epsilon
                cl.forward(a)
                err1 = error_function(cl.feature_map)
                cl.kernels[0].weights[d, i, j] -= 2 * epsilon
                cl.forward(a)
                err2 = error_function(cl.feature_map)
                expect_grad = (err1 - err2) / (2 * epsilon)
                cl.kernels[0].weights[d, i, j] += epsilon
                print('weights(%d,%d,%d): expected - actural %f - %f' % (
                    d, i, j, expect_grad, cl.kernels[0].weights_grad[d, i, j]))


def fc_gradient_check():

    def mean_square_error(out, y):
        minus = out - y
        return np.sum(np.multiply(minus, minus)) / 2.0
    fc, weights, bias, input_array, target = init_fc_test()
    out = fc.forward(input_array)
    delta_map = -np.multiply(target - out,
                             relu_derive(out))
    # delta_map = out - target
    fc.backward(delta_map)
    epsilon = 10e-4
    for i in range(fc.layers[0]):
        for j in range(fc.layers[1]):
            fc.weights[j, i] += epsilon
            out = fc.forward(input_array)
            err1 = mean_square_error(out, target)
            fc.weights[j, i] -= 2 * epsilon
            out = fc.forward(input_array)
            err2 = mean_square_error(out, target)
            expect_grad = (err1 - err2) / (2 * epsilon)
            fc.weights[j, i] += epsilon
            print('weights(%d,%d): expected - actural %f - %f' % (
                j, i, expect_grad, fc.weights_grad[j, i]))


if __name__ == '__main__':
    # conv_gradient_check()
    fc_gradient_check()
