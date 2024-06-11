class Matrix:
    def __init__(self, m, n, array):
        self.matrix = array
        self.m = m
        self.n = n

    def round_matrix(self):
        for i in range(self.m):
            for j in range(self.n):
                self.matrix[i][j] = round(self.matrix[i][j], 2)

    def copy_matrix(self):
        new = Matrix(self.m, self.n, [[0 for _ in range(self.n)] for _ in range(self.m)])
        for i in range(self.m):
            for j in range(self.n):
                new.matrix[i][j] = self.matrix[i][j]
        return new

    def __add__(self, other):
        if self.m != other.m or self.n != other.n:
            return None
        C = Matrix(self.m, self.n, [[]])
        C.matrix = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.n)] for i in range(self.m)]
        return C

    def __sub__(self, other):
        if self.m != other.m or self.n != other.n:
            return None
        C = Matrix(self.m, self.n, [[]])
        C.matrix = [[self.matrix[i][j] - other.matrix[i][j] for j in range(self.n)] for i in range(self.m)]
        return C

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            C = Matrix(self.m, self.n, [[]])
            C.matrix = [[self.matrix[i][j] * other for j in range(self.n)] for i in range(self.m)]
        elif type(other) is Matrix:
            if self.n != other.m:
                return None
            C = Matrix(self.m, other.n, [[0 for _ in range(other.n)] for _ in range(self.m)])
            for i in range(self.m):
                for j in range(other.n):
                    for k in range(self.n):
                        C.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
        return C

    def __str__(self):
        res = ""
        for row in self.matrix:
            for entry in row:
                res += str(entry) + " "
            res += "\n"
        return res

    def ERO_interchange(self, row1, row2):
        self.matrix[row1], self.matrix[row2] = self.matrix[row2], self.matrix[row1]

    def ERO_scalar_multiple(self, row, k):
        self.matrix[row] = [k * self.matrix[row][j] for j in range(self.n)]

    def ERO_add_multiple(self, src_row, des_row, k):
        self.matrix[des_row] = [self.matrix[des_row][j] + k * self.matrix[src_row][j] for j in range(self.n)]

    def Gauss_Jordan(self):
        lead = 0
        for r in range(self.m):
            if lead >= self.n:
                return
            i = r
            while self.matrix[i][lead] == 0:
                i += 1
                if i == self.m:
                    i = r
                    lead += 1
                    if self.n == lead:
                        return
            self.ERO_interchange(i, r)

            if self.matrix[r][lead] != 0:
                self.ERO_scalar_multiple(r, 1.0 / self.matrix[r][lead])
            for i in range(self.m):
                if i != r:
                    self.ERO_add_multiple(r, i, -self.matrix[i][lead])
            lead += 1

    def trace(self):
        if not self.is_square():
            return None
        tr = 0
        for i in range(self.m):
            tr += self.matrix[i][i]
        return tr

    def is_square(self):
        return self.m == self.n

    def is_diagonal(self):
        if not self.is_square():
            return False
        for i in range(self.m):
            for j in range(self.n):
                if i != j and self.matrix[i][j] != 0:
                    return False
        return True

    def is_upper(self):
        if not self.is_square():
            return False
        for i in range(self.m):
            for j in range(self.n):
                if i > j and self.matrix[i][j] != 0:
                    return False
        return True

    def is_lower(self):
        if not self.is_square():
            return False
        for i in range(self.m):
            for j in range(self.n):
                if i < j and self.matrix[i][j] != 0:
                    return False
        return True

    def identity(self):
        if self.is_square():
            for i in range(self.m):
                self.matrix[i] = [0 for _ in range(self.n)]
                self.matrix[i][i] = 1

    def transpose(self):
        B = Matrix(self.n, self.m, [[0 for _ in range(self.m)] for _ in range(self.n)])
        for i in range(self.m):
            for j in range(self.n):
                B.matrix[j][i] = self.matrix[i][j]
        return B

    def is_ref(self):
        row = 0
        column = 0
        while column < self.n and row < self.m:
            found_pivot = False
            for i in range(row, self.m):
                if self.matrix[i][column] != 0:
                    if found_pivot:
                        return False
                    found_pivot = True
            if found_pivot:
                row += 1
            column += 1
        return True

    def is_rref(self):
        row = 0
        column = 0
        while column < self.n and row < self.m:
            for j in range(column, self.n):
                if self.matrix[row][j] != 0:
                    if j < column:
                        return False
                    if self.matrix[row][j] != 1:
                        return False
                    for i in range(0, self.m):
                        if self.matrix[i][j] != 0 and i != row:
                            return False
                    row += 1
                    break
            column += 1
        return True

    def __pow__(self, power):
        pass

    def inverse(self):
        if self.is_square():
            B = Matrix(self.m, 2 * self.n, [])
            for r in range(self.m):
                B.matrix.append(self.matrix[r] + [int(i == r) for i in range(self.m)])
            B.Gauss_Jordan()
            if B.matrix[self.m - 1][self.m - 1] != 1:
                return None
            Inv = Matrix(self.m, self.n, [])
            for row in B.matrix:
                Inv.matrix.append(row[self.n:])
            return Inv
        return None

    def minor(self, i, j):
        return [row[:j] + row[j + 1:] for row in (self.matrix[:i] + self.matrix[i + 1:])]

    def determinant(self):
        if self.m != self.n:
            return None
        if self.m == 1:
            return self.matrix[0][0]
        elif self.m == 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
        else:
            det = 0
            for j in range(self.n):
                det += ((-1) ** j) * self.matrix[0][j] * Matrix(self.m - 1, self.n - 1, self.minor(0, j)).determinant()
            return det

    def adj(self):
        det = self.determinant()
        Inv = self.inverse()
        return Inv * det

    def rank(self):
        self.Gauss_Jordan()
        r = 0
        while r < self.m:
            is_zero = True
            for e in self.matrix[r]:
                if e != 0:
                    r += 1
                    is_zero = False
                    break
            if is_zero:
                break
        return r

    def nullity(self):
        r = self.rank()
        return self.n - r
