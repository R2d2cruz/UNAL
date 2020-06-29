import math

from .Vector2D import Vector2D


class Matrix2D:
    def __init__(self):
        self.values = [[0.0] * 3, [0.0] * 3, [0.0] * 3, ]
        self.identity()

    def identity(self):
        for row in range(3):
            for col in range(3):
                self.values[row][col] = 1.0 if row == col else 0.0

    def multiply(self, matrix):
        temp = [[0.0] * 3, [0.0] * 3, [0.0] * 3, ]
        temp[0][0] = (self.values[0][0] * matrix.values[0][0]) + \
                            (self.values[0][1] * matrix.values[1][0]) + \
                            (self.values[0][2] * matrix.values[2][0])
        temp[0][1] = (self.values[0][0] * matrix.values[0][1]) + \
                            (self.values[0][1] * matrix.values[1][1]) + \
                            (self.values[0][2] * matrix.values[2][1])
        temp[0][2] = (self.values[0][0] * matrix.values[0][2]) + \
                            (self.values[0][1] * matrix.values[1][2]) + \
                            (self.values[0][2] * matrix.values[2][2])
        temp[1][0] = (self.values[1][0] * matrix.values[0][0]) + \
                            (self.values[1][1] * matrix.values[1][0]) + \
                            (self.values[1][2] * matrix.values[2][0])
        temp[1][1] = (self.values[1][0] * matrix.values[0][1]) + \
                            (self.values[1][1] * matrix.values[1][1]) + \
                            (self.values[1][2] * matrix.values[2][1])
        temp[1][2] = (self.values[1][0] * matrix.values[0][2]) + \
                            (self.values[1][1] * matrix.values[1][2]) + \
                            (self.values[1][2] * matrix.values[2][2])
        temp[2][0] = (self.values[2][0] * matrix.values[0][0]) + \
                            (self.values[2][1] * matrix.values[1][0]) + \
                            (self.values[2][2] * matrix.values[2][0])
        temp[2][1] = (self.values[2][0] * matrix.values[0][1]) + \
                            (self.values[2][1] * matrix.values[1][1]) + \
                            (self.values[2][2] * matrix.values[2][1])
        temp[2][2] = (self.values[2][0] * matrix.values[0][2]) + \
                            (self.values[2][1] * matrix.values[1][2]) + \
                            (self.values[2][2] * matrix.values[2][2])
        self.values = temp

    def rotateAngle(self, angle: float):
        mat = Matrix2D()
        sin = math.sin(angle)
        cos = math.cos(angle)
        mat.values[0] = [cos, sin, 0]
        mat.values[1] = [-sin, cos, 0]
        mat.values[2] = [0, 0, 1]
        self.multiply(mat)

    def rotateVector(self, vector: Vector2D, side: Vector2D):
        mat = Matrix2D()
        mat.values = [
            [vector.x, vector.y, 0],
            [side.x, side.y, 0],
            [0, 0, 1]]
        self.multiply(mat)

    def transformVector2D(self, vector: Vector2D):
        tempX = (self.values[0][0] * vector.x) + (self.values[1][0] * vector.y) + (self.values[2][0])
        tempY = (self.values[0][1] * vector.x) + (self.values[1][1] * vector.y) + (self.values[2][1])
        vector.x = tempX
        vector.y = tempY


"""




//applies a v2D transformation matrix to a single Vector2D
inline void C2DMatrix::TransformVector2Ds(Vector2D &vPoint)
{

  double tempX =(m_Matrix[0][0]*vPoint.x) + (m_Matrix[1][0]*vPoint.y) + (m_Matrix[2][0]);

  double tempY = (m_Matrix[0][1]*vPoint.x) + (m_Matrix[1][1]*vPoint.y) + (m_Matrix[2][1]);
  
  vPoint.x = tempX;

  vPoint.y = tempY;
}




//create a transformation matrix
inline void C2DMatrix::Translate(double x, double y)
{
  Matrix mat;
  
  mat[0][0] = 1; mat[0][1] = 0; mat[0][2] = 0;
  
  mat[1][0] = 0; mat[1][1] = 1; mat[1][2] = 0;
  
  mat[2][0] = x;    mat[2][1] = y;    mat[2][2] = 1;
  
  //and multiply
  MatrixMultiply(mat);
}

//create a scale matrix
inline void C2DMatrix::Scale(double xScale, double yScale)
{
  C2DMatrix::Matrix mat;
  
  mat[0][0] = xScale; mat[0][1] = 0; mat[0][2] = 0;
  
  mat[1][0] = 0; mat[1][1] = yScale; mat[1][2] = 0;
  
  mat[2][0] = 0; mat[2][1] = 0; mat[2][2] = 1;
  
  //and multiply
  MatrixMultiply(mat);
}
"""
