import ellipse
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

ellipseA = ellipse.Ellipse(b,b,5)
ellipseA.plot_2D()

ellipseB = ellipse.Ellipse(b,h,15)
ellipseB.plot_2D()

ellipseC = ellipse.Ellipse(c,f,15)
ellipseC.plot_2D()

ellipseD = ellipse.Ellipse(c,g,5)
ellipseD.plot_2D()

ellipseE = ellipse.Ellipse(c,b,5)
ellipseE.plot_2D()

ellipseE = ellipse.Ellipse(b,c,5)
ellipseE.plot_2D()