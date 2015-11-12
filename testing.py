import ellipse2
import coordinate
import math

a = coordinate.Coordinate()
b = coordinate.Coordinate(1,1)
c = coordinate.Coordinate(3,3)
d = coordinate.Coordinate(5,10,15)
e = coordinate.Coordinate(0,0,7)
f = coordinate.Coordinate(3,5)
g = coordinate.Coordinate(5,3)
h = coordinate.Coordinate(10,10)

ellipseA = ellipse2.Ellipse(b,b,5)
ellipseA.plot_2D()

ellipseB = ellipse2.Ellipse(h,b,15)
ellipseB.plot_2D()