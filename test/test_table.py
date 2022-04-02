import pytest
import numpy as np
from table import table
import random

def test_1():
    x_max = random.randint(5,10)
    y_max = random.randint(5,10)
    l1 = [i for i in table(x_max,y_max)]
    l2 = []
    for i in range(x_max):
        for j in range(y_max):
            l2.append((i,j))
    assert len(l1) == len(l2)
    for i in range(len(l1)):
        assert l1[i] == l2[i]
        
    return True

def test_1_repeat():
    for _ in range(1000):
        assert test_1()

def test_circle_integrate():
    ans = 0
    delta = 1e-2
    for x,y in table(('x',-1,1,delta),
                     ('y',lambda _:-np.sqrt(1-_.x**2), lambda _: np.sqrt(1-_.x**2),delta)):
        ans += delta**2
    assert np.abs(ans-np.pi) < 1e-2
