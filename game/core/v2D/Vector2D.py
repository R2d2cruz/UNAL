from math import atan2, pi, sqrt

EPSILON = 0.00001
PI_QUARTER = (2 * pi / 8)


class Vector2D:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return '<' + str(self.x) + ', ' + str(self.y) + '>'

    def __add__(self, vector):
        return Vector2D(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector):
        return Vector2D(self.x - vector.x, self.y - vector.y)

    def __mul__(self, scalar: float):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float):
        return Vector2D(self.x / scalar, self.y / scalar)

    def __isub__(self, vector):
        return self - vector

    def __iadd__(self, vector):
        return self + vector

    def __imul__(self, scalar):
        return self * scalar

    def __itruediv__(self, scalar):
        return self / scalar

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def length(self) -> float:
        return sqrt(self.x * self.x + self.y * self.y)

    def lengthSq(self) -> float:
        return self.x * self.x + self.y * self.y

    def setZero(self):
        self.x = 0.0
        self.y = 0.0

    def copy(self):
        return Vector2D(self.x, self.y)

    def isZero(self) -> bool:
        return self.x == 0.0 and self.y == 0.0

    def isGtEpsilon(self) -> bool:
        return self.lengthSq() > EPSILON

    def getCompass(self) -> int:
        arc = atan2(self.y, self.x)
        quad = round(arc / PI_QUARTER)
        return (quad + 8) % 8


def getVector2D(obj: object) -> Vector2D:
    return Vector2D(obj.x, obj.y)


def truncate(vector: Vector2D, maxLength: float) -> Vector2D:
    if vector.length() > maxLength:
        return normalize(vector) * maxLength
    return Vector2D(vector.x, vector.y)


def normalize(vector: Vector2D) -> Vector2D:
    lon = vector.length()
    if lon > EPSILON:
        return vector / lon
    return Vector2D(vector.x, vector.y)


def distanceSq(vectorA: Vector2D, vectorB: Vector2D) -> float:
    return (vectorB - vectorA).lengthSq()


def distance(vectorA: Vector2D, vectorB: Vector2D) -> float:
    return (vectorB - vectorA).length()