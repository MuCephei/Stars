import ellipse
import coordinate
import sphere
import is_num
import constants

class Orbit:

	#do something here and keep in mind that it is a two body system

	def __init__(self,body_one,body_two,barycenter,vector_normal,other_focus_one,other_focus_two,
		distance_one,distance_two,initial_angle_one,initial_angle_two):
		#sanitizing
		#I added the other_ to focus one and two so as to make it more clear that they are the 
		#non barycenter foci of the ellipses

		if isinstance(body_one,sphere.Sphere):
			self.body_one = body_one
		else:
			raise IncorrectInput("The first input must be a sphere")

		if isinstance(body_two,sphere.Sphere):
			self.body_two = body_two
		else:
			raise IncorrectInput("The second input must be a sphere")

		if isinstance(barycenter,coordinate.Coordinate):
			self.barycenter = barycenter
		else:
			raise IncorrectInput("The third input must be a Coordinate")

		if isinstance(vector_normal,vector.Vector):
			self.vector_normal = vector_normal
		else:
			raise IncorrectInput("The fourth input must be a Vector")

		if isinstance(other_focus_one,coordinate.Coordinate):
			self.other_focus_one = other_focus_one
		else:
			raise IncorrectInput("The fifth input must be a Coordinate")

		if isinstance(other_focus_two,coordinate.Coordinate):
			self.other_focus_two = other_focus_two
		else:
			raise IncorrectInput("The sixth input must be a Coordinate")

		#if the two focal points are not on the plane then there is an issue
		self.plane = coordinate.Plane(self.vector_normal,self.barycenter)
		if not self.plane.on_plane(self.other_focus_one):
			raise PointNotOnPlane("The fifth input must be on the plane described by the third and fourth inputs")
		if not self.plane.on_plane(self.other_focus_two):
			raise PointNotOnPlane("The sixth input must be on the plane described by the third and fourth inputs")

		if is_num.isNumber(distance_one):
			self.distance_one = float(distance_one)
		else:
			raise IncorrectInput("The seventh input must be a number")

		if is_num.isNumber(distance_two):
			self.distance_two = float(distance_two)
		else:
			raise IncorrectInput("The eigth input must be a number")

		if is_num.isNumber(initial_angle_one):
			self.initial_angle_one = float(initial_angle_one)
		else:
			raise IncorrectInput("The ninth input must be a number")

		if is_num.isNumber(initial_angle_two):
			self.initial_angle_two = float(initial_angle_two)
		else:
			raise IncorrectInput("The tenth input must be a number")

		self.ellipse_one = ellipse.Ellipse(self.other_focus_one,self.barycenter,
			self.vector_normal,self.distance_one)

		self.ellipse_two = ellipse.Ellipse(self.other_focus_two,self.barycenter,
			self.vector_normal,self.distance_one)

		self.reduced_mass = (self.body_one.mass * self.body_two.mass)/(self.body_one.mass + self.body_two.mass)

		self.initial_location_one = self.ellipse_one.get_location(0)
		self.initial_location_two = self.ellipse_two.get_location(0)

		self.initial_vector = self.initial_location_two - self.initial_location_one
		#this initial_vector is from body_two to body_one