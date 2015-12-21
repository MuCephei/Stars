#This is the backbone of the whole operation
#This module include coordinates,vectors and planes
#more information will be included in each class
import is_num
import math

class Coordinate:
    #A coordinate has x,y,z values and can find the distance between itself and another point
    #it can also find the shortest path between a path made by two other coordinates and it self

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

    def shortest_path(self,a,b):
        #this finds the shorestest path from self to the line made by a and b
        #this is motivated by the area between three points being a triangle
        #the top portion is twice the area of said triangle (by making a rectangle)
        top = (self - a)*(self - b)
        #note that self-a gives a vector from self to a
        result =  top.distance
        #the cross product of the two vectors above has a distance equal to the area of the square
        result = result /b.distance(a)
        #recall that a triangle is base*height/2
        #so if the square is twice the area of the triangle (or base * height)
        #then dividing by base gives height, and the diseired length
        return result

    def distance(self,other):
        #gives distance from self to other
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

    def getDirection(self,letter):
        #The name is a little unclear
        #This is where you give a letter as an input, say i
        #and it will give you the X value
        if (letter == 'x' or letter == 'i' or letter == 'X' or letter == 'I'):
            return self.x
        elif (letter == 'y' or letter == 'j' or letter == 'Y' or letter == 'J'):
            return self.y
        elif (letter == 'z' or letter == 'k' or letter == 'Z' or letter == 'K'):
            return self.z
        else:
            return None

    def __add__(self,other):
        #This only accepts Coordinate + Vector = Coordinate in that particular order
        if isinstance(other,Vector):
            x = self.x + other.getX()
            y = self.y + other.getY()
            z = self.z + other.getZ()
            return Coordinate(x,y,z)
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
            #other is b
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

#*******************************************************************************************************

class Vector(Coordinate):
    #Note that vector when expressed like this is just a dimension, and has no starting point
    #For convienience I express the vector as starting at 0 (a coordinate)

    def getDistanceXY(self):
        #this is the length of the vector as if it had no z value
        # or it was flatened onto the ground

        flat = Coordinate(self.x,self.y)
        return flat.distance(Coordinate())
        # This is the distance to the origin

    def coordinate(self):
        return Coordinate(self.x,self.y,self.z)

    def get_angleXY(self):
        return self.angleXY

    def get_angleZ(self):
        return self.angleZ

    def get_distance(self):
        return self.distance

    def rotate(self,angle):
        #if you want to rotate something on a plane then use Plane's rotate method
        #this rotates the current vector around 0,0,0 (which I do not remember if that goes without saying)
        if not is_num.isNumber(angle):
            raise IncorrectInput("The first agrument must be a number")

        x = (self.x * math.cos(angle)) - (self.y * math.sin(angle))
        y = (self.x * math.sin(angle)) + (self.y * math.cos(angle))

        return Vector(x,y,self.z)

    def unitVector(self):
        #this returns a vector of length 1
        if self.distance == 0:
            return Vector(1,0,0)
        else:
            x = self.x/self.distance
            y = self.y/self.distance
            z = self.z/self.distance
            return Vector(x,y,z)

    def find_orthagonal(self):
        #this returns a vector orthagonal in the x axis 90 degrees
        if(self.x != 0 and self.y == 0 and self.z == 0):
            #this is when the vector is exactly x
            #here we just return y
            result = Vector(0,1,0)
        else:
            result = self*Vector(1,0,0)
        return result

    def __init__(self,x = None,y = None,z = None):
        Coordinate.__init__(self,x,y,z)

        self.distance = Coordinate.distance(self,Coordinate())
        # This is just the distance to the origin
        if self.x == 0 and self.y > 0:
            self.angleXY = math.pi/2
        elif self.x == 0 and self.y < 0:
            self.angleXY = 3 * math.pi/2
        elif self.x == 0 and self.y == 0:
            self.angleXY = 0
            #this one is kindof arbirtrary
        else:
            #I need to take into account the quadrants here
            #Q1 and Q2 are good the way they are
            self.angleXY = math.atan(self.y/self.x)
            if self.y < 0:
                self.angleXY += math.pi

        self.distanceXY = self.getDistanceXY()

        #cos = a/h
        #a = distanceXY
        #h = distance
        if(self.distance == 0):
            self.angleZ = 0
        else:
            #quadrants are important here as well
            self.angleZ = math.acos(self.distanceXY/self.distance)
            if self.distanceXY < 0:
                self.angleZ += math.pi

    def __str__(self):
        result = Coordinate.__str__(self)
        result += " Distance: " + str(self.distance)
        result += " angleXY: " + str(self.angleXY)
        result += " angleZ: " + str(self.angleZ)
        return result

    def __eq__(self,other):
        if isinstance(other,Vector):
            result = True
            if(other.get_distance() != self.distance):
                result = False
            elif(other.getX() != self.x):
                result = False
            elif(other.getY() != self.y):
                result = False
            elif(other.getZ() != self.z):
                result = False
            return result
        else:
            raise IncorrectEquality("You must compare two Vectors")

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

    def __eq__(self,other):
        #The other point must be a Vector
        if isinstance(other,Vector):
            if self.x == other.getX():
                if self.y == other.getY():
                    if self.z == other.getZ():
                        return False
        return True

#*******************************************************************************************************

class Plane:

    def __init__(self,vector_normal,point):
        #the equation fo a plane is 
        #ax + by + cz = d
        #where one of a,b or c is not 0

        #make sure that the first input is a coordinate
        if isinstance(vector_normal,Vector):
            self.vector_normal = vector_normal.unitVector()
        else:
            raise IncorrectInput("The first input must be a Vector")

        if not isinstance(point,Coordinate):
            raise IncorrectInput("The second input must be a Coordinate")

        self.a = self.vector_normal.getX()#note that self.(a, b and c) have unimportant magnitudes
        self.b = self.vector_normal.getY()
        self.c = self.vector_normal.getZ()
        self.d = self.a * point.getX() + self.b * point.getY() + self.c * point.getZ()
        #self.a is from the formula while point.getX() is the value of the input coordinate

    def left(self,other):
        return self.a * other.getX() + self.b * other.getY() + self.c * other.getZ() - self.d

    def on_plane(self,other):
        #this tells you if a coordinate or vector is on the plane
        #seems to work so far
        result = False
        if isinstance(other,Coordinate) or isinstance(other,Vector):
            if self.d * 1.001 >= self.a * other.getX() + self.b * other.getY() + self.c * other.getZ():
                if self.d * .999 <= self.a * other.getX() + self.b * other.getY() + self.c * other.getZ():
                    result = True
            if self.d * 1.001 <= self.a * other.getX() + self.b * other.getY() + self.c * other.getZ():
                if self.d * .999 >= self.a * other.getX() + self.b * other.getY() + self.c * other.getZ():
                    result = True
            #this is designed to allow for a slight rounding error        
        else:
            raise IncorrectInput("The first input must be a coordinate")
        return result

    def rotate(self,other,angle):
        #this rotates an vector around the vector normal to the plane
        #returns a vector
        if not isinstance(other,Vector):
            raise IncorrectInput("The first input must be a Vector")

        if not is_num.isNumber(angle):
            raise IncorrectInput("The second agrument must be a number")

        cross = (other * self.vector_normal).unitVector()
        #this gives us a vector pointing in the right direction with a length of one
        result = cross * math.sin(angle)
        result += (other.unitVector() * math.cos(angle))
        result = result.unitVector()
        result = result * other.get_distance()
        return result

    def __str__(self):
        string = "Vector Normal = " + str(self.vector_normal)
        string += "\nA = " + str(self.a)
        string += "\nB = " + str(self.b)
        string += "\nC = " + str(self.c)
        string += "\nD = " + str(self.d)

        return string

origin = Coordinate()