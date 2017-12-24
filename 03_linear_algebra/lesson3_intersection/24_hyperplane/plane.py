# -- coding: utf-8 --
from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Plane(object):
 
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 3

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Plane.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Plane.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    def __eq__(self, basic):
        return (self.dimension == basic.dimension) and (self.normal_vector == basic.normal_vector) and (self.constant_term == basic.constant_term)



    #功能：判断两平面是否平行
    #参数：
    #   [in]self : this plane
    #   [in]basic : another plane
    #返回值：
    #   True 平行；False 不平行
    def is_parallel(self, basic):
        return self.normal_vector.Is_Parallelism(basic.normal_vector)


    #功能：判断两平面是否相同
    #参数：
    #   [in]self : this plane
    #   [in]basic : another plane
    #返回值：
    #   True 相同；False 不同
    def is_sameplane(self, basic):
        if self.is_parallel(basic):
            n = self.basepoint.minus(basic.basepoint);
            if n.Is_Orthogonal(self.normal_vector):
                if n.Is_Orthogonal(basic.normal_vector):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

"""
normal_vector1 = Vector(['-0.412', '3.806', '0.728'])
constant_term1 = -3.46
normal_vector2 = Vector(['1.03', '-9.515', '-1.82'])
constant_term2 = 8.65
my_plane1 = Plane(normal_vector1, constant_term1)
my_plane2 = Plane(normal_vector2, constant_term2)
print "test1 is_parallel"
print my_plane1.is_parallel(my_plane2)
print "test1 is_sameplane"
print my_plane1.is_sameplane(my_plane2)


normal_vector3 = Vector(['2.611', '5.528', '0.283'])
constant_term3 = 4.6
normal_vector4 = Vector(['7.715', '8.306', '5.342'])
constant_term4 = 3.76
my_plane3 = Plane(normal_vector3, constant_term3)
my_plane4 = Plane(normal_vector4, constant_term4)
print "test2 is_parallel"
print my_plane3.is_parallel(my_plane4)
print "test2 is_sameplane"
print my_plane3.is_sameplane(my_plane4)

normal_vector5 = Vector(['-7.926', '8.625', '-7.212'])
constant_term5 = -7.952
normal_vector6 = Vector(['-2.642', '2.875', '-2.404'])
constant_term6 = -2.443
my_plane5 = Plane(normal_vector5, constant_term5)
my_plane6 = Plane(normal_vector6, constant_term6)
print "test3 is_parallel"
print my_plane5.is_parallel(my_plane6)
print "test3 is_sameplane"
print my_plane5.is_sameplane(my_plane6)
"""