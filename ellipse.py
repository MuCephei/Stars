import vector
import is_num
import numpy
import math
import matplotlib.pyplot as plt

class Ellipse:
    
    def __init__(self,focal_one,focal_two,eccentricity = None):

        if isinstance(focal_one,vector.Coordinate):
            self.focal_one = focal_one
        else:
            print("Error: Creating an Ellipse\nfocal_one is not a vector.Coordinate")
            self.focal_one = vector.Coordinate()

        if isinstance(focal_two,vector.Coordinate):
            self.focal_two = focal_two
        else:
            print("Error: Creating an Ellipse\nfocal_two is not a vector.Coordinate")
            self.focal_two = vector.Coordinate()

        if eccentricity is not None and is_num.isNumber(eccentricity):
            self.eccentricity = eccentricity
        else:
            self.eccentricity = 0

        self.semimajor_axis = focal_one.distance(focal_two)/2
        self.semiminor_axis = math.sqrt(self.semimajor_axis**2*(1-self.eccentricity**2))
        self.area = math.pi * self.semimajor_axis * self.semiminor_axis
        self.theta = math.atan((focal_one.getX()-focal_two.getX())/(focal_one.getY()-focal_two.getY()))


    def __str__(self):
        string = "Focal One = " + str(self.focal_one)
        string += "\nFocal Two = " + str(self.focal_two)
        string += "\nEccentricity = " + str(self.eccentricity)
        string += "\nSemimajor axis = " + str(self.semimajor_axis)
        string += "\nSemiminor axis = " + str(self.semiminor_axis)
        string += "\nArea = " + str(self.area)
        return string

    def radius(self,theta_input):
        #this result is from the primary axis or focal_one
        #self.theta is the rotation of the ellipse while theta_input is the theta with reference to focal_one
        #this means that theta + theta_input will give angle I want
        theta = is_num.isAngle(self.theta + theta_input)
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
        #this accepts a vector.Vector to the first focal point
        #it returns another Ellispse that is not to scale of the distance viewed
        if not isinstance(other,vector.Vector):
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
            v = vector.Vector(r,i)
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