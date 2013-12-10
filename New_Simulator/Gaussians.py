# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:17:51 2013

@author: ferdinando
"""

from scipy.stats import norm
import numpy as np


def getMean(wcet,sigma=0.001,p=0.005):
    """Returns the mean of the gaussian given the variance (sigma), and
    the probability p that the obtained value is bigger than wcet
    """
    return wcet-norm.isf(p)*sigma


def getRandomValue(mu,sigma=0.05):
    """Returns a random value from a gaussian distribution with mean mu
    and variance sigma"""
    return np.random.normal(mu,sigma)
