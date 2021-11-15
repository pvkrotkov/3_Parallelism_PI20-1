from multiprocessing import Process, Pool
import csv
from random import *

'''
Программа будет генерировать случайную матрицу размера, заданного пользователем, а затем создавать файлы для matrix1, matrix2 и результата
'''

#Функция для генерации матрицы и записи ее в файл
def gen_matrix(n, name):
    res = [sample([x for x in range(1,100)], n) for _ in range(n)]

    with open(name, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        for row in res:
            writer.writerow(row)

    print(res)

#Функция умножения матрицы
def multiply(args):
    i, j, = args[0] 
    A, B = args[1:] 
    res = 0

    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    
    return res

#Функция, чтобы принимать ввод от пользователя и избегать отрицательного ввода и строк
def take_input_length():
    flag = False
    while flag == False:
        try:
            inpt = int(input('Введите длину вашей матрицы: \nВведите "0", чтобы остановить программу!\n'))
        except:
            print('Неправильный ввод')
        else:
            if inpt>=0:
                flag = True
            else:
                print('Введите число больше 0!')
    return inpt

#Функция, которая получает имя файла и возвращает матрицу из этого файла
def open_matrix(name):
    with open(name, 'r') as f:
        file = csv.reader(f, delimiter=';')
        res = [ list(map(int, row)) for row in file]
    return res

def write_result(name, matrix):
    with open(name, 'w') as f:
        file = csv.writer(f, delimiter=';')
        for row in matrix:
            file.writerow(row)

def main():
    
    while True:
        #взять длину матрицы от пользователя
        length = take_input_length()
        if length==0:
            break

        #создать две матрицы
        gen_matrix(length, 'matrix1.csv')
        gen_matrix(length, 'matrix2.csv')

        #открыть две матрицы
        matrix1 = open_matrix('matrix1.csv')
        matrix2 = open_matrix('matrix2.csv')

        #определить количество прецессов по длине матрицы
        proc_amount = Pool(processes=len(matrix1[0])*len(matrix2))

        #помещаем все числа в матрицу в один столбец чисел
        elements = [((i,j), matrix1, matrix2) for i in range(len(matrix1[0])) for j in range(len(matrix2))]

        #умножение элементов
        result = proc_amount.map(multiply, elements)

        #возвращение одного столбца в матрицу
        result_matrix = [result[i:i+len(matrix2)] for i in range(0, len(matrix1[0])*len(matrix2), len(matrix2))]

        print(result_matrix)

        #записываем матрицу результатов в отдельный файл
        write_result('result_matrix.csv', result_matrix)


if __name__ == '__main__':
    main()
