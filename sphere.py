import is_num
import math
import constants
import coordinate
import matplotlib.pyplot as plt
import random

class Sphere:
	#Celestial spheres are fun

	#This is intended to be used to implement stars that shine as well as objects that don't
	#This should be interpreted in the context of orbits but doens't need to be

	def __init__(self,radius,mass):
		#time to sanitize

		if is_num.isNumber(radius):
			self.radius = float(radius)
		else:
			raise IncorrectInput("The first argument must be a number")

		if is_num.isNumber(mass):
			self.mass = float(mass)
		else:
			raise IncorrectInput("The second argument must be a number")

		self.volume = 4/3 * math.pi * self.radius**3
		self.area = 4 * math.pi * self.radius**2
		self.area_2D = math.pi * self.radius**2
		self.averageDensity = self.volume/self.mass

	def flux(self,distance):
		return 0

	def get_2D_area(self):
		return self.area_2D

#I'm going to get back to fleshing out Stars later, but right now I want to get orbits done

class Star(Sphere):
	#This is a sphere that we know one hell of a lot more about
	#mostly from it's mass

	def __init__(self,radius,mass):
		self.luminosity = constants.solar_luminosity * (mass)**3.5
		Sphere.__init__(self,radius*constants.solar_radius,mass*constants.solar_mass)
		#I'm making a light array the consists of points, which each have a vector from the middle of the star
		base_vector = coordinate.Vector(0,0,1)

		total_limb_luminosity = 0

		#it is not possible to have a point for every meter
		#so we are going to have 1 000 000 randomly scattered points

		number_of_points = 10000
		#don't make this number much bigger than 50

		self.light_array = []

		for n in range(number_of_points):
			distance = random.uniform(0,self.radius)
			theta = random.uniform(0,math.pi*2)
			#now the randomness needs to be adjusted to not give a concentration in the center
			x = math.sqrt(distance) * math.cos(theta)
			y = math.sqrt(distance) * math.sin(theta)
			vector = coordinate.Vector(x,y)
			angle_from_center = math.asin(vector.distance/self.radius)
			curr_luminosity = 2/5 + (3 * math.cos(angle_from_center)/5)
			total_limb_luminosity = total_limb_luminosity + curr_luminosity
			self.light_array.append(Point(vector,curr_luminosity))

		self.luminosity_coefficient = self.luminosity/total_limb_luminosity

	def plot(self):
		#the star's center is it's reference point here
		x_values = []
		y_values = []
		intensity_values = []

		for i in self.light_array:
			x_values.append(i.vector.getX())
			y_values.append(i.vector.getY())
			intensity_values.append(1/i.intensity)

		plt.scatter(x_values,y_values,c=intensity_values,s = 10)
		plt.gray()
		plt.axis('equal')
		plt.show()


	def radius_in_AU(self):
		return self.radius/constants.AU

	def flux(self,distance):
		if is_num.isNumber(distance):
			distance = float(distance)
		else:
			raise IncorrectInput("The first argument must be a number")

		return self.luminosity/(4*math.pi*distance)

class Point():

	def __init__(self,vector,intensity):

		if isinstance(vector,coordinate.Vector):
			self.vector = vector
		else:
			raise IncorrectInput("The first argument must be a Vector")

		if is_num.isNumber(intensity) and intensity > 0:
			self.intensity = intensity
		else:
			raise IncorrectInput("The second argument must be a positive number")
