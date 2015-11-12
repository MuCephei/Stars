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
        #This only accepts Coordinate + Vector = Vector in that particular order
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
        #This accepts Coordinate / Constant = Coordinate
        if is_num.isNumber(other):
            if other != 0:
                inverse = 1/float(other)
                return self * inverse
            else:
                raise DivideByZero("You cannot Divide by Zero")
        else:
            raise IncorrectDivision("You must divide a Coordinate by a Constant")



class Vector(Coordinate):
    #Note that vector when expressed like this is just a dimension, and has no starting point
    #For convienience I express the vector as starting at 0 (a coordinate)


    def getDistanceXY(self):
        #this is the length of the vector as if it had no z value
        # or it was flatened onto the ground

        flat = Coordinate(self.x,self.y)
        return flat.distance(Coordinate())
        # This is the distance to the origin

    def get_angleXY(self):
        return self.angleXY

    def get_angleZ(self):
        return self.angleZ

    def distance(self):
        return self.distance

    def rotate(self,angle,plane = None):
        #for right now the plane part does nothing, but later on it should be used
        #this rotates the current vector around 0,0,0 (which I do not remember if that goes without saying)
        if not is_num.isNumber(angle):
            raise IncorrectInput("The first agrument must be a number")

        if plane is None:
            #easy case we assume the plane is x,y,z=0
            angle = is_num.angle(angle)
            x = (self.x * math.cos(angle)) - (self.y * math.sin(angle))
            y = (self.x * math.sin(angle)) + (self.y * math.cos(angle))

            return Vector(x,y,self.z)

        elif isinstance(plane,Plane):
            print("This does not do anything right now.\nPlease come back later")
        else:
            raise IncorrectInput("The second agrument must be nothing, or a Plane")

    def unitVector(self):
        #this returns a vector of length 1
        if self.distance == 0:
            return Vector(1,0,0)
        else:
            x = self.x/self.distance
            y = self.y/self.distance
            z = self.z/self.distance
            return Vector(x,y,z)

    def __init__(self,x = None,y = None,z = None):
        Coordinate.__init__(self,x,y,z)

        self.distance = Coordinate.distance(self,Coordinate())
        # This is just the distance to the origin
        if self.y == 0:
            self.angleXY = 0
        else:
            self.angleXY = math.tan(self.x/self.y)

        self.distanceXY = self.getDistanceXY()

        #cos = a/h
        #a = distanceXY
        #h = distance
        if(self.distance == 0):
            self.angleZ = 0
        else:
            self.angleZ = math.acos(self.distanceXY/self.distance)

    def __str__(self):
        result = Coordinate.__str__(self)
        result += " Distance: " + str(self.distance)
        result += " angleXY: " + str(self.angleXY)
        result += " angleZ: " + str(self.angleZ)
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
        #This accepts Vector / Constant = Vector
        if is_num.isNumber(other):
            if other != 0:
                inverse = 1/float(other)
                return self * inverse
            else:
                raise DivideByZero("You cannot Divide by Zero")
        else:
            raise IncorrectDivision("You must divide a Vector by a Constant")