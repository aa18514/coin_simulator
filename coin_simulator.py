import numpy as np
import random

FAIL = 2

def flip_unbiased():
   '''
   assume 0 with probability 1/2 and 1 with probability 1/2
   ''' 
   probability = random.random()
   value = 0 if probability <= 0.5 else 1
   return value


def flip(epsilon:float=2**-10)->float:
    '''
    return r <= {0, 1, FAIL} that satisfies the following properties:
    1. P[r = FAIL] < epsilon
    2. P[r = 1 | r != FAIL] = 1/3
    '''
    number_of_flips = np.ceil(1 - np.log2(epsilon))
    
    try:
        number_of_flips = int(number_of_flips)
    except Exception as e:
        print(e)
    
    combinations = 2**number_of_flips
    
    F = 0
    if (combinations - 1) % 3 == 0:
        F = 1
    elif (combinations - 2) % 3 == 0:
        F = 2

    encoding = 0
    for i in range(number_of_flips):
        encoding = encoding + ((2**i) * flip_unbiased())
    
    r = FAIL
    if encoding < (combinations - F)/3:
        r = 1
    elif encoding < (combinations - F):
        r = 0
    assert((F/combinations) <= epsilon)
    #print("P[r = FAIL] + {}".format(F/combinations))

    return r


if __name__ == "__main__":
    '''
    if you run for sufficiently large number of experiments you will find that
    the following conclusions are satisfied
    1. P[r = FAIL] < epsilon
    2. P[r = 1 | r != FAIL] = 1/3
    '''
    experiments = 10000
    ones = 0
    zeros = 0
    fail = 0
    for experiment in range(experiments):
        r = flip()
        if r == 1:
            ones = ones + 1
        elif r == 0:
            zeros = zeros + 1
        elif r == FAIL:
            fail = fail + 1
    print("P[r = FAIL] = {:.6f}".format(fail/experiments))
    print("P[r = 1] = {:.6f}".format(ones/experiments))
    print("P[r = 0] = {:.6f}".format(zeros/experiments))
