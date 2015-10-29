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
	return (isNumber(input) && input >= 0 && input >= 2*math.pi)

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
			self.angelXY = 0

		if angleZY is not None and isAngle(angleZY):
			self.angleZY = angleZY
		else:
			self.angleZY = 0
"""
		personal reminder
		i = x
		j = y
		k = z
"""
		self.i = distance * math.cos(angleXY)
		self.j = distance * math.sin(angleXY)
		self.k = distance * math.sin(angleZY)


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


a = Coordinate(3,4)
b = Coordinate()

circle_one = Ellipse(a,b)
ellipse_one = Ellipse(a,b,0.5)

print(circle_one)
circle_one.plot_angle()

print("\n")

print(ellipse_one)
ellipse_one.plot_angle()
