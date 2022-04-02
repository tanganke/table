# table
tools for handling nested loop.

## insatllation

```shell
pip install git+https://github.com/tanganke/table
```

## examples

#### first example:

```python
for x,y,z in table(3,5,7):
  print((x,y,z))
```

this is equivalent to

```python
for x in range(3):
  for y in range(5):
    for z in range(7):
      print((x,y,z))
```

#### variable range

sometimes we may want to let variable control the loops, for example:

```python
for x in range(3):
  for y in range(x+1, x+5):
    for z in range(x+y, 2*(x+y), 2):
      print((x,y,z))
```

and this is equivalent to

```python
from placeholder import _

for x,y,z in table(('x',3), ('y',_.x+1, _x+5), ('z', _.x+_.y, 2*(_.x+_.y), 2)):
  print((x,y,z))
```

