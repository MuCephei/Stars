import ellipse
import coordinate
import math

#This prints a bunch of fun ellipses

a = coordinate.Coordinate()
b = coordinate.Coordinate(1,1)
z = coordinate.Coordinate(1,1,2)
c = coordinate.Coordinate(3,3)
d = coordinate.Coordinate(5,1,15)
e = coordinate.Coordinate(0,0,7)
f = coordinate.Coordinate(3,5)
g = coordinate.Coordinate(0,5,3)
h = coordinate.Coordinate(0,5,0)

ellipseZ = ellipse.Ellipse(a,e,a-c,10)
ellipseZ.plot3()

ellipseA = ellipse.Ellipse(b,z,a-d,5)
ellipseA.plot3()

ellipseB = ellipse.Ellipse(a,h,a-g,10)
ellipseB.plot3()

ellipseB = ellipse.Ellipse(a,b,a-f,5)
ellipseB.plot3()

ellipseB = ellipse.Ellipse(d,h,a-z,25)
ellipseB.plot3()

ellipseC = ellipse.Ellipse(c,f,a-b,15)
ellipseC.plot3()

ellipseD = ellipse.Ellipse(c,g,a-b,5)
ellipseD.plot3()

ellipseE = ellipse.Ellipse(c,b,a-g,5)
ellipseE.plot3()

ellipseE = ellipse.Ellipse(b,c,a-g,5)
ellipseE.plot3()