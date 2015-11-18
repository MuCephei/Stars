import is_num
import math
import constants

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

#I'm going to get back to fleashing out Stars later, but right now I want to get orbits done

class Star(Sphere):
	#This is a sphere that we know one hell of a lot more about
	#mostly from it's mass

	def __init__(self,radius,mass):
		Sphere.__init__(self,radius,mass)

		# self.effective_temperature
		# self.luminosity

		#we could do a lot more here
		#and rise in increasing complexcity (I am not afraid to misspell things)
		#however all we need right now is the star's luminosity

	def flux(self,distance):
		if is_num.isNumber(distance):
			distance = float(distance)
		else:
			raise IncorrectInput("The first argument must be a number")

		return self.luminosity/(4*math.pi*distance)