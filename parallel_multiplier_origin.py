from multiprocessing import  Queue, cpu_count#Manager, Queue#Process, Pool,
from multiprocessing.pool import ThreadPool
import csv

f1_fin = []
f2_fin = []

AB_table = []
AB_table.append(f1_fin)
AB_table.append(f2_fin)

def nums_from_file(file_Name1, file_Name2):
    global f1_fin, f2_fin
    file = open(file_Name1 + '.txt')
    content = file.readlines()
    file.close()

    for i in content:
        tempLs = []
        temp = i.replace("\n", "").split(";")
        for j in temp:
            tempLs.append(int(j))
        f1_fin.append(tempLs)
    N = len(f1_fin)

    file = open(file_Name2 + '.txt')
    content = file.readlines()
    file.close()

    for i in content:
        tempLs = []
        temp = i.replace("\n", "").split(";")
        for j in temp:
            if j != "*":
                tempLs.append(int(j))
        f2_fin.append(tempLs)
    N = len(f2_fin)

def elements_Multiple_result(index, A, B):
    i, j = index
    res = 0
    N = len(A[0])
    for k in range(N):
        res += A[i][k] * B[k][j]
    return (res)

def operation(que, m_cpu, num, que_b=False):
    if finish:
        if que_b:
            print(que_b)
            que = que.get()
        matrix1 = que[0]
        matrix2 = que[1]
        d1 = len(matrix1)
        d2 = len(matrix2[0])
        matric_otv = []
        pool = ThreadPool(processes=min(max(2, d1 * d2 - 1), m_cpu))
        for i in range(d1):
            matric_otv.append([])
            for k in range(d2):
                p1 = pool.apply_async(elements_Multiple_result, ((i, k), matrix1, matrix2))
                matric_otv[i].append(p1.get())
        return matric_otv
while True:

    try:
        ask = input('Введите через пробел названия текстовых файлов в которых содержаться матрицы: (принимаются только названия. Расширание писать не нужно)\n').split(' ')

        nums_from_file(ask[0], ask[1])

        print(f'Получены две матрицы: {str(f1_fin)} и {str(f2_fin)}\n')

        finish = False
        pros = []
        m_cpu = cpu_count()

        finish = True
        final_res = operation(AB_table, m_cpu, 'From table', False)
        finish = True
        print('\033[32m\033[5mРезультат умеожения: \033[0m')
        for i in range(len(final_res)):
            print(final_res[i])
    except FileNotFoundError:
        print('\033[31m\033[7mОдного из файлов в директории нет\033[0m')
