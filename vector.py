import is_num
import math

class Vector:
    #three demensional vector
    def __init__(self,distance,angleXY,angleZ = None):

        if is_num.isNumber(distance):
            self.distance = distance
        else:
            self.distance = 0

        self.angleXY = is_num.isAngle(angleXY)
        if angleXY is None:
            self.angleXY = 0

        self.angleZ = is_num.isAngle(angleZ)
        if angleZ is None:
            self.angleZ = 0
        
        distanceXY = self.distance * math.cos(self.angleZ)                
        self.i = distanceXY * math.sin(self.angleXY)
        self.j = distanceXY * math.cos(self.angleXY)
        self.k = distance * math.sin(self.angleZ)
        #i = x
        #j = y
        #k = z

    def addCoor(self,other):
        #we know that other is a Coordinate here
        x = other.getX()
        y = other.getY()
        z = other.getZ()

        result = Coordinate(x+self.i,y+self.j,z+self.k)
        return result


    def __add__(self,other):
        if isinstance(other,Coordinate):
            return self.addCoor(other)
        else:
            return other

    def get_xy(self):
        return self.angleXY

    def get_z(self):
        return self.angleZ

class Coordinate:
    # note that coordinates are static points in space that cannot change with time

    def __init__(self,x = None,y = None,z = None):
        #make this make sure that the coordianates are some sort of number
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
        result = "Error"
        if isinstance(other,Coordinate):
            deltaX = self.x - other.getX()
            deltaY = self.y - other.getY()
            deltaZ = self.z - other.getZ()
            result = math.sqrt(deltaX**2 + deltaY**2 + deltaZ**2)
        return result

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def addCoor(self,other):
        #this returns a vector from self to other
        distance = self.distance(other)
        x = other.getX() - self.x
        y = other.getY() - self.y
        #we need the relative coordinates for this
        #we also need the xy distance
        distanceXY = math.sqrt(x**2+y**2)
        
        if x == 0:
            angleXY = 0
        else:
            angleXY = math.atan(y/x)
        angleZ = math.acos(distanceXY/distance)
        vector = Vector(distance,angleXY,angleZ)
        return vector

    def addVector(self,other):
        #this returns a Coordinate
        return other + self

    def __add__(self,other):
        if isinstance(other,Coordinate):
            return self.addCoor(other)
        elif (isinstance(other,Vector)):
            return self.addVector(other)
        else:
            return other

    def __sub__(self,other):
        if isinstance(other,Coordinate):
            return self.subCoor(other)
        else:
            return other
