import math
from Geometry import Point

# runtime dispatch of init constructors
print(Point.__init__.__doc__)

# a method signature and its docstring
print(Point.distanceTo.__doc__)

p1 = Point(10, 20)
p2 = Point(20, 30)
p3 = Point(20, 30)
p4 = Point(50, 60, 45.67)
p5 = Point(50, 60, 45.67)
assert p1.distanceTo(p2) == math.sqrt(200)

# check operator overloading works
assert p1 != p2
assert p2 == p3
assert not p2 != p3
assert p4 == p5
assert not p4 == p3

assert math.isnan(p1.z)

# check distance between 3D points
p1 = Point(50, 60, 45)
p2 = Point(50, 60, 75)
print(p1.distanceTo(p2, in3D=True))

# check __repr__
print(p1)
print(p2)
