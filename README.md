# Stars
Project for stars about eclipsing binaries

The process starts with the creation of Stars
These objects have light array inside of them that are oriented in a direction
The arrays are halfspheres that represent the light that is visible from the angle of the halfsphere
The halfsphere or light array (same thing) must be re-oreiented everytime it is viewed from a different angle
They can be displayed by themselves or with another star obstruction the view, from an arbitrary observation point

These stars are then used to create an orbit, along with some other input data
The orbit module processes the input data and creates two ellipse objects
Each of these ellipse object are pure geometric objects and contain the ability to be ploted is various ways
They notable can determine the position in space given an angle

The orbit object then has the ability to determine the period and eccentricity of the ellipse objects, and can use that to find
the angle that the star is in at any given time during the orbit
The orbit object has the ability to plot the position of the stars with respect time, as well as the relative light that is seen
from an observer in arbirary space
Plotting the relative light can be done with respect to time or orbital angle

The testfile has been input with some reasonable data that produces an eclipsing event that has been zoomed in on with respect to angle
I would do it with respect to time but the resolution with respect to time is too low
