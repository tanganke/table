import pytest
from sympy import im
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
