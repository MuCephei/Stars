import coordinate
import is_num
import numpy
import math
import matplotlib.pyplot as plt

class Ellipse:

    def __init__(self,focal_one,focal_two,vector_normal,distance,size = None):

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
        self.eccentricity = self.vector.get_distance()/(self.semimajoraxis * 2)
        if self.eccentricity > 1:
            raise IncorrectInput("These inputs do not produce a valid Ellipse")
        self.semiminor_axis = math.sqrt(self.semimajoraxis**2 * (1-self.eccentricity**2))
        self.area = math.pi * self.semimajoraxis * self.semiminor_axis

        if size is None:
            self.size = 1
        elif is_num.isNumber(size):
            self.size = float(size)
        else:
            raise IncorrectInput("The six argument must be a number")

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

    def get_coordinates(self,theta_values,points = None):
        #this returns the coordinates of the ellipse
        #this is with respect to angle, not time becuase an ellipse isn't an orbit
        #hopefully this helps me implement both displaying the ellipses and projecting them

        if points is None:
            points = 1000 #default

        coordinates = []    

        for i in theta_values:

            coordinates.append(self.get_location(i))

        return coordinates

    def get_cardinalPoints(self):

        cardinalPoints = []

        #(The cardinal points are the two farest away points and the two closest points)
        #or the points at either end of the semi major/minor axises 

        distance_along_semimajoraxis = ((1 - self.eccentricity) * self.semimajoraxis)
        #a(1-e)
        unitVector = self.vector.unitVector()
        middle = self.focal_one + (self.vector/2)
        perpendicular_vector = self.plane.rotate(unitVector,math.pi/2)

        cardinalPoints.append(self.focal_two + (unitVector * distance_along_semimajoraxis))
        #purple
        cardinalPoints.append(self.focal_one - (unitVector * distance_along_semimajoraxis))
        #yellow
        #this is negative becuase self.vector is going in the opposite direction
        #these are the semimajor end points

        cardinalPoints.append(middle + (perpendicular_vector * self.semiminor_axis))
        #pink
        cardinalPoints.append(middle - (perpendicular_vector * self.semiminor_axis))
        #blue
        #this is negative becuase perpendicular_vector is going in the opposite direction
        #these are the semiminor end points

        return cardinalPoints

    def plot_bonus_point(self,figure,axis_one,axis_two,point):
        value_one = [point.getDirection(axis_one)]
        value_two = [point.getDirection(axis_two)]

        figure.scatter(value_one,value_two,color = 'black')

    def plotCardinal(self,figure,axis_one,axis_two):

        if not isinstance(figure,plt.Subplot):
            raise IncorrectInput("The first input must be a figure")

        if (self.focal_one.getDirection(axis_one) == None or self.focal_one.getDirection(axis_two) == None):
            raise IncorrectInput("The second and third inputs must be vaild axis names")

        cardinalPoints = self.get_cardinalPoints()
        colours = ('purple','yellow','pink','blue')
        #these are so the cardinal points may be indetified individually on the plot
        cardinal_one_values = []
        cardinal_two_values = []

        for i in cardinalPoints:
            cardinal_one_values.append(i.getDirection(axis_one))
            cardinal_two_values.append(i.getDirection(axis_two))

        figure.scatter([self.focal_one.getDirection(axis_one),self.focal_two.getDirection(axis_one)],
            [self.focal_one.getDirection(axis_two),self.focal_two.getDirection(axis_two)],color = 'red')
        figure.scatter(cardinal_one_values,cardinal_two_values,color = colours)

    def plot_specific_angles(self,figure,axis_one,axis_two,colour,theta_values,size = None):

        if not isinstance(figure,plt.Subplot):
            raise IncorrectInput("The first input must be a figure")

        if (self.focal_one.getDirection(axis_one) == None or self.focal_one.getDirection(axis_two) == None):
            raise IncorrectInput("The second and third inputs must be vaild axis names")

        if size is None:
            size = 1
        elif not is_num.isNumber(size) or size <= 0:
            raise IncorrectInput("The fifth input must be a positive number")

        coordinates = self.get_coordinates(theta_values,len(theta_values))

        one_values = []
        two_values = []

        for a in coordinates:
            one_values.append(a.getDirection(axis_one))
            two_values.append(a.getDirection(axis_two))

        figure.scatter(one_values,two_values,color = colour)

    def plot(self,figure,axis_one,axis_two,colour,size = None,points = None):
        #figure is the figure that the points are going to be plotteed on
        #I'm not sure how to gets

        #sanitize data

        if not isinstance(figure,plt.Subplot):
            raise IncorrectInput("The first input must be a figure")

        if (self.focal_one.getDirection(axis_one) == None or self.focal_one.getDirection(axis_two) == None):
            raise IncorrectInput("The second and third inputs must be vaild axis names")

        if points is None:
            points = 1000 #default

        if size is None:
            size = 1
        elif not is_num.isNumber(size) or size <= 0:
            raise IncorrectInput("The fifth input must be a positive number")

        theta_values = numpy.linspace(0,math.pi*2,points)

        coordinates = self.get_coordinates(theta_values)

        one_values = []
        two_values = []

        for a in coordinates:
            one_values.append(a.getDirection(axis_one))
            two_values.append(a.getDirection(axis_two))


        figure.scatter(one_values,two_values,s = size,color = colour)
        #Below is the central focal points and the cardinal points

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



