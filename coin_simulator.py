import numpy as np
import random
from fractions import Fraction
import matplotlib.pyplot as plt


FAIL = 2

def flip_unbiased():
   '''
   assume 0 with probability 1/2 and 1 with probability 1/2
   ''' 
   probability = random.random()
   value = 0 if probability <= 0.5 else 1
   return value


def generate_fail(combinations, frac):
    F = 0
    while ((frac.numerator * (combinations - F)) % \
            frac.denominator) != 0:
        F = F + 1
    return F


def flip(epsilon:float=0.0001, proba=Fraction(5, 6))->(float, float):
    '''
    choose delta number of flips above np.ceil(1-log2(epsilon))
    return r <= {0, 1, FAIL} that satisfies the following properties:
    1. P[r = FAIL] < epsilon
    2. P[r = 1 | r != FAIL] = 1/3
    ''' 
    flips = int(np.ceil(2-np.log2(epsilon)))
    combinations = 2**flips
    F = generate_fail(combinations, proba)
    while F/combinations >= epsilon:
        flips = flips + 1
        combinations = 2**flips
        F = generate_fail(combinations, proba)
        assert((proba.numerator * (combinations - F)) %\
                proba.denominator == 0)
    encoding = 0
    for i in range(flips):
        encoding = encoding + (flip_unbiased() << i)
    r = FAIL
    if encoding < (proba.numerator * (combinations - F))/\
            proba.denominator:
        r = 1
    elif encoding < (combinations - F):
        r = 0
    assert((F/combinations) <= epsilon)
    error = ((proba.numerator * (combinations - F))/proba.denominator)/\
            combinations
    error = (proba.numerator/proba.denominator) - error
    return error, r



if __name__ == "__main__":
    '''
    if you run for sufficiently large number of experiments you will find that
    the following conclusions are satisfied
    1. P[r = FAIL] < epsilon
    2. P[r = 1 | r != FAIL] = 1/3
    '''
    experiments = 1
    epsilon = np.arange(1e-10, 1e-1, 1e-6)
    errors = []
    f = Fraction(5, 6)
    for e in epsilon:
        ones = 0
        zeros = 0
        fail = 0
        for experiment in range(experiments):
            error, r = flip(e, f)
            if r == 1:
                ones = ones + 1
            elif r == 0:
                zeros = zeros + 1
            elif r == FAIL:
                fail = fail + 1
        errors.append(error)
    plt.xlabel('epsilon')
    plt.ylabel('errors')
    plt.plot(epsilon, errors)
    plt.show()
