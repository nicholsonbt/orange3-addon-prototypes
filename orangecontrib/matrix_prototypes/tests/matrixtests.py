import numpy as np

from orangecontrib.matrix_prototypes.matrix import Matrix, MatrixDomain, MatrixAxis




if __name__ == "__main__":
    x = MatrixAxis("x", ["X0", "X1", "X2"], dict())
    y = MatrixAxis("y", ["Y0", "Y1"], dict())
    z = MatrixAxis("z", ["Z0", "Z1", "Z2", "Z3"], dict())

    domain = MatrixDomain([x, y, z])

    data = np.array([
        [
            [ 1,  2,  3,  4],
            [ 5,  6,  7,  8],
        ],
        [
            [ 9, 10, 11, 12],
            [13, 14, 15, 16],
        ],
        [
            [17, 18, 19, 20],
            [21, 22, 23, 24],
        ],
    ])

    matrix = Matrix("Matrix", data, domain, dict())


    print(matrix)

    print("\n---------------\n")

    t = matrix.as_table("x")
    print(t)

    print("\n---------------\n")

    print(Matrix.from_table(t))
