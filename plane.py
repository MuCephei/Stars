import vector

class Plane:
    #this may need to be adjusted

    def __init__(self,a,b,c):
    	#the equation fo a plane is apparently 
    	#ax + by + cz = d
    	#where one of a,b or c is not 0

    	#make sure that the imputs are Coordinates
    	if not isinstance(a,Coordinate):
    		a = Coordinate()
    	if not isinstance(b,Coordinate):
    		b = Coordinate()
    	if not isinstance(c,Coordinate):
    		c = Coordinate()
        if (a == b && b == c):
        	#we have a probleme here becuase someone thinks it's funny to 
        	#pass non coordinates to a plane
        	#or three identical points
        	raise ImproperInput("Houston we have a problem with three identical points being passed to a plane")

        self.vector_one = a - b
        self.vector_two = b - c
        if (self.vector_one == self.vector_two):
        	raise ImproperInput("Houston we have a problem with two identical vectors")
        cross_product = vector_one * vector_two
        coor = cross_product + Coordinate()
        #by the way im converting back and forth because im practicing hiding things
        #not because it is actually useful
        self.a = coor.getX()
        self.b = coor.getY()
        self.c = coor.getZ()
        self.d = self.a * a.getX() + self.b * a.getY() + self.c * a.getZ()
        #self.a is from the formula while a.getX() is the value of one of the input coordinates




