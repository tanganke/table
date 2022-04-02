from timeit import timeit
from table import table
from placeholder import _

def f1():
    for i in range(10):
        for j in range(10):
            for k in range(10):
                pass

def f2():
    for i,j,k in table(10,10,10):
        pass

print(timeit(f1,number=100))
print(timeit(f2,number=100))


def f1():
    for i in range(10):
        for j in range(i,i+10):
            for k in range(j,j+10):
                pass

def f2():
    for i,j,k in table(('i',10),('j',_.i,_.i+10),('k',_.j,_.j+10)):
        pass

print(timeit(f1,number=100))
print(timeit(f2,number=100))

