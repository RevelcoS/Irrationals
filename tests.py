import unittest, operator, math
from irrationals import ContFraction, Irrational, Fraction, sqrt
from irrationals import ImaginaryPartError, NonIntegerError, DifferentIrrationalPartError
from irrationals import PerfectSquareError, ZeroCoefficientError, NonIrrationalError


class TestIrrational(unittest.TestCase):
    def test_base(self):
        #1
        irr = sqrt(5)
        self.assertEqual(irr, Irrational(0, (1, 5)))

        #2
        irr = sqrt(3) + 2
        self.assertEqual(irr, Irrational(2, (1, 3)))

        #3
        irr = sqrt(7) - 7
        self.assertEqual(irr, Irrational(-7, (1, 7)))

        #4
        irr = 7 * sqrt(2) - 10
        self.assertEqual(irr, Irrational(-10, (7, 2)))

        #5
        irr = (6 * sqrt(99) + 7) / 13
        self.assertEqual(irr, Fraction(Irrational(7, (6, 99)), 13))

        #6
        irr = (30 * sqrt(5) + 120) / 105
        self.assertEqual(irr, Fraction(Irrational(8, (2, 5)), 7))

        #7
        irr = 105 / (30 * sqrt(5) + 120)
        self.assertEqual(irr, Fraction(Irrational(28, (-7, 5)), 22))

    def test_operators(self):
        ### Integers
        irr = 2 * sqrt(5) - 1

        #1
        expr = 2 * ((irr + 12) - 10)
        self.assertEqual(expr, Irrational(2, (4, 5)))

        #2
        expr = (36 * irr) / 72
        self.assertEqual(expr, Fraction(Irrational(-1, (2, 5)), 2))

        ### Irrational
        irr1, irr2 = 3 + 5 * sqrt(2), -6 - 3 * sqrt(2)

        #3
        self.assertEqual(irr1 + irr2, Irrational(-3, (2, 2)))

        #4
        self.assertEqual(irr1 - irr2, Irrational(9, (8, 2)))

        #5
        self.assertEqual(irr1 * irr2, Irrational(-48, (-39, 2)))

        #6
        self.assertEqual(irr1 / irr2, Fraction(Irrational(4, (-7, 2)), 6))

        ## Mixed
        irr1, irr2 = 1 - 5 * sqrt(2), (1 + 5 * sqrt(2)) / 2

        #7
        res = Fraction(Irrational(3, (-5, 2)), 2)
        self.assertEqual(irr1 + irr2, res)
        self.assertEqual(irr2 + irr1, res)

        #8
        res = Fraction(Irrational(-1, (15, 2)), 2)
        self.assertEqual(irr2 - irr1, res)
        self.assertEqual(irr1 - irr2, -res)

        #9
        res = Fraction(Irrational(-49, (0, 2)), 2)
        self.assertEqual(irr1 * irr2, res)
        self.assertEqual(irr2 * irr1, res)

        #10
        res = Fraction(Irrational(-102, (20, 2)), 49)
        self.assertEqual(irr1 / irr2, res)
        self.assertEqual(irr2 / irr1, res.flip())

        ## Fraction
        irr1, irr2 = (1 + 2 * sqrt(2)) / 3, (2 - 3 * sqrt(2)) / 2

        #11
        self.assertEqual(irr1 + irr2, Fraction(Irrational(8, (-5, 2)), 6))

        #12
        self.assertEqual(irr1 - irr2, Fraction(Irrational(-4, (13, 2)), 6))

        #13
        self.assertEqual(irr1 * irr2, Fraction(Irrational(-10, (1, 2)), 6))

        #14
        self.assertEqual(irr1 / irr2, Fraction(Irrational(-2, (-1, 2)), 3))

    def test_repr(self):
        ### Irrational
        #1
        irr = sqrt(5)
        self.assertEqual(str(irr), 'sqrt(5)')

        #2
        irr = -sqrt(5)
        self.assertEqual(str(irr), '-sqrt(5)')

        #3
        irr = sqrt(5) - 1
        self.assertEqual(str(irr), '-1 + sqrt(5)')

        #4
        irr = sqrt(5) + 1
        self.assertEqual(str(irr), '1 + sqrt(5)')

        #5
        irr = -sqrt(5) + 1
        self.assertEqual(str(irr), '1 - sqrt(5)')

        #6
        irr = -sqrt(5) - 1
        self.assertEqual(str(irr), '-1 - sqrt(5)')

        #7
        irr = 2 * sqrt(2) + 3
        self.assertEqual(str(irr), '3 + 2 * sqrt(2)')

        #8
        irr = -2 * sqrt(5) - 1
        self.assertEqual(str(irr), '-1 - 2 * sqrt(5)')

        #9
        irr = 2 * sqrt(5) + 1
        self.assertEqual(str(irr), '1 + 2 * sqrt(5)')

        #10
        irr = -2 * sqrt(5)
        self.assertEqual(str(irr), '-2 * sqrt(5)')

        #11
        irr = 0 * sqrt(5) - 1
        self.assertEqual(str(irr), '-1')

        #12
        irr = 2 * sqrt(0) + 1
        self.assertEqual(str(irr), '1')

        #13
        irr = 0 * sqrt(0) + 0
        self.assertEqual(str(irr), '0')

        #14
        irr = 8 - 2 * sqrt(16)
        self.assertEqual(str(irr), '0')

        ## Fraction
        #15
        irr = (sqrt(5) + 1) / 2
        self.assertEqual(str(irr), '1 + sqrt(5) / 2')

        #16
        irr = -2 * sqrt(5) / 4 
        self.assertEqual(str(irr), '-sqrt(5) / 2')

        #17
        irr = -sqrt(100) / -10
        self.assertEqual(str(irr), '1')

        #18
        irr = 0 * sqrt(2) / 3
        self.assertEqual(str(irr), '0')

        #19
        irr = 2 * sqrt(0) / 3
        self.assertEqual(str(irr), '0')

        #20
        irr = (-sqrt(4) + 1) / 2
        self.assertEqual(str(irr), '-1 / 2')

        #21
        irr = (2 * sqrt(5) + 2) / 2
        self.assertEqual(str(irr), '1 + sqrt(5)')

        #22
        irr = (45 + 15 * sqrt(5)) / 50
        self.assertEqual(str(irr), '9 + 3 * sqrt(5) / 10')
    
    def test_errors(self):
        # ImaginaryPartError
        self.assertRaises(ImaginaryPartError, sqrt, -1)

        # NonIntegerError
        self.assertRaises(NonIntegerError, sqrt, 2.2)
        self.assertRaises(NonIntegerError, Fraction, 1 + sqrt(2), 1.2)

        # DifferentIrrationalPartError
        for op in (operator.add, operator.mul, operator.sub, operator.truediv):
            self.assertRaises(DifferentIrrationalPartError, op, sqrt(5), sqrt(7))

class TestContFraction(unittest.TestCase):
    def test_base(self):
        #1
        cont_fraction = ContFraction(sqrt(2))
        self.assertEqual(str(cont_fraction), '(1, (2))')

        #2
        cont_fraction = ContFraction(sqrt(3))
        self.assertEqual(str(cont_fraction), '(1, (1, 2))')

        #3
        cont_fraction = ContFraction(sqrt(5))
        self.assertEqual(str(cont_fraction), '(2, (4))')

        #4
        cont_fraction = ContFraction(sqrt(29))
        self.assertEqual(str(cont_fraction), '(5, (2, 1, 1, 2, 10))')

        #5
        cont_fraction = ContFraction((sqrt(5) + 1) / 2)
        self.assertEqual(str(cont_fraction), '((1))')
    
    def test_approximation(self):
        # Decimal approximation
        self.assertEqual(str(ContFraction(sqrt(2)).approximate())[:10], str(math.sqrt(2))[:10])

        # Fraction approximation
        self.assertEqual(ContFraction(sqrt(29)).approximate(depth=7, is_fraction=True), (2251, 418))
    
    def test_errors(self):
        # PerfectSquareError
        self.assertRaises(PerfectSquareError, ContFraction, sqrt(4))

        # ZeroCoefficientError
        self.assertRaises(ZeroCoefficientError, ContFraction, Irrational(2, (0, 5)))

        # NonIrrationalError
        self.assertRaises(NonIrrationalError, ContFraction, 5)

if __name__ == '__main__':
    unittest.main()