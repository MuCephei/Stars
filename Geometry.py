import vector
import ellipse

a = vector.Coordinate(3,8)
b = vector.Coordinate(3,8,10)
c = vector.Coordinate(4,8)
#z-values don't quite work yet

circle_one = ellipse.Ellipse(a,b)
ellipse_one = ellipse.Ellipse(a,b,0.5)

print(circle_one)
#circle_one.plot_angle()
circle_one.plot_cross_section("Circle")

print("\n")

print(ellipse_one)
#ellipse_one.plot_angle()
ellipse_one.plot_cross_section("Ellipse")

"""
I don't think that I am correctly addjusting the inclination based on the z axis
Even though im plotting based on the ellipse being flat, there still should be different values
even if the overall shape is still a circle

I considered adding in the option for an ellipse with a rotation compared to the default layout
Instead I think it will be better to tie the ellipse to it's own frame of reference

"""