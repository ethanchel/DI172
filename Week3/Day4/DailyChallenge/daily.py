# Instructions
# The goal is to create a class that represents a simple circle.

# A Circle can be defined by either specifying the radius or the diameter - use a decorator for it.
# The user can query the circle for either its radius or diameter.



# Abilities of a Circle Instance
# Your Circle class should be able to:

# ✅ Compute the circle’s area.
# ✅ Print the attributes of the circle — use a dunder method (__str__ or __repr__).
# ✅ Add two circles together and return a new circle with the new radius — use a dunder method (__add__).
# ✅ Compare two circles to see which is bigger — use a dunder method (__gt__).
# ✅ Compare two circles to check if they are equal — use a dunder method (__eq__).
# ✅ Store multiple circles in a list and sort them — implement __lt__ or other comparison methods.


import math
from functools import singledispatchmethod
class Circle:
    @singledispatchmethod
    def __init__(self, value):
        raise NotImplementedError("Unsupported type")

    @__init__.register
    def _(self, radius: float):
        self.radius = radius

    @__init__.register
    def _(self, diameter: int):
        self.radius = diameter / 2

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def area(self):
        return math.pi * (self.radius ** 2)

    def __str__(self):
        return f"Circle(radius={self.radius}, diameter={self.diameter}, area={self.area})"

    def __add__(self, other):
        if isinstance(other, Circle):
            return Circle(self.radius + other.radius)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Circle):
            return self.radius > other.radius
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Circle):
            return self.radius == other.radius
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Circle):
            return self.radius < other.radius
        return NotImplemented
# Example usage:
c1 = Circle(5)          # Circle with radius 5
c2 = Circle(10)         # Circle with radius 10
c3 = Circle(20)         # Circle with diameter 20
print(c1)                # Print circle attributes
print(c2.area)          # Print area of circle c2
c4 = c1 + c2            # Add two circles
print(c4)                # Print new circle attributes
print(c1 > c2)         # Compare circles
print(c1 == c2)        # Check equality
circles = [c2, c1, c3]
circles.sort()          # Sort circles
for c in circles:
    print(c)            # Print sorted circlesimport math
