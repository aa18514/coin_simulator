import random
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt


FAIL = 2

def flip_unbiased():
    '''
    assume 0 with probability 1/2 and 1 with probability 1/2
    '''
    probability = random.random()
    value = 0 if probability <= 0.50 else 1
    return value


def generate_fail(combinations, frac):
    F = 0
    for i in range(frac.denominator):
        numerator = frac.numerator * (combinations - i)
        if numerator % frac.denominator == 0:
            F = i
            break
    return F


def flip(epsilon: float = 2**-500, proba: Fraction = Fraction(4, 5))->(float, Fraction):
    '''
    choose delta number of flips above np.ceil(1-log2(epsilon))
    return r <= {0, 1, FAIL} that satisfies the following properties:
    1. P[r = FAIL] < epsilon
    2. P[r = 1 | r != FAIL] = proba
    '''
    flips = int(np.ceil(2 - np.log2(epsilon)))
    combinations = 2**flips
    F = generate_fail(combinations, proba)
    while F/combinations >= epsilon:
        flips = flips + 1
        combinations = 2**flips
        F = generate_fail(combinations, proba)
        assert (proba.numerator * (combinations - F)) %\
                proba.denominator == 0
    encoding = 0
    for i in range(flips):
        encoding = encoding + (flip_unbiased() << i)
    r = FAIL
    if encoding < (proba.numerator * (combinations - F))/\
            proba.denominator:
        r = 1
    elif encoding < (combinations - F):
        r = 0
    assert (F/combinations) <= epsilon
    error = ((proba.numerator * (combinations - F))/(combinations * proba.denominator))
    error = (proba.numerator/proba.denominator) - error
    error = F/combinations
    return error, r



if __name__ == "__main__":
    '''
    if you run for sufficiently large number of experiments you will find that
    the following conclusions are satisfied
    1. P[r = FAIL] < epsilon
    2. P[r = 1 | r != FAIL] = 1/3
    '''
    experiments = 10000
    epsilon = np.arange(1e-10, 1e-1, 1e-3)
    print(epsilon)
    errors = []
    f = Fraction(28, 50)
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
        print("P[r = 1] = {}".format(ones/experiments))
        print("P[r = 0] = {}".format(zeros/experiments))
        print("P[r = FAIl] = {}".format(fail/experiments))
        print('\n\n')
        errors.append(error)
    plt.xlabel('epsilon')
    plt.ylabel('errors')
    plt.plot(epsilon, errors)
    plt.show()
