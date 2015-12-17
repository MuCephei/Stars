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
		self.averageDensity = self.volume/self.mass

	def flux(self,distance):
		return 0

	def get_2D_area(self):
		return self.area_2D

class Star(Sphere):
	#This is a sphere that we know one hell of a lot more about
	#mostly from it's mass


	def create_light_array(self,vector_prime):
		vector_prime = vector_prime.unitVector()
		vector_normal = vector_prime.find_orthagonal().unitVector()
		vector_aux = (vector_prime*vector_normal).unitVector()
		total_limb_luminosity = 0
		self.light_array = []

		for n in range(self.number_of_points):
			distance = random.uniform(0,1)
			theta = random.uniform(0,math.pi*2)
			a = math.sqrt(distance) * math.cos(theta)*self.radius
			b = math.sqrt(distance) * math.sin(theta)*self.radius
			f = math.sqrt(a**2+b**2)
			c = math.sqrt(self.radius**2-f**2)
			vector_one = a * vector_normal
			vector_two = b * vector_aux
			vector_three = c * vector_prime
			x = vector_one.getX() + vector_two.getX() + vector_three.getX()
			y = vector_one.getY() + vector_two.getY() + vector_three.getY()
			z = vector_one.getZ() + vector_two.getZ() + vector_three.getZ()
			vector = coordinate.Vector(x,y,z)

			angle_from_center = math.asin(f/self.radius)
			curr_luminosity = 2/5 + (3 * math.cos(angle_from_center)/5)
			total_limb_luminosity = total_limb_luminosity + curr_luminosity
			self.light_array.append(Point(vector,curr_luminosity))

		self.luminosity_coefficient = self.luminosity/total_limb_luminosity

	def __init__(self,radius,mass):
		self.luminosity = constants.solar_luminosity * (mass)**3.5
		Sphere.__init__(self,radius*constants.solar_radius,mass*constants.solar_mass)
		#I'm making a light array the consists of points, which each have a vector from the middle of the star
		base_vector = coordinate.Vector(0,0,1)

		total_limb_luminosity = 0

		self.number_of_points = 5000
		#don't make this number much bigger than 30000

		self.create_light_array(base_vector)

	def plot(self):

		x_values = []
		y_values = []
		z_values = []
		intensity_values = []

		for i in self.light_array:
			x_values.append(i.vector.getX())
			y_values.append(i.vector.getY())
			z_values.append(i.vector.getZ())
			intensity_values.append(i.intensity)

		size = 20

		fig = plt.figure(figsize = (7,13))
		xy = fig.add_subplot(311,aspect = 'equal',title = "X-Y Plane")
		yz = fig.add_subplot(312,aspect = 'equal',title = "Y-Z Plane")
		xz = fig.add_subplot(313,aspect = 'equal',title = "X-Z Plane")

		plt.gray()

		xy.scatter(x_values,y_values,c=intensity_values,s = size)
		xy.axis('equal')

		yz.scatter(y_values,z_values,c=intensity_values,s = size)
		yz.axis('equal')

		xz.scatter(x_values,z_values,c=intensity_values,s = size)
		xz.axis('equal')

		plt.show()

	def plot_with_obstruction(self,observation_point,center,center_prime,body):
		
		x_values = []
		y_values = []
		z_values = []
		intensity_values = []

		total_light = 0

		for i in self.light_array:
			distance = center_prime.shortest_path(observation_point,center + i.vector)
			if distance > body.radius:
				x_values.append(i.vector.getX()+center.getX())
				y_values.append(i.vector.getY()+center.getY())
				z_values.append(i.vector.getZ()+center.getZ())
				intensity_values.append(i.intensity)
				total_light = total_light + i.intensity
		total_light = total_light * self.luminosity_coefficient
		print("")
		print(total_light/self.luminosity)

		for i in body.light_array:
			x_values.append(i.vector.getX()+center_prime.getX())
			y_values.append(i.vector.getY()+center_prime.getY())
			z_values.append(i.vector.getZ()+center_prime.getZ())
			intensity_values.append(i.intensity)

		print((total_light+body.luminosity)/(self.luminosity + body.luminosity))
		print("")

		size = 20

		fig = plt.figure(figsize = (7,13))
		xy = fig.add_subplot(311,aspect = 'equal',title = "X-Y Plane")
		yz = fig.add_subplot(312,aspect = 'equal',title = "Y-Z Plane")
		xz = fig.add_subplot(313,aspect = 'equal',title = "X-Z Plane")

		plt.gray()

		xy.scatter(x_values,y_values,c=intensity_values,s = size)
		xy.axis('equal')

		yz.scatter(y_values,z_values,c=intensity_values,s = size)
		yz.axis('equal')

		xz.scatter(x_values,z_values,c=intensity_values,s = size)
		xz.axis('equal')

		plt.show()

	def intersection_star(self,observation_point,center,center_prime,radius_prime):
		#this returns true if one star is obscuring the other star's path
		#prime refers to the other star's center or radius
		distance_one = observation_point.distance(center)
		distance_two = observation_point.distance(center_prime)

		vector_one = observation_point - center_prime
		adjusted_vector = (distance_one/distance_two) * vector_one
		adjusted_center = observation_point + adjusted_vector

		adjusted_distance = adjusted_center.distance(center)

		result = adjusted_distance - self.radius - (radius_prime * distance_one/distance_two)
		# if result < 0:
		# 	print(result)
		return result < 0

	def total_light_obstruction(self,observation_point,center,center_prime,radius_prime):
		total_light = 0
		for i in self.light_array:
			#we need to know if we need to reject the point of light or not
			#to do this we find the shortest distance between a line made of two points and a third point
			distance = center_prime.shortest_path(observation_point,center + i.vector)
			if distance > radius_prime:
				total_light = total_light + i.intensity
		return total_light * self.luminosity_coefficient

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
