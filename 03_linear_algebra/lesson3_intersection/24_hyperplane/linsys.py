# -- coding: utf-8 --
from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30

#参数化输出解集
class Parametrization(object):
    BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM_MSG = 'The basepoint and direction vectors should all live in the same dimention'

    def __init__(self, basepoint, direction_vectors):
        self.basepoint = basepoint
        self.direction_vectors = direction_vectors
        self.dimension = self.basepoint.dimension

        try:
            for v in direction_vectors:
                assert v.dimension == self.dimension
        except AssertionError:
            raise Exception(self.BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):\
        #保留几位小数
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

            if not MyDecimal(abs(coefficient) - 1).is_near_zero():
                output += '{}'.format(abs(coefficient))

            return output

        output = 'Parametrization Linear System:\n'
        first_nonzero_indexs = self.indices_of_first_nonzero_terms_in_each_row();

        for i in range(self.dimension):
            output += 'x_{} = '.format(i+1)
            if (not MyDecimal(self.basepoint[i]).is_near_zero()) or (first_nonzero_indexs[i] == -1):
                output += '{} '.format(round(self.basepoint[i], num_decimal_places))

            terms = [write_coefficient(direction_vector[i], is_initial_term=(j+1==first_nonzero_indexs[i])) + ' t_{}'.format(j+1)
                    for j, direction_vector in enumerate(self.direction_vectors) if round(direction_vector[i], num_decimal_places) != 0]
            output += ' '.join(terms)

            output += '\n'

        return output
    
    def indices_of_first_nonzero_terms_in_each_row(self):
        #num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_variables

        for i, base in enumerate(self.basepoint):
            if not MyDecimal(base).is_near_zero():
                indices[i] = 0

        for j, direction_vector in enumerate(self.direction_vectors):
            for i, tempvalue in enumerate(direction_vector):
                if (indices[i] == -1) and (not MyDecimal(tempvalue).is_near_zero()):
                    indices[i] = j+1

        return indices


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
        	#判断每个平面是否是同一维度
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def compute_solution(self):
        try:
            return self.do_gaussian_elimination_and_extract_solution()
        except Exception as e:
            if (str(e) == self.NO_SOLUTIONS_MSG):
                return str(e)
            else:
                raise e
    
    def do_gaussian_elimination_and_extract_solution(self):
        rref = self.compute_rref()

        rref.raise_exception_if_contradictory_equation()
        #rref.raise_exception_if_too_few_pivots()

        direction_vectors = rref.extract_direction_vectors_for_parametrization()
        basepoint = rref.extract_basepoint_for_parametrization()
        
        return  Parametrization(basepoint, direction_vectors)

    def extract_direction_vectors_for_parametrization(self):
        num_varaible = self.dimension
        first_nonzero_indexs = self.indices_of_first_nonzero_terms_in_each_row()
        free_variable_indices = set(range(num_varaible)) - set(first_nonzero_indexs)

        direction_vectors = []

        for free_variable in free_variable_indices:
            vector_coords = [0] * num_varaible
            vector_coords[free_variable] = 1
            for i,p in enumerate(self.planes):
                pivot_index = first_nonzero_indexs[i]
                if pivot_index < 0:
                    break
                vector_coords[pivot_index] = -p.normal_vector[free_variable]
            direction_vectors.append(Vector(vector_coords))
        
        return direction_vectors

    def extract_basepoint_for_parametrization(self):
        num_varaible = self.dimension
        first_nonzero_indexs = self.indices_of_first_nonzero_terms_in_each_row()
        
        basepoint = [0] * num_varaible

        for i,p in enumerate(self.planes):
            pivot_index = first_nonzero_indexs[i]
            if pivot_index < 0:
                break
            basepoint[pivot_index] = p.constant_term

        return Vector(basepoint)


    
    def raise_exception_if_contradictory_equation(self):
        for p in self.planes:
            try:
                p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    if not MyDecimal(p.constant_term).is_near_zero():
                        raise Exception(self.NO_SOLUTIONS_MSG)
                    else:
                        pass 
                        "0=0"
                else:
                    raise e

    def raise_exception_if_too_few_pivots(self):
        non_zero_indices = self.indices_of_first_nonzero_terms_in_each_row()
        num_pivots = sum([1 if index >= 0 else 0 for index in non_zero_indices])

        if num_pivots < self.dimension:

            raise Exception(self.INF_SOLUTIONS_MSG)



    def compute_rref(self):
        tf = self.compute_triangular_form()
        m = len(tf)
        none_zero_itme_in_each_row = tf.indices_of_first_nonzero_terms_in_each_row()

        for i in range(m)[::-1]:
            none_zero_item = none_zero_itme_in_each_row[i]
            if none_zero_item < 0:
                continue
            #首个非0项系数化为1
            c = tf[i].normal_vector[none_zero_item]
            tf.multiply_coefficient_and_row(Decimal(1)/c, i)
            #消去上方none_zero_item列的项
            tf.clear_allj_abovei(i, none_zero_item)

        return tf

    def clear_allj_abovei(self, i, j):
        #这里是值拷贝的意思，因为python默认传引用，而这里为了保存原始值。
        system = deepcopy(self)

        for row in range(i)[::-1]:
            c = self[row].normal_vector[j]
            self.add_multiple_times_row_to_row(-c, i, row)

    def compute_triangular_form(self):
        #这里是值拷贝的意思，因为python默认传引用，而这里为了保存原始值。
        system = deepcopy(self)

        m = len(self)
        n = self.dimension
        j = 0
        i = 0
        for i in range(m):
            while j<n:
                c = self[i].normal_vector[j]
                if MyDecimal(c).is_near_zero():
                    r = self.nonezero_coeff_under_i(i, j)
                    if r:
                        self.swap_rows(i, r)
                        break
                    else:
                        j += 1
                        continue
                else:
                    break

            if j<n:
                self.clear_allj_bllowi(i,j)
                j += 1

        return self


    def nonezero_coeff_under_i(self, i, j):
        row1 = i + 1
        row2 = j
        m = len(self)
        while row1<m:
            if self[row1].normal_vector[row2] != 0:
                return row1
            row1 += 1
        return 0

    def clear_allj_bllowi(self, i, j):
        row1 = i + 1
        m = len(self)
        while row1<m:
            c = self[row1].normal_vector[j]
            if not MyDecimal(c).is_near_zero():
                self.add_multiple_times_row_to_row(-c/self[i].normal_vector[j], i, row1)
            row1 += 1


    def swap_rows(self, row1, row2):
        #下面是我的写法：
        #tempplane = self[row1]
        #self[row1] = self[row2]
        #self[row2] = tempplane
        #更好的写法：
        self[row1], self[row2] = self[row2], self[row1]


    def multiply_coefficient_and_row(self, coefficient, row):
        n = self[row].normal_vector
        k = self[row].constant_term
        
        new_normal_vector = n.times_scalar(coefficient)
        new_constant_term = k * coefficient

        #注意：这里创建了新的plane对象，而不是直接修改当前plane的normal_vector和constant_term.
        #如果修改了现有的plane，则还需要重置该plane的基准点属性。
        self[row] = Plane(normal_vector=new_normal_vector, constant_term=new_constant_term)


    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        #下面是我写的
        #plus_normal_vector = self[row_to_add].normal_vector.times_scalar(coefficient)
        #plus_constant_term = self[row_to_add].constant_term * coefficient
        #self[row_to_be_added_to].normal_vector += plus_normal_vector
        #self[row_to_be_added_to].constant_term += plus_constant_term
        n1 = self[row_to_add].normal_vector
        n2 = self[row_to_be_added_to].normal_vector
        c1 = self[row_to_add].constant_term
        c2 = self[row_to_be_added_to].constant_term

        temp = n1.times_scalar(coefficient)
        new_normal_vector = n2.plus(temp)
        new_constant_term = c2 + c1*coefficient

        self[row_to_be_added_to] = Plane(normal_vector=new_normal_vector, constant_term=new_constant_term)


    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                #这里保证即便出现异常也能继续执行
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
