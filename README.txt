*** Continued fractions ***

Module irrationals.py is used to convert irrational numbers
to continued fractions and to approximate them. Notice,
that module converts only irrational numbers of the
quadratic equations, i.e. the irrational number must
be a root of some polinomial ax^2 + bx + c. Also, all
inputs must be integers.

You can create irrational number either with
'Fraction' / 'Irrational' class or with 'sqrt' function
(Notice, that 'sqrt' function is from irrationals.py module).
For example, (1 + 3 * sqrt(2)) / 2 is the same as
Fraction(Irrational(1, (3, 2)), 2). Also, you can do
addition, subtraction, multiplication and division with
irrational numbers.

Continued fraction of some irrational will be represented
as (a0, a1, ..., ak-1, (ak, ak+1, ..., an-1, an)) where
a0, ..., an are the elements of the continued fraction 
and ak, ..., an are the periodic elements.
For example, ContFraction(sqrt(29)) is (5, (2, 1, 1, 2, 10))
and ContFraction((sqrt(5) + 1) / 2) is ((1)).

To approximate irrational number use method 'approximate'
from 'ContFraction' class. The accuracy can be specified
with 'depth' param and fraction representation can be
specified with 'is_fraction' param. For example, 
ContFraction(sqrt(2)).approximate() will return 1.41421...

See https://en.wikipedia.org/wiki/Continued_fraction#Periodic_continued_fractions
for further information.