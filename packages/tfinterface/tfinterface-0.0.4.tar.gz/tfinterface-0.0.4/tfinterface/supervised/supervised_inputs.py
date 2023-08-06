#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xc9bb81c7

# Compiled with Coconut version 1.2.3-post_dev1 [Colonel]

# Coconut Header: --------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_compose, _coconut_pipe, _coconut_starpipe, _coconut_backpipe, _coconut_backstarpipe, _coconut_bool_and, _coconut_bool_or, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: ------------------------------------------------------

from tfinterface.utils import get_global_step
from tfinterface.base import GeneralInputs
import tensorflow as tf


class SupervisedInputs(GeneralInputs):
    """
# Inteface
* `features : Tensor` -
* `labels : Tensor` -
* `keep_prob : Tensor` -
* `training : Tensor` -
* `global_step : Variable` -
    """

    def __init__(self, name, features, labels, dropout_keep_prob=0.5, **kwargs):
        self._dropout_keep_prob = dropout_keep_prob

        training_specs = dict(shape=(), dtype=tf.bool)
        keep_prob_specs = dict(shape=(), dtype=tf.float32)

        super(SupervisedInputs, self).__init__(name, features=features, labels=labels, keep_prob=keep_prob_specs, training=training_specs, global_step=get_global_step)

    def fit_feed(self, keep_prob=None, **kwargs):
        keep_prob = keep_prob if keep_prob is not None else self._dropout_keep_prob

        return self.get_feed(keep_prob=keep_prob, training=True, **kwargs)


    def predict_feed(self, **kwargs):
        return self.get_feed(keep_prob=1.0, training=False, **kwargs)

class SupervisedPlaceholderInputs(SupervisedInputs):

    def _build(self, shape_features, shape_labels, dtype_features=tf.float32, dtype_labels=tf.float32, **kwargs):
        super(self.__class__, self)._build(**kwargs)

        if type(shape_features) is int:
            shape_features = [None, shape_features]

        if type(shape_labels) is int:
            shape_labels = [None, shape_labels]

        self.features = tf.placeholder(dtype_features, shape=shape_features, name="features")
        self.labels = tf.placeholder(dtype_features, shape=shape_features, name="labels")


    def fit_feed(self, features, labels):
        feed = super(SupervisedPlaceholderInputs, self).fit_feed_base().copy()

        feed.update({self.features: features, self.labels: labels})

        return feed


    def predict_feed(self, features):
        feed = super(SupervisedPlaceholderInputs, self).predict_feed_base().copy()

        feed.update({self.features: features})

        return feed

class SupervisedPlaceholderInputs(SupervisedInputs):

    def _build(self, shape_features, shape_labels, dtype_features=tf.float32, dtype_labels=tf.float32, **kwargs):
        super(self.__class__, self)._build(**kwargs)

        if type(shape_features) is int:
            shape_features = [None, shape_features]

        if type(shape_labels) is int:
            shape_labels = [None, shape_labels]

        self.features = tf.placeholder(dtype_features, shape=shape_features, name="features")
        self.labels = tf.placeholder(dtype_features, shape=shape_features, name="labels")


    def fit_feed(self, features, labels):
        feed = super(self.__class__, self).fit_feed_base().copy()

        feed.update({self.features: features, self.labels: labels})

        return feed


    def predict_feed(self, features):
        feed = super(self.__class__, self).predict_feed_base().copy()

        feed.update({self.features: features})

        return feed
