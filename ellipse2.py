import coordinate
import is_num
import numpy
import math
import matplotlib.pyplot as plt

class Ellipse:

    def __init__(self,focal_one,focal_two,distance,inclination_angle = None):

        #first I need to sanitize the data
        
        if isinstance(focal_one,coordinate.Coordinate):
            self.focal_one = focal_one
        else:
            raise InncorectInput("The first argument must be a Coordinate")

        if isinstance(focal_two,coordinate.Coordinate):
            self.focal_two = focal_two
        else:
            raise InncorectInput("The second argument must be a Coordinate")

        #distance is 2r for a circle and  r + r' for all ellispes
        #also 2* semimajoraxis
        if is_num.isNumber(distance):
            self.semimajoraxis = float(distance)/2
        else:
            raise InncorectInput("The third argument must be a number")

        #the inclination angle is in radians
        if inclination_angle is None:
            self.inclination_angle = 0
        elif is_num.isNumber(inclination_angle):
            self.inclination_angle = is_num.angle(inclination_angle)
        else:
            raise InncorectInput("The fourth argument must be a number")

        self.vector = self.focal_one - self.focal_two
        #this vector is from focal_one to focal_two
        self.eccentricity = self.vector.distance/(self.semimajoraxis * 2)
        if self.eccentricity > 1:
            raise InncorectInput("These inputs do not produce a valid Ellipse")
        self.semiminor_axis = math.sqrt(self.semimajoraxis**2 * (1-self.eccentricity**2))
        self.area = math.pi * self.semimajoraxis * self.semiminor_axis

        #this vector is from focal_one to focal_two

    def __str__(self):

        string = "Focal One = " + str(self.focal_one)
        string += "\nFocal Two = " + str(self.focal_two)
        string += "\nEccentricity = " + str(self.eccentricity)
        string += "\nInclination Angle = " + str(self.inclination_angle)
        string += "\nSemimajor Axis = " + str(self.semimajoraxis)
        string += "\nSemiminor Axis = " + str(self.semiminor_axis)
        string += "\nArea = " + str(self.area)
        string += "\nVector = " + str(self.vector)
        return string

    def radius(self,theta):
        #this result is distance from the focal that the angle is with respect to

        #however for the result to be uselful it needs to be oriented to whatever plane you are using
        #for example if theta is pi/2 then it will give the distance to the point directly above focal_one 
        # in the ellipse's own plane of reference

        theta = is_num.angle(theta)
        result = theta
        #this makes the angle <= 2pi and > 0
        if theta is not None:
            result = self.semimajoraxis * (1 - self.eccentricity**2)
            result = result / (1 + (self.eccentricity * math.cos(theta)))
        return result

    def plot_2D(self,points = None):
        #this plots the ellipse in the xy plane
        # in the future I plan on being able to plot on an arbitrary plane
        # but for now we need this for testing

        #points is the number of points that we will use in the scatterplot

        if points is None:
            points = 1000 #default

        #for right now this is going to plot the four "corners" of the ellipse
        cardinalPoints = []
        x_values = []
        y_values = []

        distance_along_semimajoraxis = ((1 - self.eccentricity) * self.semimajoraxis)

        unitVector = self.vector.unitVector()

        cardinalPoints.append(self.focal_two + (unitVector * distance_along_semimajoraxis))

        cardinalPoints.append(self.focal_one - (unitVector * distance_along_semimajoraxis))
        #this is negative becuase self.vector is going in the opposite direction

        middle = self.focal_one + (self.vector/2)

        perpendicular_vector = unitVector.rotate(math.pi/2)

        cardinalPoints.append(middle + (perpendicular_vector * self.semiminor_axis))

        cardinalPoints.append(middle - (perpendicular_vector * self.semiminor_axis))

        x = 0
        for i in cardinalPoints:
            print(x)
            print(i)
            x_values.append(i.getX())
            y_values.append(i.getY())
            x += 1

        fig = plt.figure(figsize = (10,10))
        ax = fig.add_subplot(111,aspect = 'equal',title = "X-Y Plane")

        #ax.axis([min_x,max_x,min_y,max_y])

        ax.scatter([self.focal_one.getX(),self.focal_two.getX()],[self.focal_one.getY(),self.focal_two.getX()],color = 'red')

        ax.scatter(x_values,y_values,color = 'blue')

        plt.show()


"""


        theta_values = numpy.linspace(0,2*math.pi,points)
        # equally spaced angles
        #note that this will not mean equally spaced points on the graph

        x_values = []
        y_values = []
        max_x = None
        min_x = None
        max_y = None    
        min_y = None
        #these are fields that are going to be used in the graph
        #I set the max and min fields to None so I don't have to assume where in cartesian space I will be

        #the vector of the ellipse (points from focal_one to focal_two) will contain the information required 
        # to understand the result from radius(theta)

        #remember that radius(theta) assumes we gave it the angle from it's own plane of reference
        # where self.vector is along the x axis

        offset = self.vector.get_angleXY()

        for i in theta_values:
            d = self.radius(i)
            phi = i + offset
            #phi is the angle that you are from from focal_one
            #it's focal_one becuase we used self.vector
            #we can use focal_two by instead using -1*self.vector
            x = self.focal_one.getX() + d*math.cos(phi)
            y = self.focal_one.getY() + d*math.sin(phi)
            #remember that d is distance from the focal we chose (one)
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
            #these are so we can have the graph be the right size

        x_difference = max_x - min_x
        y_difference = max_y - min_y

        increase = .1

        max_x += x_difference * increase
        min_x -= x_difference * increase

        max_y += y_difference * increase
        min_y -= y_difference * increase

        #what I did above was make the upper and lowers bounds of the graph increase
        # so we have space on the edges

        fig = plt.figure(figsize = (10,10))
        ax = fig.add_subplot(111,aspect = 'equal',title = "X-Y Plane")

        ax.axis([min_x,max_x,min_y,max_y])

        ax.scatter([self.focal_one.getX(),self.focal_two.getX()],[self.focal_one.getY(),self.focal_two.getX()])

        ax.scatter(x_values,y_values)

        plt.show()

"""




