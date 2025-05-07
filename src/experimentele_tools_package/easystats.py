import numpy as np
import sympy as sp
from scipy.stats import chi2
"""
A library that contains general functions to be used in data analysis

TODO:
    Documentation for existing functions
    Add generic error propagation function

    Figure out possibilities for statistics functions
"""

def bereken_gemiddelde(metingen):
    gem = sum(metingen)/(len(metingen))
    return gem


def bereken_variantie_gekend_gemiddelde(metingen, gekend_gem):
    s2 = sum((metingen - gekend_gem)**2)/(len(metingen))
    s = np.sqrt(s2)
    return s


def bereken_variantie_ongekend_gemiddelde(metingen, ongekend_gem):
    s2 = sum((metingen - ongekend_gem)**2)/(len(metingen - 1))
    s = np.sqrt(s2)
    return s


def foutpropagatie_som(a, b, s_x, s_y):
    return np.sqrt((a*s_x)**2 + (b*s_y)**2)


def foutpropagatie_product(p, q, s_x, s_y, X, Y, Z):
    return Z*np.sqrt((p*(s_x/X))**2 + (q*(s_y/Y))**2)


def foutpropagatie_algemeen():
    pass