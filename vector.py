import math

class Vector():
    # Class for Vector
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)
        
        except ValueError:
            raise ValueError("The coordinates must not be empty")
        
        except TypeError:
            raise TypeError("The coordinates must be the iterable")


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)
    
    def __eq__(self, v):
        return self.coordinates == v.coordinates

    # Manipulations
    def plus(self, v):
        new_coordinates = [x+y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    def minus(self, v):
        new_coordinates = [x-y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    def times_scalar(self, c):
        new_coordinates = [c*x for x in self.coordinates]
        return Vector(new_coordinates)
    
    # Magnitude and Direction
    def magnitude(self, v=None):
        if v:
            coordinates_squared = [x**2 for x in v.coordinates]
        else:
            coordinates_squared = [x**2 for x in self.coordinates]
        
        return math.sqrt(sum(coordinates_squared))
    
    def normalized(self):
        try:
            return self.times_scalar(1/self.magnitude())
        except ZeroDivisionError:
            raise Exception("Could not normalize Zero vector")
    
    def dot_product(self, v):
        result = sum([x*y for x, y in zip(self.coordinates, v.coordinates)])
        return result
    
    def dot_product_find_teta(self, v, in_degree=False):
        teta = math.acos(self.dot_product(v)/(self.magnitude() * self.magnitude(v=v)))
        if in_degree:
            return teta * 180/math.pi
        else:
            return teta
        

if __name__ == '__main__':
   # Adding vectors 
   v = Vector([8.128, -9.341])
   w = Vector([-1.129, 2.111])
   print(v.plus(w))

   # Subtracting vectors
   v = Vector([7.119, 8.125])
   w = Vector([-8.223, 0.878])
   print(v.minus(w))

   # Scalar Multiplication
   v = Vector([1.671, -1.012, -0.318])
   c = 7.41
   print(v.times_scalar(c))

   # Find magnitude
   v = Vector([-0.221, 7.437])
   print(v.magnitude()) 

   v = Vector([8.813, -1.331, -6.247])
   print(v.magnitude())

   # Normalize
   v = Vector([5.581, -2.136])
   print(v.normalized())

   v = Vector([1.996, 3.108, -4.554])
   print(v.normalized())

   # Dot Product quiz running
   v = Vector([7.887, 4.138])
   w = Vector([-8.802, 6.776])
   print(v.dot_product(w))

   v = Vector([-5.955, -4.904, -1.874])
   w = Vector([-4.496, -8.755, 7.103])
   print(v.dot_product(w))

   # Find Teta in Radians and Degrees
   # In radians
   v = Vector([3.183, -7.627])
   w = Vector([-2.668, 5.319])
   print(v.dot_product_find_teta(w))
   # In degrees
   v = Vector([])
   w = Vector([])


