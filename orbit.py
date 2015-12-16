import ellipse
import coordinate
import sphere
import is_num
import constants
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import newton

class Orbit:

	#do something here and keep in mind that it is a two body system

	def __init__(self,body_one,body_two,barycenter,vector_normal,vector_inline,specific_orbital_energy,eccentricity):
		#sanitizing
		
		if isinstance(body_one,sphere.Sphere):
			self.body_one = body_one
		else:
			raise IncorrectInput("The first input must be a sphere")

		if isinstance(body_two,sphere.Sphere):
			self.body_two = body_two
		else:
			raise IncorrectInput("The second input must be a sphere")

		if isinstance(barycenter,coordinate.Coordinate):
			self.barycenter = barycenter*constants.AU
		else:
			raise IncorrectInput("The third input must be a Coordinate")

		if isinstance(vector_normal,coordinate.Vector):
			self.vector_normal = vector_normal
		else:
			raise IncorrectInput("The fourth input must be a Vector")

		if isinstance(vector_inline,coordinate.Vector):
			self.vector_inline = vector_inline.unitVector()
			#this is a vector from the barycenter to the first focal point
			#the negative of this vector is from the barycenter to the second focal point
			#also this vector has no meaningfull magnitude
		else:
			raise IncorrectInput("The fifth input must be a Vector")

		if is_num.isNumber(specific_orbital_energy):
			self.specific_orbital_energy = float(specific_orbital_energy)
		else:
			raise IncorrectInput("The sixth input must be a number")

		if self.specific_orbital_energy >= 0:
			raise IncorrectInput("The inputs do not make a valid elliptical orbit.\nThe specific orbital energy must be less than 0")

		if is_num.isNumber(eccentricity):
			self.eccentricity = float(eccentricity)
		else:
			raise IncorrectInput("The seventh input must be a number")

		#some conviences
		self.mass_sum = body_one.mass + body_two.mass

		self.standard_gravitation_parameter = constants.G * self.mass_sum

		self.reduced_mass = (self.body_one.mass * self.body_two.mass)/self.mass_sum

		self.mass_ratio_one = self.body_one.mass / self.mass_sum

		self.mass_ratio_two = self.body_two.mass / self.mass_sum

		self.semimajor_sum = -1 * self.standard_gravitation_parameter / ( 2 * self.specific_orbital_energy)
		self.semimajor_sum = self.semimajor_sum * constants.AU

		self.semimajoraxis_one = self.semimajor_sum * self.mass_ratio_two

		self.semimajoraxis_two = self.semimajor_sum - self.semimajoraxis_one

		self.angular_momentum = self.reduced_mass * math.sqrt(
			constants.G * self.mass_sum * self.semimajor_sum * (1 - self.eccentricity **2))

		self.period = 2 * math.pi * math.sqrt(self.semimajor_sum**3/self.standard_gravitation_parameter)

		#focal_one is the second focal of the first ellipse
		#focal_two is the first focal of the second ellipse
		#Yes I know that that is kindof wierd
		distance_to_focal_one = 2 * self.semimajoraxis_one * self.eccentricity
		distance_to_focal_two = -2 * self.semimajoraxis_two * self.eccentricity
		#this one is negative becuase it is in the oppositve direction of the inlinevector

		self.focal_one = barycenter + (self.vector_inline * distance_to_focal_one)
		self.focal_two = barycenter + (self.vector_inline * distance_to_focal_two)

		self.ellipse_one = ellipse.Ellipse(self.barycenter,self.focal_one,self.vector_normal,2*self.semimajoraxis_one)
		self.ellipse_two = ellipse.Ellipse(self.barycenter,self.focal_two,self.vector_normal,2*self.semimajoraxis_two)

	def angle(self,t, Y):
		radius = self.semimajor_sum * (1 - self.eccentricity**2)/(1+self.eccentricity*math.cos(Y))
		dtheta = self.angular_momentum/(self.reduced_mass * radius ** 2)
		return dtheta

	def __str__(self):
		return self.ellipse_one.__str__() + self.ellipse_two.__str__()

	def get_relative_speed(self,distance):

		if not is_num.isNumber(distance):
			raise IncorrectInput("The first argument must be a number")

		return math.sqrt(2 * (self.specific_orbital_energy + (self.standard_gravitation_parameter / distance)))

	def find_angle(self,time):
		mean_anomaly = self.mean_anomaly(time)
		en = newton(self.eccentric_anomaly,math.pi,args=(mean_anomaly,))
		#en is the eccentric anomaly
		return self.true_anomaly(en)

	def eccentric_anomaly(self,ea,mean_anomaly):
		return mean_anomaly + self.eccentricity*math.cos(ea)-ea

	def mean_anomaly(self,time):
		#this is the angle that would be traveled in a period of time if it was a perfect circle
		return 2 * math.pi*time/self.period

	def true_anomaly(self,e):
		#this calcuates the true anomaly from an eccentric anomaly
		#in other words the angle the point would make from the center of the ellipse if it
		#was on a perfect circle
		#e = eccentric anomaly
		rhs = (math.cos(e) - self.eccentricity)/(1 - (self.eccentricity * math.cos(e)))
		result = math.acos(rhs)
		return result

	def plot_raw_luminosity(self):

		time = np.linspace(0,self.period*2,10000)
		angle = []
		for t in time:
			theta = self.find_angle(t)
			if (t%self.period) > (self.period/2):
				#the period gives odd results from ellipses that are not straight along the x axis

				theta = (2*math.pi)-theta
			angle.append(theta)

		coordinate_one = self.ellipse_one.get_coordinates(angle,time.size())

	def plot_time(self,points):

		vector = self.vector_normal*self.vector_inline
		plane = coordinate.Plane(vector,barycenter)

		time = np.linspace(0,self.period*2,points)
		angle = []
		for t in time:
			theta = self.find_angle(t)
			#to find out what quadrant this is in we need to take the determinant
			#first we need the point it would be at
			#we can do this for either ellipse
			location = self.ellipse_one.get_location(theta)
			if self.determinant(self.barycenter,self.focal_one,location) < 0:
				theta = (2*math.pi)-theta
			angle.append(theta)

		plt.plot(time,angle)
		plt.show()

		fig = plt.figure(figsize = (7,13))
		xy = fig.add_subplot(311,aspect = 'equal',title = "X-Y Plane")
		yz = fig.add_subplot(312,aspect = 'equal',title = "Y-Z Plane")
		xz = fig.add_subplot(313,aspect = 'equal',title = "X-Z Plane")

		self.ellipse_one.plot_specific_angles(xy,"x","y","green",angle,self.body_one.radius_in_AU())
		self.ellipse_one.plot_specific_angles(yz,"y","z","green",angle,self.body_one.radius_in_AU())
		self.ellipse_one.plot_specific_angles(xz,"x","z","green",angle,self.body_one.radius_in_AU())

		self.ellipse_two.plot_specific_angles(xy,"x","y","orange",angle,self.body_two.radius_in_AU())
		self.ellipse_two.plot_specific_angles(yz,"y","z","orange",angle,self.body_two.radius_in_AU())
		self.ellipse_two.plot_specific_angles(xz,"x","z","orange",angle,self.body_two.radius_in_AU())
		
		self.ellipse_one.plotCardinal(xy,"x","y")
		self.ellipse_one.plotCardinal(yz,"y","z")
		self.ellipse_one.plotCardinal(xz,"x","z")
		self.ellipse_two.plotCardinal(xy,"x","y")
		self.ellipse_two.plotCardinal(yz,"y","z")
		self.ellipse_two.plotCardinal(xz,"x","z")

		plt.show()

	def plot(self):
		#this just plots the ellipse
		fig = plt.figure()
		xy = fig.add_subplot(311,aspect = 'equal',title = "X-Y Plane")
		yz = fig.add_subplot(312,aspect = 'equal',title = "Y-Z Plane")
		xz = fig.add_subplot(313,aspect = 'equal',title = "X-Z Plane")

		self.ellipse_one.plot(xy,"x","y","green",self.body_one.radius_in_AU())
		self.ellipse_one.plot(yz,"y","z","green",self.body_one.radius_in_AU())
		self.ellipse_one.plot(xz,"x","z","green",self.body_one.radius_in_AU())
		self.ellipse_one.plotCardinal(xy,"x","y")
		self.ellipse_one.plotCardinal(yz,"y","z")
		self.ellipse_one.plotCardinal(xz,"x","z")

		self.ellipse_two.plot(xy,"x","y","orange",self.body_two.radius_in_AU())
		self.ellipse_two.plot(yz,"y","z","orange",self.body_two.radius_in_AU())
		self.ellipse_two.plot(xz,"x","z","orange",self.body_two.radius_in_AU())
		self.ellipse_two.plotCardinal(xy,"x","y")
		self.ellipse_two.plotCardinal(yz,"y","z")
		self.ellipse_two.plotCardinal(xz,"x","z")

		plt.show()