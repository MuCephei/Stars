import vector
import ellipse

a = vector.Coordinate(3,4)
b = vector.Coordinate(10,-10)
#z-values don't quite work yet

circle_one = ellipse.Ellipse(a,b)
ellipse_one = ellipse.Ellipse(a,b,0.75)

print(circle_one)
#circle_one.plot_angle()
circle_one.plot_cross_section("Circle")
#is a circle, just doesn't look it

print("\n")

print(ellipse_one)
#ellipse_one.plot_angle()
ellipse_one.plot_cross_section("Ellipse")
#they always seem to look the same