from .Matrix2D import *
from .Vector2D import *


def rotateAroundOrigin(vector: Vector2D, angle: float):
    mat = Matrix2D()
    mat.rotateAngle(angle)
    mat.transformVector2D(vector)


def ointToLocalSpace(point: Vector2D, agent) -> Vector2D:
    transPoint = point.copy()
    mat = Matrix2D()
    tx = -agent.getPos().Dot(agent.heading)
    ty = -agent.getPos().Dot(agent.side)
    mat.values[0][0] = agent.heading.x
    mat.values[0][1] = agent.side.x
    mat.values[1][0] = agent.heading.y
    mat.values[1][1] = agent.side.y
    mat.values[2][0] = tx
    mat.values[2][1] = ty
    mat.transformVector2D(transPoint)
    return transPoint
