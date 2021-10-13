import multiprocessing
import random


def generate_matrix(n, m):
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(m):
            matrix[i].append(random.randint(1, 100))
    return matrix


def read_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        m = [[0 for _ in range(len(lines))] for _ in range(len(lines[0].split()))]
        for i, line in enumerate(lines):
            for j in range(len(line.split())):
                m[i][j] = line.split()[j]
    return m


def write_to_file(A, filename, pr=False):
    with open(filename, 'w') as f:
        for line in A:
            f.write(' '.join([str(elem) for elem in line])+'\n')
            if pr:
                print(' '.join([str(elem) for elem in line]))


def element(index, A, B, q):
    i, j = index
    res = sum([A[i][k] * B[k][i] for k in range(len(A) or len(B))])
    d = {
        'res': res,
        'i': i,
        'j': j
    }
    q.put(d)


q = multiprocessing.Manager().Queue()

matrix1 = generate_matrix(20, 20)
matrix2 = generate_matrix(20, 20)
write_to_file(matrix1, 'matrix1')
write_to_file(matrix2, 'matrix2')
matrixR = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix2[0]))]

for i in range(len(matrix1)):
    for j in range(len(matrix2[0])):
        proc = multiprocessing.Process(target=element, args=((i, j), matrix1, matrix2, q))
        proc.start()
        proc.join()

for i in range(len(matrix1)):
    for j in range(len(matrix2[0])):
        r = q.get()
        matrixR[r['i']][r['j']] = r['res']

write_to_file(matrixR, 'matrixR')