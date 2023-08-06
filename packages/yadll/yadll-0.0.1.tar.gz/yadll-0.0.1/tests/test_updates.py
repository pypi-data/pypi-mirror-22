# -*- coding: UTF-8 -*-

import pytest

import numpy as np

import theano

import yadll


def test_nadam():
    pytest.raises(NotImplementedError, yadll.updates.nadam, 'cost', 'params')


PCT_TOLERANCE = 1E-5


class TestUpdateFunctions(object):
    # compare results on a toy problem to values
    toy_values = {'sgd': [0.81707280688755,
                          0.6648326359915,
                          0.5386151140949],
                  'momentum': [0.6848486952183,
                               0.44803321781003,
                               0.27431190123502],
                  'nesterov_momentum': [0.67466543592725,
                                        0.44108468114241,
                                        0.2769002108997],
                  'adagrad': [0.55373120047759,
                              0.55373120041518,
                              0.55373120039438],
                  'rmsprop': [0.83205403985348,
                              0.83205322744821,
                              0.83205295664444],
                  'adadelta': [0.95453237704725,
                               0.9545237471374,
                               0.95452214847397],
                  'adam': [0.90034972009036,
                           0.90034967993061,
                           0.90034966654402],
                  'adamax': [0.90211749000754,
                             0.90211748762402,
                             0.90211748682951],
                  }

    def f(self, X):
        return ([0.1, 0.2, 0.3] * X**2).sum()

    @pytest.mark.parametrize('method, kwargs', [
        ['sgd', {'learning_rate': 0.1}],
        ['momentum', {'learning_rate': 0.1, 'momentum': 0.5}],
        ['nesterov_momentum', {'learning_rate': 0.1, 'momentum': 0.5}],
        ['adagrad', {'learning_rate': 0.1, 'epsilon': 1e-6}],
        ['rmsprop', {'learning_rate': 0.01, 'rho': 0.9, 'epsilon': 1e-6}],
        ['adadelta', {'learning_rate': 1, 'rho': 0.95, 'epsilon': 1e-6}],
        ['adam', {'learning_rate': 0.01, 'beta1': 0.9, 'beta2': 0.999, 'epsilon': 1e-8}],
        ['adamax', {'learning_rate': 0.01, 'beta1': 0.9, 'beta2': 0.999, 'epsilon': 1e-8}],
        ])
    def test_updates(self, method, kwargs):
        A = yadll.utils.shared_variable([1, 1, 1])
        B = yadll.utils.shared_variable([1, 1, 1])
        update_func = getattr(yadll.updates, method)
        updates = update_func(self.f(A) + self.f(B),
                              [A, B],
                              **kwargs)
        do_update = theano.function([], [], updates=updates)

        for _ in range(10):
            do_update()
        print method
        print A.get_value()
        print B.get_value()
        print self.toy_values[method]
        assert np.allclose(A.get_value(), B.get_value())
        assert np.allclose(A.get_value(), self.toy_values[method])
