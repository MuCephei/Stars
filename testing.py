import ellipse
import coordinate
import math

a = coordinate.Coordinate()
b = coordinate.Coordinate(1,1)
z = coordinate.Coordinate(1,1,2)
c = coordinate.Coordinate(3,3)
d = coordinate.Coordinate(5,1,15)
e = coordinate.Coordinate(0,0,7)
f = coordinate.Coordinate(3,5)
g = coordinate.Coordinate(0,5,3)
h = coordinate.Coordinate(0,5,0)

# ellipseZ = ellipse.Ellipse(a,e,c,10)
# ellipseZ.plot3()

# ellipseA = ellipse.Ellipse(b,z,d,5)
# ellipseA.plot3()

ellipseB = ellipse.Ellipse(a,h,g,10)
ellipseB.plot3()

ellipseB = ellipse.Ellipse(a,b,f,5)
ellipseB.plot3()

ellipseB = ellipse.Ellipse(d,h,z,25)
ellipseB.plot3()

# ellipseC = ellipse.Ellipse(c,f,b,15)
# ellipseC.plot3()
# ellipseC.plot_2D()

# ellipseD = ellipse.Ellipse(c,g,b,5)
# ellipseD.plot3()
# ellipseD.plot_2D()

# ellipseE = ellipse.Ellipse(c,b,g,5)
# ellipseE.plot3()
# ellipseE.plot_2D()

# ellipseE = ellipse.Ellipse(b,c,g,5)
# ellipseE.plot3()
# ellipseE.plot_2D()