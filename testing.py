#the testing values here are made up by me (eccept for the eccentricity which is from alhpa centauri)
#they have no meaning except for the fact that they given nice pictures

import coordinate
import math
import sphere
import matplotlib.pyplot as plt
import orbit
import constants

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

sphere_one = sphere.Star(10,100)
sphere_two = sphere.Star(1,1)
sphere_three = sphere.Star(1,1)

sphere_one.plot()
sphere_one.plot_with_obstruction(origin,a,c,sphere_two)
sphere_one.plot_with_obstruction(origin,a,g,sphere_two)

#the light arrays in the spheres have to be properly aligned
sphere_one.create_light_array(x)
sphere_two.create_light_array(x)

sphere_one.plot_with_obstruction(origin,e,f,sphere_two)

orbit_one = orbit.Orbit(sphere_two,sphere_three,b,(b-d).find_orthagonal(),b-d,-100000000000000,0.517)

orbit_one.plot_time(50)
orbit_one.plot()
#the plots are so the orbit can be compared with respect to time (plot_time) and purely angle (plot)

observation_point = ((b-d)*constants.AU * 100000000).coordinate()
#this finds an observation point along the main axis of the orbit

orbit_one.plot_raw_luminosity(observation_point)
#not very interessting

orbit_one.plot_raw_luminosity_angles(observation_point,1000,math.pi/-10000000,math.pi/10000000)
#this is a zoom in on the eclipising event so it is possible to see the limb darkening and path of the star in action
#interesstingly it seems that it is not perfectly centered on 0