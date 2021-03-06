import math
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector():
    # Class for Vector
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)
        
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
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)
    
    # Magnitude and Direction
    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return Decimal(math.sqrt(sum(coordinates_squared)))
    
    def normalized(self):
        try:
            return self.times_scalar(Decimal('1.0')/self.magnitude())
        except ZeroDivisionError:
            raise Exception("Could not normalize Zero vector")
    
    def dot_product(self, v):
        result = sum([x*y for x, y in zip(self.coordinates, v.coordinates)])
        return result
    
    def dot_product_find_teta(self, v, in_degrees=False):
        vector_dot_prod = self.dot_product(v)

        if self.magnitude() == 0 or v.magnitude() == 0:
            raise ZeroDivisionError('A zero vector has no angle')
        
        magnitude_dot_prod = self.magnitude() * v.magnitude()
        cos_angle = min(1, max(vector_dot_prod / magnitude_dot_prod, -1))
        
        teta = math.acos(cos_angle)
        if in_degrees:
            return teta * 180/math.pi
        else:
            return teta
    
    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot_product(v)) < tolerance
    
    def is_parallel_to(self, v):
        return (self.is_zero() or v.is_zero() or 
        self.dot_product_find_teta(v) == 0 or 
        self.dot_product_find_teta(v) == math.pi)
    
    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot_product(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == "Could not normalize Zero vector":
                raise Exception("No unique parallel component")
            else:
                raise e
    
    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == "No unique parallel component":
                raise Exception("No unique orthogonal component")
            else:
                raise e
    
    def cross(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [y_1*z_2 - y_2*z_1,
                               -(x_1*z_2 - x_2*z_1),
                               x_1*y_2 - x_2*y_1 ]
            return Vector(new_coordinates)

        except ValueError as e:
            msg = str(e)
            if msg == "need more than 2 values to unpack":
                self_embedded_R3 = Vector(self.coordinates + ('0',))
                v_embedded_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_R3.cross(v_embedded_R3)
            elif (msg == "too many values to unpack" or
                  msg == "need more than 1 value to unpack"):
                raise Exception("Only defined in two, three dimensions")
            else:
                raise e
    
    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v) / Decimal('2.0')
    
    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()
        

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
   v = Vector([7.35, 0.221, 5.188])
   w = Vector([2.751, 8.259, 3.985])
   print(v.dot_product_find_teta(w, in_degrees=True))

   # Find if vectors are parallel or orthogonal maybe both
   v = Vector([-7.579, -7.88])
   w = Vector([22.737, 23.64])
   print("Is orthogonal: ", v.is_orthogonal_to(w))
   print("Is parallel: ", v.is_parallel_to(w))
   
   v = Vector([-2.029, 9.97, 4.172])
   w = Vector([-9.231, -6.639, -7.245])
   print("Is orthogonal: ", v.is_orthogonal_to(w))
   print("Is parallel: ", v.is_parallel_to(w))

   v = Vector([-2.328, -7.284, -1.214])
   w = Vector([-1.821, 1.072, -2.94])
   print("Is orthogonal: ", v.is_orthogonal_to(w))
   print("Is parallel: ", v.is_parallel_to(w))

   # Component paralel / orthogonal
   v = Vector([3.039, 1.879])
   w = Vector([0.825, 2.036])
   print(v.component_parallel_to(w))

   # Cross product
   v = Vector([8.462, 7.893, -8.187])
   w = Vector([6.984, -5.975, 4.778])
   print(v.cross(w))

   v = Vector([-8.987, -9.838, 5.031])
   w = Vector([-4.268, -1.861, -8.866])
   print(v.area_of_parallelogram_with(w))

   v = Vector([1.5, 9.547, 3.691])
   w = Vector([-6.007, 0.124, 5.772])
   print(v.area_of_triangle_with(w)) 
