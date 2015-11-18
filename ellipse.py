import coordinate
import is_num
import numpy
import math
import matplotlib.pyplot as plt

class Ellipse:

    def __init__(self,focal_one,focal_two,vector_normal,distance):

        #first I need to sanitize the data
        
        if isinstance(focal_one,coordinate.Coordinate):
            self.focal_one = focal_one
        else:
            raise IncorrectInput("The first argument must be a Coordinate")

        if isinstance(focal_two,coordinate.Coordinate):
            self.focal_two = focal_two
        else:
            raise IncorrectInput("The second argument must be a Coordinate")

        #distance is 2r for a circle and  r + r' for all ellispes
        #also 2* semimajoraxis
        if is_num.isNumber(distance):
            self.semimajoraxis = float(distance)/2
        else:
            raise IncorrectInput("The third argument must be a number")

        #the inclination angle is in radians
        if isinstance(vector_normal,coordinate.Vector):
            #this causes problems for circles
            self.vector_normal = vector_normal
        else:
            raise IncorrectInput("The fourth argument must be a Coordinate")

        self.plane = coordinate.Plane(self.vector_normal,self.focal_one)
        self.vector = self.focal_one - self.focal_two
        #this vector is from focal_one to focal_two
        self.eccentricity = self.vector.distance/(self.semimajoraxis * 2)
        if self.eccentricity > 1:
            raise IncorrectInput("These inputs do not produce a valid Ellipse")
        self.semiminor_axis = math.sqrt(self.semimajoraxis**2 * (1-self.eccentricity**2))
        self.area = math.pi * self.semimajoraxis * self.semiminor_axis

        #this vector is from focal_one to focal_two

    def __str__(self):

        string = "Focal One = " + str(self.focal_one)
        string += "\nFocal Two = " + str(self.focal_two)
        string += "\nEccentricity = " + str(self.eccentricity)
        string += "\nPlane = " + str(self.plane)
        string += "\nSemimajor Axis = " + str(self.semimajoraxis)
        string += "\nSemiminor Axis = " + str(self.semiminor_axis)
        string += "\nArea = " + str(self.area)
        string += "\nVector = " + str(self.vector)
        return string

    def distance(self,theta):
        #this result is distance from the focal that the angle is with respect to

        #however for the result to be uselful it needs to be oriented to whatever rotation you are using
        #for example if theta is pi/2 then it will give the distance to the point directly above focal_one 
        # in the ellipse's own plane of reference

        theta = is_num.angle(theta)
        result = theta
        #this makes the angle <= 2pi and > 0
        if theta is not None:
            result = self.semimajoraxis * (1 - self.eccentricity**2)
            result = result / (1 + (self.eccentricity * math.cos(theta)))
        return result

    def get_location(self,theta):
        #this is the coordinate that is given when the angle from focal_one is angle
        distance = self.distance(theta)
        #this could be None at this point if theta is not a number
        #if distance is not None then theta is not None as well
        if distance is not None:
            current_location = self.vector.unitVector() * distance
            current_location = self.plane.rotate(current_location,theta)
            current_location = self.focal_two + current_location
        return current_location

    def get_coordinates(self,points = None):
        #this returns the coordinates of the ellipse
        #this is with respect to angle, not time becuase an ellipse isn't an orbit
        #hopefully this helps me implement both displaying the ellipses and projecting them

        if points is None:
            points = 1000 #default
            
        theta_values = numpy.linspace(0,math.pi*2,points)

        coordinates = []    

        for i in theta_values:

            coordinates.append(self.get_location(i))

        return coordinates

    def plot3(self,points = None):

        coordinates = self.get_coordinates(points)

        x_values = []
        y_values = []
        z_values = []
        cardinalPoints = []
        cardinal_x_values = []
        cardinal_y_values = []
        cardinal_z_values = []

        max_x = None
        max_y = None
        max_z = None

        min_x = None
        min_y = None
        min_z = None

        for a in coordinates:
            x_addition = a.getX()
            y_addition = a.getY()
            z_addition = a.getZ()

            x_values.append(x_addition)
            y_values.append(y_addition)
            z_values.append(z_addition)

            if(max_x is None or x_addition > max_x):
                max_x = x_addition
            if(min_x is None or x_addition < min_x):
                min_x = x_addition
            if(max_y is None or y_addition > max_y):
                max_y = y_addition
            if(min_y is None or y_addition < min_y):
                min_y = y_addition
            if(max_z is None or z_addition > max_z):
                max_z = z_addition
            if(min_z is None or z_addition < min_z):
                min_z = z_addition

        x_difference = max_x - min_x
        y_difference = max_y - min_y
        z_difference = max_z - min_z

        increase = .1

        max_x += 1 + x_difference * increase
        min_x -= 1 + x_difference * increase

        max_y += 1 + y_difference * increase
        min_y -= 1 + y_difference * increase

        max_z += 1 + z_difference * increase
        min_z -= 1 + z_difference * increase

        #we have our normal ellipse values plotted
        #now to make sure that this works we will also plot the cardinal points of the ellipse
        #(The cardinal points are the two farest away points and the two closest points)
        #or the points at either end of the semi major/minor axises 

        distance_along_semimajoraxis = ((1 - self.eccentricity) * self.semimajoraxis)
        #a(1-e)
        unitVector = self.vector.unitVector()
        middle = self.focal_one + (self.vector/2)
        perpendicular_vector = self.plane.rotate(unitVector,math.pi/2)

        cardinalPoints.append(self.focal_two + (unitVector * distance_along_semimajoraxis))
        cardinalPoints.append(self.focal_one - (unitVector * distance_along_semimajoraxis))
        #this is negative becuase self.vector is going in the opposite direction
        #these are the semimajor end points

        cardinalPoints.append(middle + (perpendicular_vector * self.semiminor_axis))
        cardinalPoints.append(middle - (perpendicular_vector * self.semiminor_axis))
        #this is negative becuase perpendicular_vector is going in the opposite direction
        #these are the semiminor end points

        for i in cardinalPoints:
            cardinal_x_values.append(i.getX())
            cardinal_y_values.append(i.getY())
            cardinal_z_values.append(i.getZ())

        #These cardinal points help me make sure that the correct ellipse is being plotted

        fig = plt.figure(figsize = (8,13))
        #the above number are arbirary numbers, I just picked some I liked to be the size of the big image it makes
        #I thought about making a function to do this, but it seemed unnessary

        xy = fig.add_subplot(311,aspect = 'equal',title = "X-Y Plane")
        xy.scatter(x_values,y_values,color = 'green')
        xy.axis([min_x,max_x,min_y,max_y])
        #Below is the central focal points and the cardinal points
        xy.scatter([self.focal_one.getX(),self.focal_two.getX()],[self.focal_one.getY(),self.focal_two.getY()],color = 'red')
        xy.scatter(cardinal_x_values,cardinal_y_values,color = 'blue')

        zy = fig.add_subplot(312,aspect = 'equal',title = "Y-Z Plane")
        zy.scatter(z_values,y_values,color = 'green')
        zy.axis([min_z,max_z,min_y,max_y])
        #Below is the central focal points and the cardinal points
        zy.scatter([self.focal_one.getZ(),self.focal_two.getZ()],[self.focal_one.getY(),self.focal_two.getY()],color = 'red')
        zy.scatter(cardinal_z_values,cardinal_y_values,color = 'blue')

        xz = fig.add_subplot(313,aspect = 'equal',title = "X-Z Plane")
        xz.scatter(x_values,z_values,color = 'green')
        xz.axis([min_x,max_x,min_z,max_z])
        #Below is the central focal points and the cardinal points
        xz.scatter([self.focal_one.getX(),self.focal_two.getX()],[self.focal_one.getZ(),self.focal_two.getZ()],color = 'red')
        xz.scatter(cardinal_x_values,cardinal_z_values,color = 'blue')

        plt.show()

class Circle(Ellipse):

    #this is a specific case of an ellipse

    def __init__(self,focal,vector_normal,radius):
        #first I need to sanitize the data
        
        if isinstance(focal,coordinate.Coordinate):
            self.focal_one = focal
            self.focal_two = focal
        else:
            raise IncorrectInput("The first argument must be a Coordinate")

        if isinstance(vector_normal,coordinate.Vector):
            self.vector_normal = vector_normal
        else:
            raise IncorrectInput("The second argument must be a Vector")

        #distance is 2r for a circle and  r + r' for all ellispes
        #also 2* semimajoraxis
        if is_num.isNumber(radius):
            self.semimajoraxis = float(radius)
        else:
            raise IncorrectInput("The fourth argument must be a number")

        self.plane = coordinate.Plane(self.vector_normal,focal)
        self.vector = self.focal_one - self.focal_two
        #this vector is from focal_one to focal_two
        self.eccentricity = self.vector.distance/(self.semimajoraxis * 2)
        if self.eccentricity > 1:
            raise IncorrectInput("These inputs do not produce a valid Ellipse")
        self.semiminor_axis = math.sqrt(self.semimajoraxis**2 * (1-self.eccentricity**2))
        self.area = math.pi * self.semimajoraxis * self.semiminor_axis

        #this vector is from focal_one to focal_two



