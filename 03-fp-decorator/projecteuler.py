from functools import reduce

# Problem9 (Special Pythagorean triplet)
# A Pythagorean triplet is a set of three natural numbers, a < b < c, for which, a^2 + b^2 = c^2
# There exists exactly one Pythagorean triplet for which a + b + c = 1000.
# Find the product abc.

SUM = 1000
# slow_product = [a * b * c for c in range(SUM) for b in range(c) for a in range(b)
#                 if (pow(a, 2) + pow(b, 2) == pow(c, 2)) and (a + b + c == SUM)]
# print(slow_product)

faster_product = [a * b * (SUM - a - b) for b in range(2, SUM - 3) for a in range(1, b)
                  if (pow(a, 2) + pow(b, 2) == pow(SUM - a - b, 2))]
print(faster_product)

# Problem6 (Sum square difference)
# The sum of the squares of the first ten natural numbers is, 1^2 + 2^2 + ... + 10^2 = 385
# The square of the sum of the first ten natural numbers is, (1 + 2 + ... + 10)^2 = 55^2 = 3025
# Hence the difference between the sum of the squares of the first ten natural numbers
# and the square of the sum is 3025 − 385 = 2640.
# Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.

NUMBERS = range(1, 101)
difference = pow(reduce(lambda x, y: x + y, NUMBERS), 2) - reduce(lambda x, y: x + y, [pow(i, 2) for i in NUMBERS])
print(difference)

# Problem48 (Self powers)
# The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.
# Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.

NUMBERS = range(1, 1001)
last_ten = reduce(lambda x, y: x + pow(y, y), [_ for _ in NUMBERS]) % (10 ** 10)
print(last_ten)

# Problem40 (Champernowne's constant)
# An irrational decimal fraction is created by concatenating the positive integers: 0.1 2 3 4 5 6 7 8 9 10 11...
# It can be seen that the 12th digit of the fractional part is 1..
# If dn represents the nth digit of the fractional part, find the value of the following expression.
# d1 × d10 × d100 × d1000 × d10000 × d100000 × d1000000

NUMBERS = range(1, 1000001)
slow_solution = reduce(lambda x, y: x * y, [int(ch) for count, ch in enumerate("".join([str(i) for i in NUMBERS]), 1)
                                            if count in [pow(10, i) for i in range(6)]])
print(slow_solution)
