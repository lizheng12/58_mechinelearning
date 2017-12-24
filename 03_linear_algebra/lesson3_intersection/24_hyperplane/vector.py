# -- coding: utf-8 --
from math import sqrt, acos, pi
#确保是Vector对象外面的数字被处理成小数，而不是浮点数或者整数
from decimal import Decimal, getcontext

getcontext().prec = 25

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector不能标准化零向量'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = '零向量没有唯一的平行向量'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = '零向量没有唯一的垂直向量'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = '仅定义了二维和三维空间中的叉积'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)
 #           self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "ZeroDivisionError"

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        if(self.dimension == v.dimension):
            for i in range(self.dimension):
                c = self.coordinates[i] - v.coordinates[i]
                if not MyDecimal(c).is_near_zero():
                    return False
            return True
        return False

    def __getitem__(self, item):
        return self.coordinates[item]

    #功能：加法
    #参数：
    #   [in]self 前操作数
    #   [in]v 后操作数
    #返回值：
    #   self和v相加的结果
    def plus(self, v):
        #列表推导式
        #new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        new_coordinates = []
        n = len(self.coordinates)
        for i in range(n):
            new_coordinates.append(self.coordinates[i] + v.coordinates[i])
        return Vector(new_coordinates)

    #功能：魔法方法加法+=
    #参数：
    #   [in]self 前操作数
    #   [in]v 后操作数
    #返回值：
    #   self和v相加的结果赋给self
    def __iadd__(self, v):
        self = self.plus(v)
        return self

    #功能：减法
    #参数：
    #   [in]self 前操作数
    #   [in]v 后操作数
    #返回值：
    #   self减v的结果
    def minus(self, v):
        #列表推导式
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    #功能：乘法
    #参数：
    #   [in]self 前操作数
    #   [in]c 后操作数
    #返回值：
    #   self和c相乘的结果
    def times_scalar(self, c):
        #列表推导式
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    #功能：求向量大小
    #参数：
    #   [in]self 向量
    #返回值：
    #   向量大小
    def magnitude(self):
        """我的方法
        magn = 0
        n = len(self.coordinates)
        for i in range(n):
            magn += self.coordinates[i]**2
        return math.sqrt(magn)
        """
        coordinates_squared = [x**Decimal(2) for x in self.coordinates]
        return sum(coordinates_squared).sqrt()
        """
        以前的错误写法：return sqrt(sum(coordinates_squared))
            这里是由于magnitude返回的值是float格式，
            而Decimal模块内置了一个计算开放的函数，
            为return sum(coordinates_squared).sqrt()
            这样写返回的值就是Decimal格式了。
        """

    #功能：求单位向量
    #参数：
    #   [in]self 向量
    #返回值：
    #   单位向量
    def normalized(self):
        """我写的
        magn = self.magnitude()
        new_coordinates = [x/magn for x in self.coordinates]
        return Vector(new_coordinates)
        """
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal(1.0)/magnitude)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
            else:
                raise e

    #功能：点积
    #参数：
    #   [in]self 前操作数
    #   [in]c 后操作数
    #返回值：
    #   点积结果值
    def dotproduct(self, c):
        return sum([x*y for x,y in zip(self.coordinates, c.coordinates)])


    #功能：向量之间的夹角
    #参数：
    #   [in]self 前操作数
    #   [in]c 后操作数
    #   [in]in_degrees 是否用角度表示（True 是; False 否;默认选项：False）
    #返回值：
    #   in_degrees为空或传入False时，返回夹角弧度值；
    #   in_degrees为True时，返回夹角角度值
    def angle(self, c, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = c.normalized()
            angle_in_radian = acos( u1.dotproduct(u2) )

            if in_degrees:
                return angle_in_radian / pi * 180.0
            else:
                return angle_in_radian

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
            else:
                raise e

#搞不懂这个，后面再说
#       except Exception as e:
#           if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
#               raise Exception('Cannot compute an angle with the zero vector')
#           else:
#               raise e


    #功能：判断两向量是否平行
    #参数：
    #   [in]self 前操作数
    #   [in]c 后操作数
    #返回值：
    #   True 平行; False 不平行
    def Is_Parallelism(self, c, tolerance=1e-10):
        print "[Is_Parallelism] begin"
        bool1 = self.magnitude() < tolerance
        bool2 = c.magnitude() < tolerance
        
        #两向量中有且只有一个向量是0向量(python的异或操作符没有找到)
        if ( (bool1 or bool2) and not(bool1 and bool2) ):
            print "[Is_Parallelism] end"
            return True

        #优达学城方法：
        #if ( ( self.angle(c) == 0 ) or ( self.angle(c) == pi ) ):
        #   print "[Is_Parallelism]angle end"
        #   return True

        #我的方法：两向量的单位向量的点积的绝对值是否等于1(点积的绝对值减1的绝对值是否小于一个很小的常量)
        if ( abs( abs(self.normalized().dotproduct( c.normalized() ) ) - Decimal(1) ) < tolerance ):
            print "[Is_Parallelism]dotproduct end"
            return True
        else:
            print "[Is_Parallelism] end"
            return False
        
    #功能：判断两向量是否互相垂直
    #参数：
    #   [in]self 前操作数
    #   [in]c 后操作数
    #返回值：
    #   True 垂直; False 不互相垂直
    def Is_Orthogonal(self, c, tolerance=1e-10):
        print "[Is_Orthogonal] begin"
        
        #两向量的点积等于0(绝对值小于一个很小的常量)
        if ( abs(self.dotproduct(c)) < tolerance ):
            print "[Is_Orthogonal] end"
            return True
        else:
            print "[Is_Orthogonal] end"
            return False


    #功能：计算该向量在另一向量上的平行分量
    #参数：
    #   [in]self 该向量
    #   [in]basic 另一向量
    #返回值：
    #   平行分量
    def component_parallel_to(self, basic):
        try:
            u = basic.normalized()
            return u.times_scalar(self.dotproduct(u))

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e


    #功能：计算该向量在另一向量上的垂直分量
    #参数：
    #   [in]self 该向量
    #   [in]basic 另一向量
    #返回值：
    #   垂直分量
    def component_orthogonal_to(self, basic):
        try:
            u = self.component_parallel_to(basic)
            return self.minus(u)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    #功能：计算两个三维向量的向量积（叉积）
    #参数：
    #   [in]self 该三维向量
    #   [in]basic 另一三维向量
    #返回值：
    #   向量积（叉积）结果
    def cross(self, basic):
        try:
            print "[cross] begin"
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = basic.coordinates
            new_coordinates = [y_1*z_2 - y_2*z_1,
                                z_1*x_2 - z_2*x_1,
                                x_1*y_2 - x_2*y_1]
            print "[cross] end"
            return Vector(new_coordinates)
        except Exception as e:
            if str(e) == "need more than 2 values to unpack":
                self_embeded_inR3 = Vector(self.coordinates + ('0',))
                basic_embeded_inR3 = Vector(basic.coordinates + ('0',))
                return self_embeded_inR3.cross(basic_embeded_inR3)
            elif(str(e) == "need more than 1 value to unpack" or
                str(e) == "too many values to unpack"
                ):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e


    #功能：计算两个三维向量所构成的平行四边形的面积
    #参数：
    #   [in]self 该三维向量
    #   [in]basic 另一三维向量
    #返回值：
    #   平行四边形面积
    def area_of_parallelogram_with(self, basic):
        cross_product = self.cross(basic)
        return cross_product.magnitude()


    #功能：计算两个三维向量所构成的三角形的面积
    #参数：
    #   [in]self 该三维向量
    #   [in]basic 另一三维向量
    #返回值：
    #   三角形面积
    def area_of_triangle_with(self, basic):
        return self.area_of_parallelogram_with(basic) / Decimal(2.0)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

"""
print "加plus:"
my_voctors1 = Vector([8.218,-9.341])
my_voctors2 = Vector([-1.129,2.111])
print my_voctors1.plus(my_voctors2)

print "\n减minus:"
my_voctors3 = Vector([7.119,8.215])
my_voctors4 = Vector([-8.223,0.878])
print my_voctors3.minus(my_voctors4)

print "\n缩放times_scalar:"
my_voctors5 = Vector([1.671,-1.012, -0.318])
print my_voctors5.times_scalar(7.41)

print "\n大小magnitude:"
my_voctors6 = Vector([-0.221,7.437])
my_voctors7 = Vector([8.813, -1.331, -6.247])
print my_voctors6.magnitude()
print my_voctors7.magnitude()

print "\n单位向量normalized:"
my_voctors8 = Vector([5.581, -2.136])
my_voctors9 = Vector([1.996, 3.108, -4.554])
print my_voctors8.normalized()
print my_voctors9.normalized()

print "\n点积1dotproduct:"
my_voctors10 = Vector([7.887, 4.138])
my_voctors11 = Vector([-8.802, 6.776])
print my_voctors10.dotproduct(my_voctors11)

print "\n点积2dotproduct:"
my_voctors12 = Vector([-5.955, -4.904, -1.874])
my_voctors13 = Vector([-4.496, -8.755, 7.103])
print my_voctors12.dotproduct(my_voctors13)

print "\n角度angle:"
my_voctors14 = Vector([3.183, -7.627])
my_voctors15 = Vector([-2.668, 5.319])
my_voctors16 = Vector([7.35, 0.221, 5.188])
my_voctors17 = Vector([2.751, 8.259, 3.985])
print my_voctors14.angle(my_voctors15)
print my_voctors16.angle(my_voctors17, True)

print "\n平行垂直1:"
my_voctors18 = Vector([-7.579, -7.88])
my_voctors19 = Vector([22.737, 23.64])
print my_voctors18.Is_Parallelism(my_voctors19)
print my_voctors18.Is_Orthogonal(my_voctors19)

print "\n平行垂直2:"
my_voctors20 = Vector([-2.029, 9.97, 4.172])
my_voctors21 = Vector([-9.231, -6.639, -7.245])
print my_voctors20.Is_Parallelism(my_voctors21)
print my_voctors20.Is_Orthogonal(my_voctors21)

print "\n平行垂直3:"
my_voctors22 = Vector([-2.328, -7.284, -1.214])
my_voctors23 = Vector([-1.821, 1.072, -2.94])
print my_voctors22.Is_Parallelism(my_voctors23)
print my_voctors22.Is_Orthogonal(my_voctors23)

print "\n平行垂直4:"
my_voctors24 = Vector([2.118, 4.827])
my_voctors25 = Vector([0, 0])
print my_voctors24.Is_Parallelism(my_voctors25)
print my_voctors24.Is_Orthogonal(my_voctors25)

print "\n向量投影1:"
my_voctors26 = Vector([3.039, 1.879])
my_voctors27 = Vector([0.825, 2.036])
print my_voctors26.component_parallel_to(my_voctors27)

print "\n向量投影2:"
my_voctors28 = Vector([-9.88, -3.264, -8.159])
my_voctors29 = Vector([-2.155, -9.353, -9.473])
print my_voctors28.component_orthogonal_to(my_voctors29)

print "\n向量投影3:"
my_voctors30 = Vector([3.009, -6.172, 3.692, -2.51])
my_voctors31 = Vector([6.404, -9.144, 2.759, 8.718])
print my_voctors30.component_parallel_to(my_voctors31)
print my_voctors30.component_orthogonal_to(my_voctors31)

print "\n叉积1:"
my_voctors32 = Vector([8.462, 7.893, -8.187])
my_voctors33 = Vector([6.984, -5.975, 4.778])
print my_voctors32.cross(my_voctors33)

print "\n平行四边形面积1:"
my_voctors34 = Vector([-8.987, -9.838, 5.031])
my_voctors35 = Vector([-4.268, -1.861, -8.866])
print my_voctors34.area_of_parallelogram_with(my_voctors35)

print "\n三角形面积1:"
my_voctors36 = Vector([1.5, 9.547, 3.691])
my_voctors37 = Vector([-6.007, 0.124, 5.772])
print my_voctors36.area_of_triangle_with(my_voctors37)

print "\n叉积error test:"
my_voctors38 = Vector([8.462,1.5])
my_voctors39 = Vector([6.984,1.5])
print my_voctors38.cross(my_voctors39)
"""