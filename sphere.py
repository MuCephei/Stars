import is_num
import math
import constants
import coordinate

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
		base_vector = coordinate.Vector(1,0,0)

		light_array = []
		for i in range(int(radius)):
			#I am creating a plane at each instance to rotate the necessary vector around
			#the plane is normal to the arbitrary base_vector
			# has a point at length,0,0
			#where length is some away into the star
			length = math.sqrt(radius**2 - i ** 2)
			center = coordinate.Coordinate(length)
			plane = coordinate.Plane(base_vector,center)
			angle = math.asin(i/radius)
			luminosity_coefficient = 2/5 + (3 * math.cos(angle)/5)
			curr_luminosity = luminosity_coefficient * self.flux(radius)
			x = (int(radius)+1)**2
			for n in range(x):
				temp_vector = coordinate.Vector(n)
				theta = math.pi*2*n/x
				#note that theta is for rotating around the plane, not the angle from the interior of the star
				#the angle from the interior of the star is angle
				light_array.append(Point(plane.rotate(temp_vector,theta),curr_luminosity))

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
