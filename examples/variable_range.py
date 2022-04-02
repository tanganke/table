from placeholder import _
from table import table

for x,y,z in table(('x',3), 
    ('y',lambda _: _.x+1, _.x+5), 
    ('z', lambda _: _.x+_.y, lambda _: 2*(_.x+_.y), 2)):
  print((x,y,z))
