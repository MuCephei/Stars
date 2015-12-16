import ellipse
import coordinate
import math
import sphere
import matplotlib.pyplot as plt
import random
import orbit
import constants

#This prints a bunch of fun ellipses

origin = coordinate.Coordinate()

def orthagonal(point_one,point_two):
	#takes two coordinates and returns a vector
	vector_one = point_one - point_two
	vector_two = point_one - origin
	return vector_one * vector_two

range_max = 100
range_min = -100

vectorZero = coordinate.Vector()

a = coordinate.Coordinate(3,4,5)
b = coordinate.Coordinate(17,-4,9)
c = coordinate.Coordinate(-1,-1,-1)
d = coordinate.Coordinate(4,9,16)

#def __init__(self,body_one,body_two,barycenter,vector_normal,vector_inline,relative_speed,orbital_distance,eccentricity):

sphere_one = sphere.Star(1.227,1.1)
sphere_two = sphere.Star(0.865,0.907)

orbit_one = orbit.Orbit(sphere_one,sphere_two,b,orthagonal(b,a),b-c,-3594,0.5179)

# orbit_one.plot()

orbit_one.plot_time()

#I'm looking to get a semi-major axis of 35.6 AU


