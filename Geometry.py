import math
import matplotlib.pyplot as plt
import numpy

def isNumber(input):
    try:
        float(input)
        result = True
    except:
        result = False
    return result

def isAngle(input):
    return (isNumber(input) and input >= 0 and input <= 2*math.pi)

class Coordinate:
    # note that coordinates are static points in space that cannot change with time

    def __init__(self,x = None,y = None,z = None):
        #make this make sure that the coordianates are some sort of number
        self.x = 0
        self.y = 0
        self.z = 0
        if x is not None:
            if isNumber(x):
                self.x = x
            if y is not None:
                if isNumber(y):
                    self.y = y
                if z is not None:
                    if isNumber(z):
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
        angleXY = math.acos(other.getX()/other.getY())
        angleZY = math.acos(other.getZ()/other.getY())
        vector = Vector(distance,angleXY,angleZY)
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

class Vector:
    #three demensional vector
    def __init__(self,distance,angleXY,angleZY = None):

        if isNumber(distance):
            self.distance = distance
        else:
            self.distance = 0

        if isAngle(angleXY):
            self.angleXY = angleXY
        else:
            self.angleXY = 0

        if angleZY is not None and isAngle(angleZY):
            self.angleZY = angleZY
        else:
            self.angleZY = 0
                        
        self.i = distance * math.cos(self.angleXY)
        self.j = distance * (math.sin(self.angleXY) + math.cos(self.angleZY))
        self.k = distance * math.sin(self.angleZY)
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
        return angleXY

    def get_zy(self):
        return angleZY

class Ellipse:
    
    def __init__(self,focal_one,focal_two,eccentricity = None):

        if isinstance(focal_one,Coordinate):
            self.focal_one = focal_one
        else:
            print("Error: Creating an Ellipse\nfocal_one is not a Coordinate")
            self.focal_one = Coordinate()

        if isinstance(focal_two,Coordinate):
            self.focal_two = focal_two
        else:
            print("Error: Creating an Ellipse\nfocal_two is not a Coordinate")
            self.focal_two = Coordinate()

        if eccentricity is not None and isNumber(eccentricity):
            self.eccentricity = eccentricity
        else:
            self.eccentricity = 0

        self.semimajor_axis = focal_one.distance(focal_two)/2
        self.semiminor_axis = math.sqrt(self.semimajor_axis**2*(1-self.eccentricity**2))
        self.area = math.pi * self.semimajor_axis * self.semiminor_axis


    def __str__(self):
        string = "Focal One = " + str(self.focal_one)
        string += "\nFocal Two = " + str(self.focal_two)
        string += "\nEccentricity = " + str(self.eccentricity)
        string += "\nSemimajor axis = " + str(self.semimajor_axis)
        string += "\nSemiminor axis = " + str(self.semiminor_axis)
        string += "\nArea = " + str(self.area)
        return string

    def radius(self,theta):
        #this result is from the primary axis or focal_one
        #theta is in radians
        result = self.semimajor_axis * (1 - self.eccentricity**2)
        result = result / (1 + self.eccentricity * math.cos(theta))
        return result

    def plot_angle(self):
        # this plot is the radius as a function of angle
        radius = []
        theta = numpy.linspace(0,2*math.pi,1000)
        for x in theta:
            radius.append(self.radius(x))
        plt.plot(theta,radius)
        plt.xlabel('Radians')
        plt.show()

    def eccentricity_from_axis(self,semimajor_axis,semiminor_axis):
        result = (1+(semimajor_axis/semiminor_axis)) * (1-(semimajor_axis/semiminor_axis))
        result = math.sqrt(result)
        return result

    def viewed_from_angle(self,other):                                     
        #this accepts a Vector to the first focal point
        #it returns another Ellispse that is not to scale of the distance viewed
        if not isinstance(other,Vector):
            return None
        #somewhat janky but it means I don't have another level of indentation
        #for now I will try immplementing for just an angle variation on X
        new_focal_one = self.focal_one + other
        new_focal_two = self.focal_two + other

        



    def plot_cross_section(self,title,points = None):
        #Iproject the ellipse as a 2d object by using the plane of the ellipse as a referenec frame
        if points is None:
            points = 1000
        theta = numpy.linspace(0,2*math.pi,points)
        x_values = []
        y_values = []
        max_x = None
        min_x = None
        max_y = None
        min_y = None

        #this creates the values that will be plotted
        for i in theta:
            r = self.radius(i)
            v = Vector(r,i)
            location = v + self.focal_one
            x = location.getX()
            y = location.getY()
            x_values.append(x)
            y_values.append(y)
            if(max_x is None or x > max_x):
                max_x = x
            if(min_x is None or x < min_x):
                min_x = x
            if(max_y is None or y > max_y):
                max_y = y
            if(min_y is None or y < min_y):
                min_y = y

        x_difference = max_x - min_x
        y_difference = max_y - min_y

        #at this point we know the upper and lower bounds of the graph
        #so I'm going to add 10% to give some visibility

        increase = .1

        max_x += x_difference * increase
        min_x -= x_difference * increase

        max_y += y_difference * increase
        min_y -= y_difference * increase

        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111,aspect = 'equal',title = "X-Y Plane")

        ax.axis([min_x,max_x,min_y,max_y])

        ax.scatter(x_values,y_values)


        plt.show()


a = Coordinate(3,4)
b = Coordinate(10,-10)
#z-values don't quite work yet

circle_one = Ellipse(a,b)
ellipse_one = Ellipse(a,b,0.99)

print(circle_one)
#circle_one.plot_angle()
circle_one.plot_cross_section("Circle")
#is a circle, just doesn't look it

print("\n")

print(ellipse_one)
#ellipse_one.plot_angle()
ellipse_one.plot_cross_section("Ellipse")
#they always seem to look the same