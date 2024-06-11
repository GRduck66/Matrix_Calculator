import streamlit as st
import random as rd
from MatrixClass import *

menu = ['홈', '이항 연산', '단항 연산', '행렬의 정보', '기본 행 연산']
st.sidebar.header("행렬 계산기")
choice = st.sidebar.selectbox('메뉴', menu)
one_operator_default = ['Transpose', 'Scalar Multiple', 'Transpose Multiplication(ATA)']
one_operator_square = one_operator_default + ['Inverse', 'Adjoint', 'Power']
two_operator = ['Addition', 'Subtraction', 'Multiplication']
#st.sidebar.image("GRduck.png", caption="The ultimate being")

A = Matrix(0, 0, [[]])
B = Matrix(0, 0, [[]])
Res = Matrix(0, 0, [[]])

if 'rand' not in st.session_state:
    st.session_state.rand = 0
if 'ero_matrix' not in st.session_state:
    st.session_state.ero_matrix = A.copy_matrix()

def write_matrix(A):
    A.round_matrix()
    latex_matrix = "\\begin{bmatrix}"
    for row in A.matrix:
        latex_matrix += " & ".join(map(str, row)) + " \\\\ "
    latex_matrix += "\\end{bmatrix}"
    st.latex(latex_matrix)


def calc_two(A, B, operator):
    if operator == 'Addition':
        return A + B
    if operator == 'Subtraction':
        return A - B
    if operator == 'Multiplication':
        return A * B
    return None

def calc_one(A, operator, k):
    if operator == 'Transpose':
        return A.transpose()
    if operator == 'Scalar Multiple':
        return A * k
    if operator == 'Transpose Multiplication(ATA)':
        trans = A.transpose()
        return trans * A
    if operator == 'Inverse':
        return A.inverse()
    if operator == 'Adjoint':
        return A.adj()
    if operator == 'Power':
        return A ** k
    return None

def home():
    st.title("Welcome to Matrix Calculator!")
    st.subheader("[Mini Game]")
    luck_dict = {0:"^^ Press to start", 1:"Unlucky..", 2:"Sad..", 3:"Just normal", 4:"Pretty Good!", 5:"GOAT"}
    try_luck = st.button("PRESS!")
    if try_luck:
        st.session_state.rand = rd.randint(1, 5)
    st.subheader(luck_dict[st.session_state.rand])

def two_oper():
    st.title("이항 연산자 계산")
    st.write("[size of the matrix A]")
    with st.container(border=True):
        row1 = st.number_input('Number of rows: ', value=0, key="A_input_1")
        column1 = st.number_input('Number of columns: ', value=0, key="A_input_2")
        if row1 < 0 or column1 < 0:
            st.warning("Please enter a positive integer")
    A.m = row1
    A.n = column1
    A.matrix = [[0 for _ in range(column1)] for _ in range(row1)]
    st.write("[size of the matrix B]")
    with st.container(border=True):
        row2 = st.number_input('Number of rows: ', value=0, key="B_input_1")
        column2 = st.number_input('Number of columns: ', value=0, key="B_input_2")
        if row2 < 0 or column2 < 0:
            st.warning("Please enter a positive integer")
    B.m = row2
    B.n = column2
    B.matrix = [[0 for _ in range(column2)] for _ in range(row2)]

    if column1 > 0 and row1 > 0 and column2 > 0 and row2 > 0:
        st.write("Matrix A")
        with st.container(border=True):
            stcols1 = st.columns(column1)
            for i in range(row1):
                for j in range(column1):
                    with stcols1[j]:
                        A.matrix[i][j] = st.number_input("", value=0.0, key=f"A_{i}{j}")
        st.write("You've inputed: ")
        write_matrix(A)
        st.write("Matrix B")
        with st.container(border=True):
            stcols2 = st.columns(column2)
            for i in range(row2):
                for j in range(column2):
                    with stcols2[j]:
                        B.matrix[i][j] = st.number_input("", value=0.0, key=f"B_{i}{j}")
        st.write("You've inputed: ")
        write_matrix(B)

        st.write("Operator")
        with st.container(border=True):
            st.write("Wait a min")
            operator = st.selectbox('Select Operator: ', two_operator)
            calc_button = st.button('Get Result')

        if calc_button:
            Res = calc_two(A, B, operator)
            if Res is None:
                st.warning("The operation is not possible (Unsuitable sizes)")
            else:
                write_matrix(Res)

def one_oper():
    st.title("단항 연산자 계산")
    st.write("[size of the matrix]")
    with st.container(border=True):
        row = st.number_input('Number of rows: ', value=0)
        column = st.number_input('Number of columns: ', value=0)
        if row < 0 or column < 0:
            st.warning("Please enter a positive integer")
    A.m = row
    A.n = column
    A.matrix = [[0 for _ in range(column)] for _ in range(row)]

    if column > 0 and row > 0:
        st.write("Matrix A")
        with st.container(border=True):
            stcols = st.columns(column)
            for i in range(row):
                for j in range(column):
                    with stcols[j]:
                        A.matrix[i][j] = st.number_input("",value=0.0, key=f"A_{i}{j}")
        st.write("You've inputed: ")
        write_matrix(A)

        st.write("Operator")
        with st.container(border=True):
            k = 0
            if A.is_square():
                operations = one_operator_square
            else:
                operations = one_operator_default
            operator = st.selectbox('Select operator:', operations)
            if operator == 'Scalar Multiple':
                k = st.number_input("Enter scalar: ", value=0.0)
            if operator == 'Power':
                k = st.number_input("Enter power: ", value=0)
            calc_button = st.button('Get Result')

        if calc_button:
            Res = calc_one(A, operator, k)
            if type(Res) is None:
                st.warning("Irreversible Matrix")
            else:
                write_matrix(Res)


def matrix_info():
    st.title("행렬에 대한 모든 것!")
    st.write("[size of the matrix]")
    with st.container(border=True):
        row = st.number_input('Number of rows: ', value=0)
        column = st.number_input('Number of columns: ', value=0)
        if row < 0 or column < 0:
            st.warning("Please enter a positive integer")
    A.m = row
    A.n = column
    A.matrix = [[0 for _ in range(column)] for _ in range(row)]

    if column > 0 and row > 0:
        st.write("Matrix A")
        with st.container(border=True):
            stcols = st.columns(column)
            for i in range(row):
                for j in range(column):
                    with stcols[j]:
                        A.matrix[i][j] = st.number_input("", value=0.0, key=f"A_{i}{j}")
        st.write("You've inputed: ")
        write_matrix(A)

        st.write("Information")
        with st.container(border=True):
            if A.is_square():
                st.write(f"determinant: {A.determinant()}")
                st.write(f"trace: {A.trace()}")
            st.write(f"rank: {A.rank()}")
            st.write(f"nullity: {A.nullity()}")

def interchange(matrix, row1, row2):
    matrix.ERO_interchange(row1, row2)
    st.session_state.ero_matrix = matrix.copy_matrix()

def scale(matrix, row, k):
    matrix.ERO_scalar_multiple(row, k)
    st.session_state.ero_matrix = matrix.copy_matrix()

def compress(matrix, row, k):
    matrix.ERO_scalar_multiple(row, 1 / k)
    st.session_state.ero_matrix = matrix.copy_matrix()

def addScale(matrix, des, src, k):
    matrix.ERO_add_multiple(src, des, k)
    st.session_state.ero_matrix = matrix.copy_matrix()

def elem_row_oper():
    st.title("기본 행 연산")
    st.write("[size of the matrix]")
    with st.container(border=True):
        row = st.number_input('Number of rows: ', value=0)
        column = st.number_input('Number of columns: ', value=0)
        if row < 0 or column < 0:
            st.warning("Please enter a positive integer")
    B.m = row
    B.n = column
    B.matrix = [[0 for _ in range(column)] for _ in range(row)]

    A = st.session_state.ero_matrix.copy_matrix()

    if column > 0 and row > 0:
        st.write("Matrix A")
        with st.container(border=True):
            stcols = st.columns(column)
            for i in range(row):
                for j in range(column):
                    with stcols[j]:
                        B.matrix[i][j] = st.number_input("", value=0.0, key=f"A_{i}{j}")
            set_button = st.button("Apply")
            if set_button:
                A = B.copy_matrix()

        with st.container(border=True):
            EROINcol = st.columns(2)
            with EROINcol[0]:
                row1 = st.number_input("row1:", value=0, key="ERO_ROW1__")
            with EROINcol[1]:
                row2 = st.number_input("row2:", value=0, key="ERO_ROW2__")
            st.button("Interchange", on_click=interchange, args=(A, row1, row2))

            EROSCcol = st.columns(2)
            with EROSCcol[0]:
                row = st.number_input("row:", value=0, key="ERO_ROW_SCALE")
            with EROSCcol[1]:
                k1 = st.number_input("scalar:", value=0.0, key="ERO_SCALAR_1")
            st.button("Scalar multiple", on_click=scale, args=(A, row, k1))

            EROCPcol = st.columns(2)
            with EROCPcol[0]:
                row = st.number_input("row:", value=0, key="ERO_ROW_COMPRESS")
            with EROCPcol[1]:
                k1 = st.number_input("scalar:", value=0.0, key="ERO_SCALAR_1_DIV")
            st.button("Scalar divide", on_click=compress, args=(A, row, k1))

            EROAScol = st.columns(3)
            with EROAScol[0]:
                des_row = st.number_input("destination row:", value=0, key="ERO_DES_ROW")
            with EROAScol[1]:
                src_row = st.number_input("source row:", value=0, key="ERO_SRC_ROW")
            with EROAScol[2]:
                k2 = st.number_input("multiplier:", value=0.0, key="ERO_SCALAR_2")
            st.button("Add multiple", on_click=addScale, args=(A, des_row, src_row, k2))

            st.write("Current Matrix")
            write_matrix(A)
            if A.is_rref():
                st.success("You made a Row Reduced Echelon Form!")
                st.balloons()

if choice == '홈':
    home()
elif choice == '이항 연산':
    two_oper()
elif choice == '단항 연산':
    one_oper()
elif choice == '행렬의 정보':
    matrix_info()
elif choice == '기본 행 연산':
    elem_row_oper()
