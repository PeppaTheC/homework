import math


class Quaternion:
    __slots__ = {'w',
                 'x',
                 'y',
                 'z',
                 }

    def __init__(self, w, x, y, z):
        self.w, self.x, self.y, self.z = w, x, y, z

    def __eq__(self, other):
        return self.w == other.w and self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not self.__eq__(other)

    def __abs__(self):
        return math.sqrt(self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z)

    def norm(self):
        return self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z

    def inverse(self):
        norm = self.norm()
        return Quaternion(self.w / norm, -self.x / norm, -self.y / norm, -self.z / norm)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            result = Quaternion(
                w=self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
                x=self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
                y=self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
                z=self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            )
        elif isinstance(other, (int, float)):
            result = Quaternion(
                w=other * self.w,
                x=other * self.x,
                y=other * self.y,
                z=other * self.z,
            )
        else:
            raise TypeError('Undefined object')
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        if isinstance(other, Quaternion):
            w, x, y, z = self.w, self.x, self.y, self.z
            self.w = w * other.w - x * other.x - y * other.y - z * other.z
            self.x = w * other.x + x * other.w + y * other.z - z * other.y
            self.y = w * other.y - x * other.z + y * other.w + z * other.x
            self.z = w * other.z + x * other.y - y * other.x + z * other.w
        elif isinstance(other, (int, float)):
            self.w *= other
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            raise TypeError('Undefined object')

    def __truediv__(self, other):
        if isinstance(other, Quaternion):
            norm = other.norm()
            result = Quaternion(
                w=(self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z) / norm,
                x=(-self.w * other.x + self.x * other.w - self.y * other.z + self.z * other.y) / norm,
                y=(-self.w * other.y + self.x * other.z + self.y * other.w - self.z * other.x) / norm,
                z=(-self.w * other.z - self.x * other.y + self.y * other.x + self.z * other.w) / norm,
            )
        elif isinstance(other, (int, float)):
            result = Quaternion(
                w=self.w / other,
                x=self.x / other,
                y=self.y / other,
                z=self.z / other,
            )
        else:
            raise TypeError('Undefined object')
        return result

    def __rtruediv__(self, other):
        if isinstance(other, Quaternion):
            result = self.__truediv__(other)
        elif isinstance(other, (int, float)):
            norm = self.norm()
            result = Quaternion(
                w=(other * self.w) / norm,
                x=(-other * self.x) / norm,
                y=(-other * self.y) / norm,
                z=(-other * self.z) / norm,
            )
        else:
            raise TypeError('Undefined object')
        return result

    def __idiv__(self, other):
        if isinstance(other, Quaternion):
            norm = other.norm()
            w, x, y, z = self.w, self.x, self.y, self.z
            self.w = (w * other.w + x * other.x + y * other.y + z * other.z) / norm
            self.x = (-w * other.x + x * other.w - y * other.z + z * other.y) / norm
            self.y = (-w * other.y + x * other.z + y * other.w - z * other.x) / norm
            self.z = (-w * other.z - x * other.y + y * other.x + z * other.w) / norm
        elif isinstance(other, (int, float)):
            self.w /= other
            self.x /= other
            self.y /= other
            self.z /= other
        else:
            raise TypeError('Undefined object')

    def __add__(self, other):
        if isinstance(other, Quaternion):
            result = Quaternion(
                w=self.w + other.w,
                x=self.x + other.x,
                y=self.y + other.y,
                z=self.z + other.z,
            )
        elif isinstance(other, (int, float)):
            result = Quaternion(
                w=self.w + other,
                x=self.x,
                y=self.y,
                z=self.z,
            )
        else:
            raise TypeError('Undefined object')
        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        if isinstance(other, Quaternion):
            self.w += other.w
            self.x += other.x
            self.y += other.y
            self.z += other.z
        elif isinstance(other, (int, float)):
            self.w += other
        else:
            raise TypeError('Undefined object')

    def __sub__(self, other):
        if isinstance(other, Quaternion):
            result = Quaternion(
                w=self.w - other.w,
                x=self.x - other.x,
                y=self.y - other.y,
                z=self.z - other.z,
            )
        elif isinstance(other, (int, float)):
            result = Quaternion(
                w=self.w - other,
                x=self.x,
                y=self.y,
                z=self.z,
            )
        else:
            raise TypeError('Undefined object')
        return result

    def __rsub__(self, other):
        if isinstance(other, Quaternion):
            result = self.__sub__(other)
        elif isinstance(other, (int, float)):
            result = Quaternion(
                w=other - self.w,
                x=-self.x,
                y=-self.y,
                z=-self.z,
            )
        else:
            raise TypeError('Undefined object')
        return result

    def __isub__(self, other):
        if isinstance(other, Quaternion):
            self.w -= other.w
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        elif isinstance(other, (int, float)):
            self.w = + other
        else:
            raise TypeError('Undefined object')

    def __str__(self):
        return f"{self.w} + {self.x}i + {self.y}j + {self.z}k"

    def __repr__(self):
        return f"Quaternion({self.w},{self.x},{self.y},{self.z})"


q, p = Quaternion(1, 2, 3, 4), Quaternion(17, 2, 3, 4)


def test_quaternion_add():
    assert q + p == Quaternion(q.w + p.w, q.x + p.x, q.y + p.y, q.z + p.z)

    for s in [-3, -2.3, -1.2, -1.0, 0.0, 0, 1.0, 1, 1.2, 2.3, 3]:
        assert (q + s == Quaternion(q.w + s, q.x, q.y, q.z))
        assert (s + q == Quaternion(q.w + s, q.x, q.y, q.z))


def test_quaternion_subtract():
    assert q - p == Quaternion(q.w - p.w, q.x - p.x, q.y - p.y, q.z - p.z)
    for s in [-3, -2.3, -1.2, -1.0, 0.0, 0, 1.0, 1, 1.2, 2.3, 3]:
        assert (q - s == Quaternion(q.w - s, q.x, q.y, q.z))
        assert (s - q == Quaternion(s - q.w, -q.x, -q.y, -q.z))


def test_quaternion_multiply():
    assert q * 1.0 == q
    assert q * 1 == q
    assert 1.0 * q == q
    assert 1 * q == q
    assert p * q == q * p
    assert p * q == Quaternion(-12, 36, 54, 72)
    for s in [-3, -2.3, -1.2, -1.0, 0.0, 0, 1.0, 1, 1.2, 2.3, 3]:
        assert q * s == Quaternion(s * q.w, s * q.x, s * q.y, s * q.z)
        assert s * q == q * s
    assert 0.0 * q == q * 0.0


def test_quaternion_divide():
    assert q / q == Quaternion(1, 0, 0, 0)
    assert 1 / q == q.inverse()
    assert 1.0 / q == q.inverse()
    assert 0.0 / q == Quaternion(0, 0, 0, 0)
    assert q / 1.0 == q
    assert q / 1 == q
    for s in [-3, -2.3, -1.2, -1.0, 1.0, 1, 1.2, 2.3, 3]:
        assert q / s == q * (1.0 / s)


if __name__ == '__main__':
    test_quaternion_add()
    test_quaternion_subtract()
    test_quaternion_multiply()
    test_quaternion_divide()
