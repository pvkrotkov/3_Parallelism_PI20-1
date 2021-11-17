import multiprocessing
import random


def gen_matrix(n, m):
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(m):
            matrix[i].append(random.randint(1, 100))
    return matrix



def write_to_f(ma, filename):
    with open(filename, "w") as f:
        for line in ma:
            f.write(' '.join([str(elem) for elem in line])+'\n')



def read_from_f(filename):
    with open(filename, 'r') as f:
        m, matrix = [], []
        lines = f.readlines()
        for line in lines:
            m.append(line[0:len(line)-2].split())
        for line in m:
            matrix.append([int(item) for item in line])

    return matrix



def element(index, m1, m2, queue):
    i, j = index
    # res = sum([m1[i][k] * m2[k][i] for k in range(len(m1))])
    res = sum([m1[i][k] * m2[k][j] for k in range(len(m1))])

    dict_save_res = {'res': res, 'i': i, 'j': j}

    queue.put(dict_save_res)



if __name__ == '__main__':
    queue = multiprocessing.Manager().Queue()

    matrix1 = gen_matrix(30, 30)
    matrix2 = gen_matrix(30, 30)

    lon = len(matrix1)

    write_to_f(matrix1, 'matrix1')
    write_to_f(matrix2, 'matrix2')
    # print(read_from_f("matrix1"))
    # print(read_from_f("matrix2"))

    matrixR = [[0 for _ in range(lon)] for _ in range(lon)]

    for i in range(lon):
        for j in range(lon):
            proc = multiprocessing.Process(target=element, args=((i, j), matrix1, matrix2, queue))
            proc.start()
            proc.join()

    for i in range(lon):
        for j in range(lon):
            r = queue.get()
            matrixR[r['i']][r['j']] = r['res']



    write_to_f(matrixR, 'matrixR')