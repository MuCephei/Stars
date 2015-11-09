import is_num
import math

class Coordinate:

    """
    toDo

    rotation - do later
        I plan on using this to change frames of reference

    """

    def __init__(self,x = None,y = None,z = None):
        self.x = 0
        self.y = 0
        self.z = 0
        if x is not None:
        	if is_num.isNumber(x):
        		self.x = x
        if y is not None:
        	if is_num.isNumber(y):
        		self.y = y
        if z is not None:
        	if is_num.isNumber(z):
        		self.z = z

    def __str__(self):
    	return "X:" + str(self.x) +" Y:" + str(self.y) + " Z:" + str(self.z)

    def distance(self,other):
        if isinstance(other,Coordinate):
            deltaX = self.x - other.getX()
            deltaY = self.y - other.getY()
            deltaZ = self.z - other.getZ()
            result = math.sqrt(deltaX**2 + deltaY**2 + deltaZ**2)
        else:
        	raise IncorrectInput("Please input a Coordinate")
        return result

    def getX(self):
    	return self.x

    def getY(self):
    	return self.y

    def getZ(self):
    	return self.z

    def __add__(self,other):
        #This only accepts Coordinate + Vector = Vectorin that particular order
        if isinstance(other,Vector):
            x = self.x + other.getX()
            y = self.y + other.getY()
            z = self.z + other.getZ()
            return Vector(x,y,z)
        else:
            raise IncorrectAddition("You must add a Vector to a Vector or Coordinate")

    def __sub__(self,other):
        #This accepts Coordinate - Vector = Coordinate and Coordinate - Coordinate = Vector
        if isinstance(other,Vector):
            #This is kindof the opposite of __add__
            x = self.x - other.getX()
            y = self.y - other.getY()
            z = self.z - other.getZ()
            return Coordinate(x,y,z)

        elif isinstance(other,Coordinate):
            #This is somewhat strange in that CoordinateA - CoordinateB = Vector(from A to B)
            #self is a
            #other is b - a
            # a coordinate is b
            x = other.getX() - self.x
            y = other.getY() - self.y
            z = other.getZ() - self.z
            return Vector(x,y,z)
        else:
            raise IncorrectSubtraction("You must subtract a Coordinate or Vector from a Coordinate")

    def __mul__(self,other):
        #this accepts Coordinate * Constant = Coordinate
        if is_num.isNumber(other):
            x = self.x * other
            y = self.y * other
            z = self.z * other
            return Coordinate(x,y,z)
        else:
            raise IncorrectMultiplication("You must multiply a Coordinate by a Constant")

    def __rmul__(self,other):
        #this accepts Constant * Coordinate = Coordinate
        return self * other

    def __div__(self,other):
        #This accepts Constant / Coordinate = Coordinate
        if is_num.isNumber(other):
            inverse = 1/float(other)
            return self * inverse
        else:
            raise IncorrectDivision("You must divide a Coordinate by a Constant")



class Vector(Coordinate):
    #Note that vector when expressed like this is just a dimension, and has no starting point
    #For convienience I express the vector as starting at 0 (a coordinate)

    """
    *
        cross product
            vector
        constant
    /
        constant

    rotation - do later
        I plan on using this to change frames of reference

    """

    def __init__(self,x = None,y = None,z = None):
        Coordinate.__init__(self,x,y,z)

    def __str__(self):
        result = Coordinate.__str__(self)
        result += " I'm a Vector"
        return result

    def __add__(self,other):
        #This accepts Vector + Vector = Vector
        if isinstance(other,Vector):
            x = self.x + other.getX()
            y = self.y + other.getY()
            z = self.z + other.getZ()
            return Vector(x,y,z)
        else:
            raise IncorrectAddition("You must add a Vector to a Vector or Coordinate")

    def __sub__(self,other):
        #this accepts Vector - Vector = Vector
        if isinstance(other,Vector):
            #Note that I could multiply the vector by -1 and then add it instead
            x = self.x - other.getX()
            y = self.y - other.getY()
            z = self.z - other.getZ()
            return Vector(x,y,z)
        else:
            raise IncorrectSubtraction("You must subtract a Vector from a Vector")

    def __mul__(self,other):
        #This accepts Vector * Constant  = Vector or Vector x Vector = Vector
        if is_num.isNumber(other):
            x = self.x * other
            y = self.y * other
            z = self.z * other
            return Vector(x,y,z)
        elif isinstance(other,Vector):
            #here we do the cross product, notably NOT the dot product
            #if I need that I will make a dot product function
            x = (self.y*other.getZ() - self.z*other.getY())
            y = (self.z*other.getX() - self.x*other.getZ())
            z = (self.x*other.getY() - self.y*other.getX())
            return Vector(x,y,z)
        else:
            raise IncorrectMultiplication("You must multiply a Vector by a Constant or Vector")


    def __div__(self,other):
        #This accepts Vector / Coordinate = Vector
        if is_num.isNumber(other):
            inverse = 1/float(other)
            return self * inverse
        else:
            raise IncorrectDivision("You must divide a Vector by a Constant")

pointA = Coordinate(3,2,5)
pointB = Coordinate(20,5,7)
pointG = Coordinate(10,3,8)

vectorC = pointA-pointB
vectorD = pointB-pointG
vectorE = vectorC * vectorD

print("A")
print(pointA)
print("B")
print(pointB)
print("C")
print(vectorC)
print("D")
print(vectorD)
print("E")
print(vectorE)
    