import is_num
import math

class Coordinate:

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
        	return result
        else:
        	raise IncorrectInput("Please input a Coordinate")

    def getX(self):
    	return self.x

    def getY(self):
    	return self.y

    def getZ(self):
    	return self.z

    def subCoor(self,other):
    	#this is the vector from other to self
    	#however we will not do anything until I create vectors again

    def __sub__(self,other):
    	if isinstance(other,Coordinate):
    		return self.subCoor(other)
    		#returns a vector from other to self
    	elif isinstance(other,Vector):
    		return None
    		#**************************************************************************
    		#do something here
    		#namely self minus the vector (invert all the vector's values)
        else:
        	raise CannotSubtract("You cannot subtract",other)

