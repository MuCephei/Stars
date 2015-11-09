import is_num
import math
import coordinateRedoing

class Vector(coordinateRedoing.Coordinate):
    #Note that vector when expressed like this is just a dimension, and has no starting point
    #For convienience I express the vector as starting at 0 (a coordinate)

    """
    +
        coordinate
        Vector
    -
        coordinate - vector
        Vector
    *
        cross product
            vector
        constant
    /
        constant

    rotation

    """

    def __init__(self,x = None,y = None,z = None):
        coordinateRedoing.Coordinate.__init__(self,x,y,z)

    

































#for testing
pointA = coordinateRedoing.Coordinate(3,4,5)
pointB = coordinateRedoing.Coordinate(9,9,9)

vectorA = Vector(6,7,8)

print(pointA)
print(pointB)
print(vectorA)