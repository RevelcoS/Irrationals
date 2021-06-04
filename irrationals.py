import math
from functools import reduce

class Error(ValueError):
    '''Base class for errors'''
    message = 'Error'
    def __str__(self):
        return self.message

class PerfectSquareError(Error):
    '''Raised when the irrational part is a perfect square'''
    message = 'The irrational part is a perfect square'

class ImaginaryPartError(Error):
    '''Raised when the irrational part is less than 0'''
    message = 'The irrational part is less than 0'

class NonIntegerError(Error):
    '''Raised when any input part is not an integer'''
    message = 'Non-integer value input'

class DifferentIrrationalPartError(Error):
    '''Raised when the irrational parts are different'''
    message = 'Different irrational parts'

class ZeroCoefficientError(Error):
    '''Raised when trying to convert irrational with coeff = 0 to ContFraction'''
    message = 'Zero coefficient of the irrational part'

class NonIrrationalError(Error):
    '''Raised when trying to convert non-irrational to ContFraction'''
    message = 'Non-irrational value input'

def is_integer(*args):
    for arg in args:
        if not isinstance(arg, int):
            raise NonIntegerError

class Irrational:
    '''The helper-class to construct irrationals'''
    def __init__(self, real:int, irr:tuple):
        '''
        Attributes:
            real -- the real part of the number
            irr -- the tuple (a, b) where a is the coeff of the irrational part b
        
        Example:
        Irrational(2, (-3, 3)) is the same as  2 - 3 * sqrt(3)

        Notice, that you can not work with numbers with
        different irrational parts (i.e. b is not changable).
        Also, irrational part can not be perfect square and must be
        greater than or equal to 0.
        '''

        self.real = real
        self.coeff, self.irr = irr

        is_integer(self.real, self.coeff, self.irr)

        if self.irr < 0:
            raise ImaginaryPartError
    
    def __add__(self, num):
        if type(num) == Irrational:
            is_different_irr(self, num)
            return Irrational(
                self.real + num.real,
                (
                    self.coeff + num.coeff, self.irr
                ))

        if type(num) == int:
            return Irrational(
                    self.real + num,
                    (
                        self.coeff, self.irr
                    ))
        
        if type(num) == Fraction:
            return num.__add__(self)

    def __radd__(self, num):
        return self.__add__(num)

    def __mul__(self, num):
        if type(num) == Irrational:
            is_different_irr(self, num)
            return Irrational(
                self.real * num.real + self.coeff * num.coeff * self.irr,
                (
                    self.real * num.coeff + self.coeff * num.real, self.irr
                ))

        if type(num) == int:
            return Irrational(
                    self.real * num,
                    (
                        self.coeff * num, self.irr
                    ))
        
        if type(num) == Fraction:
            return num.__mul__(self)
    
    def __rmul__(self, num):
        return self.__mul__(num)
    
    def __truediv__(self, num):
        if type(num) == int:
            return Fraction(self, num)
        
        if type(num) == Irrational:
            return Fraction(self) / num
        
        if type(num) == Fraction:
            return num.__rtruediv__(self)


    def __rtruediv__(self, num):
        return self.__truediv__(num).flip()
    
    def __floordiv__(self, num:int):
        return Irrational(
            self.real // num,
            (
                self.coeff // num, self.irr
            ))
    
    def __sub__(self, num):
        return self + -num
    
    def __rsub__(self, num):
        return -self.__sub__(num)
    
    def __neg__(self):
        return (-1) * self
    
    def __eq__(self, num):
        return self.real == num.real and self.coeff == num.coeff and self.irr == num.irr
    
    def __repr__(self):
        sq = math.sqrt(self.irr)
        if sq == int(sq):
            return str(int(self.value()))

        buffer = []
        if self.real != 0:
            buffer.append(str(self.real))
        if self.coeff != 0 and self.irr != 0:
            tmp = []
            coeff = self.coeff
            if buffer: coeff = abs(coeff)
            if coeff not in (-1, 1):
                tmp.append(str(coeff))
            
            s = []
            if not buffer and self.coeff == -1:
                s.append('-')
            s.append(f'sqrt({self.irr})')
            tmp.append(''.join(s))
            buffer.append(' * '.join(tmp))
        
        if self.coeff < 0:
            sep = ' - '
        else:
            sep = ' + '

        if buffer: return sep.join(buffer)
        return '0'
    
    def conj(self):
        return Irrational(
            self.real,
            (
                -self.coeff, self.irr
            ))
    
    def value(self):
        return self.real + self.coeff * math.sqrt(self.irr)

def is_different_irr(a:Irrational, b:Irrational):
    if a.irr != b.irr:
        raise DifferentIrrationalPartError


class Fraction:
    '''The helper-class to construct irrational fractions'''
    def __init__(self, num:Irrational, denom:int=1):
        '''
        Attributes:
            num -- Irrational numerator
            denom -- integer denominator
        
        Example:
        Fraction(Irrational(1, (2, 5)), 2) is the same as
        (1 + 2 * sqrt(5)) / 2
        '''

        self.num = num
        self.denom = denom

        is_integer(self.denom)
        if self.denom == 0:
            raise ZeroDivisionError

        self.simplify()
    
    def __add__(self, n):
        if type(n) == int:
            return Fraction(
                self.num + n * self.denom, self.denom
            )
        
        if type(n) == Irrational:
            n = Fraction(n)
        
        if type(n) == Fraction:
            return Fraction(
                self.num * n.denom + n.num * self.denom,
                self.denom * n.denom
            )

    
    def __radd__(self, n):
        return self.__add__(n)
    
    def __mul__(self, n):
        if type(n) == int:
            return Fraction(
                self.num * n, self.denom
            )
        
        if type(n) == Irrational:
            n = Fraction(n)
        
        if type(n) == Fraction:
            return Fraction(
                self.num * n.num, self.denom * n.denom
            )
    
    def __rmul__(self, n):
        return self.__mul__(n)
    
    def __truediv__(self, n):
        if type(n) == int:
            return Fraction(
                self.num, self.denom * n
            )
        
        if type(n) == Irrational:
            n = Fraction(n)
        
        if type(n) == Fraction:
            return self * n.flip()
    
    def __rtruediv__(self, n):
        return (self.__truediv__(n)).flip()
    
    def __sub__(self, n):
        return self.__add__(-n)
    
    def __rsub__(self, n):
        return -self.__sub__(n)
    
    def __neg__(self):
        return (-1) * self
    
    def __eq__(self, n):
        return self.num == n.num and self.denom == n.denom
    
    def __repr__(self):
        num, denom = self.num, self.denom
        try:
            num = int(str(num))
            integer = True
        except:
            integer = False

        if integer:
            g = math.gcd(num, denom)
            num //= g
            denom //= g    

        buffer = [str(num)]
        if denom != 1:
            buffer.append(str(denom))
        return ' / '.join(buffer)
    
    def flip(self):
        conj = self.num.conj()
        return Fraction(
            self.denom * conj, (self.num * conj).real
        )
    
    def simplify(self):
        g = reduce(
            lambda x, y: math.gcd(x, y),
            (self.num.real, self.num.coeff, self.denom))
        
        self.num //= g
        self.denom //= g

        if self.denom < 0:
            self.denom *= -1
            self.num *= -1
    
    def floor(self):
        return math.floor(self.num.value() / self.denom)


class ContFraction:
    def __init__(self, irr):
        '''
        Attributes:
            irr -- Fraction/Irrational number
        
        Converts irrational number to continued fraction of
        the form (a0, a1, ..., ak-1, (ak, ak+1, ..., an-1, an))
        where a0, ..., an are the elements of the continued fraction
        and ak, ..., an are the periodic elements.
        '''

        if type(irr) == Irrational:
            self.irr = Fraction(irr)
        elif type(irr) == Fraction:
            self.irr = irr
        else:
            raise NonIrrationalError

        irrational = self.irr.num
        if irrational.coeff == 0:
            raise ZeroCoefficientError

        sq = math.sqrt(irrational.irr)
        if sq == int(sq):
            raise PerfectSquareError

        self.main_lst, self.period_idx = self.expand()

    def expand(self):
        '''Calculates elements of the continued fraction'''
        alpha = self.irr
        a = alpha.floor()
        main_lst, alpha_lst = [a], [alpha]
        while True:
            new_alpha = (alpha - a).flip()
            new_a = new_alpha.floor()
            if new_alpha in alpha_lst and main_lst:
                idx = alpha_lst.index(new_alpha)
                break

            alpha_lst.append(new_alpha)
            main_lst.append(new_a)
            alpha, a = new_alpha, new_a

        return tuple(main_lst), idx

    def approximate(self, depth=100, is_fraction=False):
        '''Returns approximation of the continued fraction'''
        a, p = self.main_lst, self.period_idx
        p1, p2 = 1, a[0]
        q1, q2 = 0, 1
        for i in range(1, depth + 1):
            idx = p + (i - p) % (len(a) - p) if i >= p else i
            p1, p2 = p2, a[idx] * p2 + p1
            q1, q2 = q2, a[idx] * q2 + q1

        if is_fraction:
            return (p2, q2)
        return p2 / q2
    
    def __repr__(self):
        buffer = ['(']
        for i in range(len(self.main_lst)):
            if i == self.period_idx:
                buffer.append('(')
            
            buffer.append(str(self.main_lst[i]))

            if i != len(self.main_lst) - 1:
                buffer.append(', ')
        buffer.append('))')
        return ''.join(buffer)


def sqrt(n):
    '''Easy-to-create irrational number'''
    return Irrational(0, (1, n))