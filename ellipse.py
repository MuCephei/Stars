import coordinate
import is_num
import numpy
import math
import matplotlib.pyplot as plt

class Ellipse:

    def __init__(self,focal_one,focal_two,thirdPoint,distance):

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
        if isinstance(thirdPoint,coordinate.Coordinate):
            #this causes problems for circles
            self.plane = coordinate.Plane(self.focal_one,self.focal_two,thirdPoint)
        else:
            raise InncorectInput("The fourth argument must be a Coordinate")

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

    def get_coordinates(self,points = None):
        #this returns the coordinates of the ellipse
        #this is with respect to angle, not time becuase an ellipse isn't an orbit
        #hopefully this helps me implement both displaying the ellipses and projecting them

        #Doesn't work well
        #**********************************************************************************************

        if points is None:
            points = 1000 #default
            
        theta_values = numpy.linspace(0,math.pi*2,points)

        coordinates = []    

        angle_offset = self.vector.get_angleXY() 

        for i in theta_values:
            d = self.distance(i)
            current_location = self.vector.unitVector() * d
            current_location = self.plane.rotate(current_location,i+angle_offset)
            #at this point the current_location vector points to a spot that is independant of the angle of the ellipse
            #so we need to rotate it appropriatly
            # current_location = self.plane.rotate(current_location,angle_offset)
            current_location = self.focal_two + current_location
            coordinates.append(current_location)
            # print(i+angle_offset)
            # print(current_location)

        return coordinates

    def plot_YZ(self,points = None):
        #This is unlickely to be used in the end but I want to make sure get_coordinates works

        coordinates = self.get_coordinates(points)

        y_values = []
        z_values = []

        for a in coordinates:
            y_values.append(a.getY())
            z_values.append(a.getZ())

        fig = plt.figure(figsize = (10,10))
        ax = fig.add_subplot(111,aspect = 'equal',title = "Y-Z Plane")

        ax.scatter(y_values,z_values,color = 'purple')
        #the colours are different so I know at a glance which way it's projecting it

        plt.show()

    def plot_XY(self,points = None):
        #this is to help with the testing of get_coordinates
        #this seems to work great
        #which mwans that the problem has to do with get_coordinate - I think it give funny Z values

        coordinates = self.get_coordinates(points)

        x_values = []
        y_values = []

        for a in coordinates:
            x_values.append(a.getX())
            y_values.append(a.getY())

        fig = plt.figure(figsize = (10,10))
        ax = fig.add_subplot(111,aspect = 'equal',title = "X-Y Plane")

        ax.scatter(x_values,y_values,color = 'orange')

        plt.show()

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
        perpendicular_vector = unitVector.rotate(math.pi/2)

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
        xy.scatter(x_values,y_values,color = 'orange')
        xy.axis([min_x,max_x,min_y,max_y])
        #Below is the central focal points and the cardinal points
        xy.scatter([self.focal_one.getX(),self.focal_two.getX()],[self.focal_one.getY(),self.focal_two.getY()],color = 'red')
        xy.scatter(cardinal_x_values,cardinal_y_values,color = 'blue')

        yz = fig.add_subplot(312,aspect = 'equal',title = "Y-Z Plane")
        yz.scatter(y_values,z_values,color = 'blue')
        yz.axis([min_y,max_y,min_z,max_z])
        #Below is the central focal points and the cardinal points
        yz.scatter([self.focal_one.getY(),self.focal_two.getY()],[self.focal_one.getZ(),self.focal_two.getZ()],color = 'red')
        yz.scatter(cardinal_y_values,cardinal_z_values,color = 'blue')

        xz = fig.add_subplot(313,aspect = 'equal',title = "X-Z Plane")
        xz.scatter(x_values,z_values,color = 'green')
        xz.axis([min_x,max_x,min_z,max_z])
        #Below is the central focal points and the cardinal points
        xz.scatter([self.focal_one.getX(),self.focal_two.getX()],[self.focal_one.getZ(),self.focal_two.getZ()],color = 'red')
        xz.scatter(cardinal_x_values,cardinal_z_values,color = 'blue')

        plt.show()

    def plot_2D(self,points = None):
        #im leaving this here while I make a more powerfull version that is also smaller/ easier to read
        #this plots the ellipse in the xy plane
        # in the future I plan on being able to plot on an arbitrary plane
        # but for now we need this for testing

        #points is the number of points that we will use in the scatterplot

        if points is None:
            points = 1000 #default

        #for right now this is going to plot the four "corners" of the ellipse
        cardinalPoints = []
        cardinal_x_values = []
        cardinal_y_values = []

        distance_along_semimajoraxis = ((1 - self.eccentricity) * self.semimajoraxis)
        #a(1-e)

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
            cardinal_x_values.append(i.getX())
            cardinal_y_values.append(i.getY())
            x += 1

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

        offset = self.vector.get_angleXY()
        #half the time this is backwards
        #and can be fixed by adding pi, but then that screws up the other times

        for i in theta_values:
            d = self.distance(i)
            x = d * math.cos(i)
            y = d * math.sin(i)
            current_location = coordinate.Vector(x,y)
            #at this point the current_location vector points to a spot that is independant of the angle of the ellipse
            #so we need to rotate it appropriatly
            current_location = current_location.rotate(offset)
            current_location = self.focal_two + current_location
            #this will not work in 3D space
            #we are using focal_two becuase it is at the end of self.vector
            x_addition = current_location.getX()
            y_addition = current_location.getY()
            x_values.append(x_addition)
            y_values.append(y_addition)

            if(max_x is None or x_addition > max_x):
                max_x = x_addition
            if(min_x is None or x_addition < min_x):
                min_x = x_addition
            if(max_y is None or y_addition > max_y):
                max_y = y_addition
            if(min_y is None or y_addition < min_y):
                min_y = y_addition

        x_difference = max_x - min_x
        y_difference = max_y - min_y

        increase = .1

        max_x += x_difference * increase
        min_x -= x_difference * increase

        max_y += y_difference * increase
        min_y -= y_difference * increase

        fig = plt.figure(figsize = (10,10))
        ax = fig.add_subplot(111,aspect = 'equal',title = "X-Y Plane")

        #ax.axis([min_x,max_x,min_y,max_y])

        ax.scatter([self.focal_one.getX(),self.focal_two.getX()],[self.focal_one.getY(),self.focal_two.getY()],color = 'red')

        ax.scatter(x_values,y_values,color = 'green')

        ax.scatter(cardinal_x_values,cardinal_y_values,color = 'blue')

        plt.show()



class Circle(Ellipse):

    #this is a specific case of an ellipse

    def __init__(self,focal,point_one,point_two,radius):
        #first I need to sanitize the data
        
        if isinstance(focal,coordinate.Coordinate):
            self.focal_one = focal
            self.focal_two = focal
        else:
            raise InncorectInput("The first argument must be a Coordinate")

        if not isinstance(point_one,coordinate.Coordinate):
            raise InncorectInput("The second argument must be a Coordinate")

        #distance is 2r for a circle and  r + r' for all ellispes
        #also 2* semimajoraxis
        if is_num.isNumber(radius):
            self.semimajoraxis = float(radius)
        else:
            raise InncorectInput("The fourth argument must be a number")

        #the inclination angle is in radians
        if isinstance(point_two,coordinate.Coordinate):
            #this causes problems for circles
            self.plane = coordinate.Plane(self.focal_one,point_one,point_two)
        else:
            raise InncorectInput("The third argument must be a Coordinate")

        self.vector = self.focal_one - self.focal_two
        #this vector is from focal_one to focal_two
        self.eccentricity = self.vector.distance/(self.semimajoraxis * 2)
        if self.eccentricity > 1:
            raise InncorectInput("These inputs do not produce a valid Ellipse")
        self.semiminor_axis = math.sqrt(self.semimajoraxis**2 * (1-self.eccentricity**2))
        self.area = math.pi * self.semimajoraxis * self.semiminor_axis

        #this vector is from focal_one to focal_two



