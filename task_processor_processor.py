
class Matrix:
    def __init__(self, matrix=()):
        self.matrix = matrix

    def __str__(self):
        return "\n".join(" ".join(str(value) for value in row) for row in self.matrix)

    def __add__(self, other):
        if len(self.matrix) != len(other.matrix):
            raise ValueError
        res = []
        for i in range(len(self.matrix)):
            row_res = []
            for j in range(len(self.matrix[0])):
                row_res.append(self.matrix[i][j] + other.matrix[i][j])
            res.append(row_res)
        return Matrix(res)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            res = [[self.matrix[i][j] * other for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))]
        elif isinstance(other, Matrix):
            res = []
            for i in range(len(self.matrix)):
                row_value = self.matrix[i]
                row_result = []
                for j in range(len(other.matrix[i])):
                    value_res = 0
                    for k in range(len(row_value)):
                        value_res += row_value[k] * other.matrix[k][j]
                    row_result.append(value_res)
                res.append(row_result)
        return Matrix(res)


    def _trans(self, c):
        res = []
        if c == '1':
            for row in range(len(self.matrix)):
                row_res = []
                for col in range(len(self.matrix[row])):
                    row_res.append(self.matrix[col][row])
                res.append(row_res)
        elif c == '2':
            for row in range(len(self.matrix)):
                row_res = []
                for col in range(len(self.matrix[row])):
                    row_res.append(self.matrix[-col-1][-row-1])
                res.append(row_res)
        elif c == '3':
            for row in range(len(self.matrix)):
                row_res = []
                for col in range(len(self.matrix[row])):
                    row_res.append(self.matrix[row][-col-1])
                res.append(row_res)
        elif c == '4':
            for row in range(len(self.matrix)):
                row_res = []
                for col in range(len(self.matrix[row])):
                    row_res.append(self.matrix[-row-1][col])
                res.append(row_res)
        return Matrix(res)


    def matrix_minor(self, matrix, row, col):
        return [row[:col] + row[col+1: ] for row in (matrix[:row] + matrix[row+1:])]


    def determinant_recursive(self, matrix, total=0):
        if len(matrix) != len(matrix[0]):
            raise ValueError
        if len(matrix) == 1:
            return matrix[0][0]
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        for c in range(len(matrix)):
            sign = (-1)**(c)
            total += sign * matrix[0][c] * self.determinant_recursive(self.matrix_minor(matrix, 0, c))
        return total

    def trans(self, m):
        res = []
        for row in range(len(m)):
            row_res = []
            for col in range(len(m[row])):
                row_res.append(m[col][row])
            res.append(row_res)
        return res

    def adjoint_matrix(self, m):
        if len(m) == 1:
            return 1
        res = []
        for r in range(len(m)):
            row_res = []
            for c in range(len(m)):
                tmp = self.matrix_minor(m, r, c)
                row_res.append(self.determinant_recursive(tmp) * (-1)**(r+c))
            res.append(row_res)
        return self.trans(res)


    def inverse(self, m):
        det = self.determinant_recursive(m)
        det_ = 1/det
        adj_m = self.adjoint_matrix(m)
        res = []
        for r in range(len(m)):
            row_res = []
            for c in range(len(m[0])):
                row_res.append(adj_m[r][c] * det_)
            res.append(row_res)
        return Matrix(res)

    @classmethod
    def num(cls, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    @classmethod
    def factory(cls, ordinal = ''):
        print(f"Enter size of {ordinal} matrix:")
        size = int(input()[0])
        print(f"Enter {ordinal} matrix:")
        return Matrix([[Matrix.num(i) for i in input().split()] for _ in range(size)])

    @classmethod
    def factory_trans(cls):
        print("Enter matrix size:")
        size = int(input()[0])
        print(f"Enter matrix:")
        return Matrix([[Matrix.num(i) for i in input().split()] for _ in range(size)])

def usr_input():
    print(f"""1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit""")
    s = input("Your choice: ")
    if s == "1" or s == "3":
        matrix_1 = Matrix.factory("first")
        matrix_2 = Matrix.factory("second")
        if s == "1":
            return matrix_1 + matrix_2
        else:
            return matrix_1 * matrix_2
    elif s == "2":
        matrix = Matrix.factory()
        c = Matrix.num(input("Enter constant: "))
        return matrix * c
    elif s == '4':
        print(f"""1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line""")
        c = input("Your choice: ")
        matrix = Matrix.factory_trans()
        return Matrix._trans(matrix, c)
    elif s == '5':
        print("Enter matrix size:")
        size = int(input()[0])
        print(f"Enter matrix:")
        matrix = [[Matrix.num(i) for i in input().split()] for _ in range(size)]
        a = Matrix()
        return a.determinant_recursive(matrix)
    elif s == '6':
        print("Enter matrix size:")
        size = int(input()[0])
        print(f"Enter matrix:")
        matrix = [[Matrix.num(i) for i in input().split()] for _ in range(size)]
        a = Matrix()
        return a.inverse(matrix)
    elif s == "0":
        return False
    return True

a = True
while True:
    try:
        a = usr_input()
        if not a:
            break
        print("The result is:", a, sep="\n")
    except (ValueError, TypeError, IndexError, AttributeError):
        print("The operation cannot be performed.")

