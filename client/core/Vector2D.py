from math import sqrt, atan2, pi

EPSILON = 0.001
PI_QUARTER = (2 * pi / 8)


class Vector2D:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'

    def length(self) -> float:
        return sqrt(self.x * self.x + self.y * self.y)

    def lengthSq(self) -> float:
        return self.x * self.x + self.y * self.y

    def setZero(self):
        self.x = 0.0
        self.y = 0.0

    def isZero(self):
        return self.x == 0.0 and self.y == 0.0

    def isGtEpsilon(self):
        return self.lengthSq() > EPSILON

    def getCompass(self):
        arc = atan2(self.y, self.x)
        quad = round(arc / PI_QUARTER)
        return (quad + 8) % 8


def truncate(vector: Vector2D, maxLength: float) -> Vector2D:
    if vector.length() > maxLength:
        vector = normalize(vector)
    vector.x *= 3
    vector.y *= 3
    return vector


def normalize(vector: Vector2D) -> Vector2D:
    l = vector.length()
    if l > EPSILON:
        vector.x /= l
        vector.y /= l
    return vector
