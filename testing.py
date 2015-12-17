import ellipse
import coordinate
import math
import sphere
import matplotlib.pyplot as plt
import random
import orbit
import constants

#This prints a bunch of fun ellipses

origin = coordinate.origin

a = coordinate.Coordinate(0,0,40000000000)
b = coordinate.Coordinate(17,-4,9)
c = coordinate.Coordinate(0,1000000000,10000000000)
d = coordinate.Coordinate(4,9,16)
e = coordinate.Coordinate(40000000000,0,0)
f = coordinate.Coordinate(10000000000,100000000,0)
g = coordinate.Coordinate(0,1100000000,10000000000)

x = origin - coordinate.Coordinate(1,0,0)
y = origin - coordinate.Coordinate(0,1,0) 
z = origin - coordinate.Coordinate(0,0,1)
other = origin - coordinate.Coordinate(1,1,1)

#def __init__(self,body_one,body_two,barycenter,vector_normal,vector_inline,relative_speed,orbital_distance,eccentricity):
sphere_one = sphere.Star(10,100)
sphere_two = sphere.Star(1,1)
sphere_three = sphere.Star(1,1)
sphere_one.plot()

sphere_one.plot_with_obstruction(origin,a,c,sphere_two)
sphere_one.plot_with_obstruction(origin,a,g,sphere_two)

sphere_one.create_light_array(x)
sphere_two.create_light_array(x)

sphere_one.plot_with_obstruction(origin,e,f,sphere_two)

orbit_one = orbit.Orbit(sphere_two,sphere_three,b,(b-d).find_orthagonal(),b-d,-100000000000000,0.5179)

orbit_one.plot_time(50)

observation_point = ((b-d)*constants.AU * 100000000).coordinate()

orbit_one.plot_raw_luminosity(observation_point)


